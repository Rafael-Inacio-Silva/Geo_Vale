"""Verifica a fonte externa, disponibilidade e contrato da etapa territorial."""

from concurrent.futures import ThreadPoolExecutor
import pytest
from fastapi.testclient import TestClient

from geovale.api.main import criar_app
from geovale.mapa import FonteIndisponivel, LimiteEstadual, preparar_limite


def documento_estado():
    """Cria geometria sintética exclusivamente para testes de contrato."""
    return {
        'type': 'FeatureCollection',
        'features': [{'type': 'Feature', 'properties': {'geocodigo': '31'}, 'geometry': {
            'type': 'Polygon', 'coordinates': [[[-51, -23], [-40, -23], [-40, -14], [-51, -14], [-51, -23]]],
        }}],
    }


def test_jornada_http_sem_acesso_externo():
    """Uma mina, localização, contorno e rotas restritas ao mapa formam o contrato público."""
    cliente = TestClient(criar_app(LimiteEstadual(consultar=documento_estado)))
    assert cliente.get('/api/saude').json()['status'] == 'ok'
    resposta = cliente.get('/api/mapa')
    assert resposta.status_code == 200
    dados = resposta.json()
    assert [m['id'] for m in dados['minas']] == ['horizontes']
    assert dados['minas'][0]['municipio'] == 'Nova Lima'
    assert -20.14 < dados['minas'][0]['latitude'] < -20.10
    assert {f['id'] for f in dados['fundos']} == {'mapa', 'satelite'}
    assert all(f['url'].startswith('https://') and f['credito'] for f in dados['fundos'])
    limite = cliente.get('/api/mapa/limite-mg')
    assert limite.status_code == 200
    assert limite.json()['features'][0]['properties']['codigo_uf'] == '31'
    assert limite.json()['fonte']['crs'] == 'EPSG:4326'
    assert cliente.post('/api/mapa', json={}).status_code == 405
    assert cliente.get('/api/mapa/qualquer').status_code == 404
    assert cliente.get('/api/qualquer').status_code == 404


def test_cache_e_concorrencia_nao_repetem_download():
    chamadas = []
    def consultar():
        chamadas.append(1)
        return documento_estado()
    fonte = LimiteEstadual(consultar=consultar)
    with ThreadPoolExecutor(max_workers=4) as pool:
        resultados = list(pool.map(lambda _: fonte.obter(), range(4)))
    assert len(chamadas) == 1
    resultados[0]['features'].clear()
    assert len(fonte.obter()['features']) == 1


def test_autointersecao_da_fonte_recebe_ajuste_apenas_visual():
    dados = documento_estado()
    dados['features'][0]['geometry']['coordinates'] = [
        [[-51, -23], [-40, -14], [-51, -14], [-40, -23], [-51, -23]],
    ]
    exibicao = preparar_limite(dados)
    assert exibicao['fonte']['ajuste_topologico_visual'] is True
    assert exibicao['features'][0]['geometry']['type'] in ('Polygon', 'MultiPolygon')


def test_falha_inicial_informa_503_e_permite_tentar_novamente():
    chamadas = []
    def consultar():
        chamadas.append(1)
        if len(chamadas) == 1:
            raise OSError('Falha privada da conexão')
        return documento_estado()
    cliente = TestClient(criar_app(LimiteEstadual(consultar=consultar)))
    erro = cliente.get('/api/mapa/limite-mg')
    assert erro.status_code == 503
    assert 'privada' not in erro.text
    assert cliente.get('/api/mapa').status_code == 200
    assert cliente.get('/api/mapa/limite-mg').status_code == 200


def test_expiracao_renova_e_falha_preserva_data_da_ultima_resposta():
    tempo = [0]
    falhar = [False]
    chamadas = []
    def consultar():
        chamadas.append(1)
        if falhar[0]:
            raise OSError('Sem conexão')
        return documento_estado()
    fonte = LimiteEstadual(consultar=consultar, relogio=lambda: tempo[0])
    inicial = fonte.obter()
    tempo[0] = 3601
    falhar[0] = True
    antigo = fonte.obter()
    assert antigo['aviso']
    assert antigo['fonte']['consultado_em'] == inicial['fonte']['consultado_em']
    falhar[0] = False
    assert fonte.obter()['aviso'] is None
    assert len(chamadas) == 3


