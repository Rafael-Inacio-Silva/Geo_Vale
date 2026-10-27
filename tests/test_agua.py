"""Verifica recorte irregular real, contagem cadastral, completude e recuperação sem rede."""
import copy
from urllib.parse import parse_qs, urlparse

import pytest
from fastapi.testclient import TestClient
from shapely.geometry import Polygon, LineString, MultiLineString, mapping, shape

from geovale.agua import BASES, ExtracaoAgua, MAX_BYTES, MAX_FEICOES, consultar_base
from geovale.api.main import criar_app
from geovale.mapa import FonteIndisponivel


def referencias_teste():
    return {'features': [{'properties': {'id': 'aid_agua_solos'},
                          'geometry': mapping(Polygon([(0, 0), (4, 0), (0, 4)]))}],
            'fonte': {'url': 'https://fonte.gov.br/parecer.pdf', 'sha256_pdf': 'a' * 64}}


def registro(base, chave, geometria):
    propriedades = ({'id': chave, 'noriocomp': 'Rio teste', 'dsversao': 'Versão teste', 'datverbase': None}
                   if base['id'] == 'trechos' else
                   {'id_0': chave, 'nmoriginal': None, 'nmalternat': None, 'detipomass': 'Artificial', 'deversao': None})
    return {'type': 'Feature', 'id': base['camada'].split(':')[1] + '.' + str(chave),
            'properties': propriedades, 'geometry': mapping(geometria)}


def documento(feicoes):
    return {'type': 'FeatureCollection', 'features': feicoes, 'numberMatched': len(feicoes),
            'numberReturned': len(feicoes), 'crs': {'properties': {'name': 'EPSG:4326'}}}


def consulta_teste(base, limites):
    assert limites == (0, 0, 4, 4)
    if base['id'] == 'trechos':
        return documento([
            registro(base, 1, LineString([(-1, 1), (4, 1)])),
            registro(base, 2, LineString([(3, 3), (4, 3)])),  # Dentro do bbox, fora do triângulo.
            registro(base, 3, LineString([(-1, -1), (0, 0)])),  # Só encosta num ponto.
            registro(base, 4, MultiLineString([[(0, 2), (3, 2)], [(0, 3), (2, 3)]])),
        ])
    return documento([registro(base, 8, Polygon([(0, 0), (4, 0), (4, 4), (0, 4)]))])


def test_intersecao_exata_conserva_ids_conta_registro_uma_vez_e_nao_inventa_nome():
    referencias = referencias_teste()
    resultado = ExtracaoAgua(consultar=consulta_teste).obter(referencias)
    assert resultado['resumo'] == {'trechos': 2, 'massas': 1}
    roi = shape(referencias['features'][0]['geometry'])
    assert all(roi.covers(shape(f['geometry'])) for f in resultado['features'])
    assert [f['properties']['id_fonte'].split('.')[-1] for f in resultado['features']] == ['1', '4', '8']
    assert shape(resultado['features'][0]['geometry']).equals(LineString([(0, 1), (3, 1)]))
    assert shape(resultado['features'][2]['geometry']).equals(roi)
    assert resultado['features'][2]['properties']['nome'] is None
    assert resultado['fontes'][0]['registros_consultados'] == 4
    assert resultado['fontes'][1]['versoes_publicadas'] == []
    assert resultado['recorte']['id'] == 'aid_agua_solos'
    assert len(resultado['recorte']['sha256_recorte']) == 64


@pytest.mark.parametrize('defeito', ['truncada', 'demais', 'crs', 'duplicada', 'id', 'nula', 'invalida', 'campo'])
def test_fonte_incompativel_falha_inteira_sem_resumo_parcial(defeito):
    def consultar(base, limites):
        d = consulta_teste(base, limites)
        if base['id'] != 'trechos':
            return d
        if defeito == 'truncada': d['numberMatched'] += 1
        elif defeito == 'demais': d['numberMatched'] = MAX_FEICOES + 1
        elif defeito == 'crs': d['crs']['properties']['name'] = 'EPSG:31983'
        elif defeito == 'duplicada': d['features'][1] = copy.deepcopy(d['features'][0])
        elif defeito == 'id': d['features'][0]['id'] = 'outra_base.1'
        elif defeito == 'nula': d['features'][0]['geometry'] = None
        elif defeito == 'invalida': d['features'][0]['geometry'] = mapping(LineString([(0, 0), (0, 0)]))
        elif defeito == 'campo': del d['features'][0]['properties']['noriocomp']
        return d
    with pytest.raises(FonteIndisponivel):
        ExtracaoAgua(consultar=consultar).obter(referencias_teste())