@pytest.mark.parametrize('alteracao', ['identidade', 'geometria', 'crs', 'extensao', 'vazio'])
def test_fonte_incompativel_nao_e_exibida_como_minas_gerais(alteracao):
    dados = documento_estado()
    if alteracao == 'identidade':
        dados['features'][0]['properties']['geocodigo'] = '35'
    elif alteracao == 'geometria':
        dados['features'][0]['geometry'] = {'type': 'Point', 'coordinates': [-44, -18]}
    elif alteracao == 'crs':
        dados['crs'] = {'properties': {'name': 'EPSG:3857'}}
    elif alteracao == 'extensao':
        dados['features'][0]['geometry']['coordinates'] = [[[0, 0], [1, 0], [1, 1], [0, 0]]]
    else:
        dados['features'] = []
    with pytest.raises(FonteIndisponivel):
        preparar_limite(dados)


def test_interface_compilada_e_rotas_desconhecidas(tmp_path):
    """O HTML é servido somente na raiz; URLs inexistentes não mascaram erro como SPA."""
    (tmp_path / 'dados').mkdir()
    (tmp_path / 'dados/minas.json').write_text('[]')
    (tmp_path / 'frontend/dist/assets').mkdir(parents=True)
    (tmp_path / 'frontend/dist/index.html').write_text('<html lang="pt-BR">GeoVale</html>')
    cliente = TestClient(criar_app(LimiteEstadual(consultar=documento_estado), raiz=tmp_path))
    assert cliente.get('/').status_code == 200
    assert cliente.get('/arquivo-inexistente').status_code == 404
    assert cliente.get('/assets/arquivo-inexistente.js').status_code == 404


def test_sem_build_retorna_orientacao(tmp_path):
    (tmp_path / 'dados').mkdir()
    (tmp_path / 'dados/minas.json').write_text('[]')
    cliente = TestClient(criar_app(raiz=tmp_path))
    assert cliente.get('/').status_code == 503
    assert 'Compile' in cliente.get('/').json()['mensagem']


def test_catalogo_tematico_integra_fontes_estadual_e_municipal():
    """A interface recebe grupos estaduais e municipal completos, sem depender do WMS no início."""
    from urllib.parse import parse_qs, urlsplit
    cliente = TestClient(criar_app(LimiteEstadual(consultar=lambda: (_ for _ in ()).throw(OSError()))))
    resposta = cliente.get('/api/mapa')
    assert resposta.status_code == 200
    temas = resposta.json()['camadas']
    assert {t['id'] for t in temas} == {'relevo', 'agua', 'solos', 'vegetacao', 'entorno', 'barragens', 'trilhas'}
    assert len({t['ordem'] for t in temas}) == 7
    bases = [b for tema in temas for b in tema['bases']]
    assert len(bases) == len({b['camada'] for b in bases}) == 16
    for tema in temas:
        if tema['tipo'] == 'geojson':
            assert tema['url'] == '/api/mapa/trilhas' and tema['alcance'] == 'Nova Lima'
            continue
        assert urlsplit(tema['url']).hostname == 'geoserver.meioambiente.mg.gov.br'
        assert tema['credito'] and 0.1 <= tema['opacidade'] <= 1
        for base in tema['bases']:
            legenda = parse_qs(urlsplit(base['legenda']).query)
            assert legenda['request'] == ['GetLegendGraphic']
            assert legenda['layer'] == [base['camada']]
            assert urlsplit(base['metadado']).hostname == 'idesisema.meioambiente.mg.gov.br'
    assert cliente.get('/api/mapa/limite-mg').status_code == 503
    assert cliente.get('/api/mapa').json()['camadas'] == temas