def test_resultado_vazio_e_completo_nao_e_falha():
    resultado = ExtracaoAgua(consultar=lambda *args: documento([])).obter(referencias_teste())
    assert resultado['features'] == []
    assert resultado['resumo'] == {'trechos': 0, 'massas': 0}


def test_cache_defensivo_expira_nao_entrega_vencido_na_falha_e_recupera():
    agora, chamadas, falhar = [0], [], [False]
    def consultar(base, limites):
        chamadas.append(base['id'])
        if falhar[0]: raise OSError('sem rede')
        return consulta_teste(base, limites)
    fonte = ExtracaoAgua(consultar=consultar, relogio=lambda: agora[0])
    referencias = referencias_teste()
    dados = fonte.obter(referencias)
    dados['features'].clear()
    assert len(fonte.obter(referencias)['features']) == 3
    assert len(chamadas) == 2
    agora[0] = 601
    falhar[0] = True
    with pytest.raises(FonteIndisponivel): fonte.obter(referencias)
    falhar[0] = False
    assert fonte.obter(referencias)['resumo']['trechos'] == 2
    total = len(chamadas)
    referencias['features'][0]['properties']['revisao'] = 'nova'
    fonte.obter(referencias)
    assert len(chamadas) == total + 2
    referencias['fonte']['sha256_pdf'] = 'b' * 64
    assert fonte.obter(referencias)['recorte']['sha256_pdf'] == 'b' * 64
    assert len(chamadas) == total + 4


def test_wfs_fixo_tem_campos_bbox_timeout_e_limite_de_bytes(monkeypatch):
    class Resposta:
        def __enter__(self): return self
        def __exit__(self, *args): pass
        def read(self, limite):
            assert limite == MAX_BYTES + 1
            return b'{}'
    def abrir(pedido, timeout):
        p = parse_qs(urlparse(pedido.full_url).query)
        assert urlparse(pedido.full_url).hostname == 'geoserver.meioambiente.mg.gov.br'
        assert p['typeNames'] == [BASES[0]['camada']]
        assert p['CQL_FILTER'] == ["BBOX(geom,-44,-21,-43,-20,'EPSG:4326')"]
        assert p['count'] == [str(MAX_FEICOES + 1)]
        assert p['propertyName'] == [BASES[0]['campos']]
        assert p['srsName'] == ['EPSG:4326']
        assert timeout == 15
        return Resposta()
    monkeypatch.setattr('geovale.agua.urlopen', abrir)
    assert consultar_base(BASES[0], (-44, -21, -43, -20)) == {}
    monkeypatch.setattr(Resposta, 'read', lambda *args: b' ' * (MAX_BYTES + 1))
    with pytest.raises(FonteIndisponivel): consultar_base(BASES[0], (-44, -21, -43, -20))


def test_api_recorte_fixo_404_503_recuperacao_e_independencia_do_desenho(tmp_path):
    falhar = [True]
    class Fonte:
        def obter(self, referencias):
            assert next(f for f in referencias['features'] if f['properties']['id'] == 'aid_agua_solos')
            if falhar[0]: raise FonteIndisponivel()
            return {'resumo': {'trechos': 0, 'massas': 0}, 'features': []}
    cliente = TestClient(criar_app(agua=Fonte()))
    assert cliente.get('/api/minas/outra/agua-influencia').status_code == 404
    assert cliente.get('/api/minas/horizontes/agua-influencia').status_code == 503
    falhar[0] = False
    resposta = cliente.get('/api/minas/horizontes/agua-influencia?recorte=aii_agua_solos&url=https://exemplo.com')
    assert resposta.status_code == 200
    assert resposta.headers['cache-control'] == 'no-store'
    assert resposta.json()['resumo'] == {'trechos': 0, 'massas': 0}
    (tmp_path / 'dados').mkdir()
    (tmp_path / 'dados/minas.json').write_text('[{"id":"horizontes"}]')
    assert TestClient(criar_app(raiz=tmp_path, agua=Fonte())).get('/api/minas/horizontes/agua-influencia').status_code == 503
