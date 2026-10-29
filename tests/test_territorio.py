"""Verifica dados completos, recorte comum, persistência e atualização independente dos seletores."""
import copy
import json
from io import BytesIO
from pypdf import PdfReader
from pathlib import Path

import numpy as np
import pytest
from fastapi.testclient import TestClient
from rasterio.io import MemoryFile
from rasterio.transform import from_origin
from shapely.geometry import LineString, Polygon, mapping, shape

from geovale.api.main import RAIZ, criar_app
from geovale.camadas import CAMADAS
from geovale.fontes_territorio import (MAX_REGISTROS, esquema_wfs, ler_legenda, obter_wfs,
                                     recortar_raster, recortar_vetores)
from geovale.influencia import ler_influencia
from geovale.mapa import FonteIndisponivel
from geovale.territorio import DadosTerritoriais, catalogar_bases

TOTAL = len(catalogar_bases(CAMADAS))


def preparar_raiz(tmp_path):
    pasta = tmp_path / 'dados/influencias'
    pasta.mkdir(parents=True)
    (tmp_path / 'dados/minas.json').write_text('[{"id":"horizontes","nome":"Mina Horizontes","municipio":"Nova Lima","uf":"MG","empresa":"VALE S.A."}]')
    cenarios = tmp_path / 'dados/cenarios'; cenarios.mkdir()
    (cenarios / 'horizontes.json').write_bytes((RAIZ / 'dados/cenarios/horizontes.json').read_bytes())
    original = RAIZ / 'dados/influencias/horizontes.geojson'
    (pasta / 'horizontes.geojson').write_bytes(original.read_bytes())
    return tmp_path


def coleta_simulada(base, recorte):
    assert recorte.geom_type == 'Polygon'
    return {'tipo': 'vetor', 'quantidade': 1, 'campos': [{'name': 'extra'}, {'name': 'vazio'}],
            'dados': {'type': 'FeatureCollection', 'features': [{'type': 'Feature', 'id': '1',
                      'geometry': mapping(recorte), 'properties': {'extra': 'conservado', 'vazio': None}}]},
            'crs': 'EPSG:4326', 'aviso': 'teste'}, None


def test_catalogo_inteiro_persistido_reabre_sem_rede_e_nova_base_entra_sozinha(tmp_path):
    raiz = preparar_raiz(tmp_path)
    catalogo = copy.deepcopy(CAMADAS)
    chamadas = []
    def coletar(base, recorte):
        chamadas.append(base['camada'])
        return coleta_simulada(base, recorte)
    fonte = DadosTerritoriais(raiz, catalogo=catalogo, coletar=coletar)
    assert fonte.obter('horizontes')['bases_prontas'] == 0
    fonte.atualizar()
    d = fonte.obter('horizontes')
    assert d['completo'] and d['total_bases'] == TOTAL
    assert len(chamadas) == TOTAL
    assert {b['tema_id'] for b in d['bases']} == {t['id'] for t in CAMADAS}
    for b in d['bases']:
        registro = fonte.registros('horizontes', b['id'])
        assert registro['dados']['features'][0]['properties'] == {'extra': 'conservado', 'vazio': None}
    segunda = DadosTerritoriais(raiz, catalogo=catalogo, coletar=lambda *args: pytest.fail('não deve consultar'))
    assert segunda.obter('horizontes')['completo']
    segunda.atualizar()
    catalogo[0]['bases'].append({**catalogo[0]['bases'][0], 'camada': 'IDE:nova_base_teste', 'nome': 'Nova base'})
    assert fonte.obter('horizontes')['total_bases'] == TOTAL + 1
    assert fonte.obter('horizontes')['bases_prontas'] == TOTAL
    fonte.atualizar()
    assert fonte.obter('horizontes')['completo']
    assert len(chamadas) == TOTAL + 1
    assert chamadas[-1] == 'IDE:nova_base_teste'


def test_mudar_recorte_invalida_dados_incompativeis_e_reprocessa(tmp_path):
    raiz = preparar_raiz(tmp_path)
    chamadas = []
    def coletar(base, recorte):
        chamadas.append(base['camada'])
        return coleta_simulada(base, recorte)
    fonte = DadosTerritoriais(raiz, coletar=coletar)
    fonte.atualizar()
    arquivo = raiz / 'dados/influencias/horizontes.geojson'
    d = json.loads(arquivo.read_text())
    d['fonte']['preparado_em'] = 'nova revisão'
    arquivo.write_text(json.dumps(d))
    assert fonte.obter('horizontes')['bases_prontas'] == 0
    fonte.atualizar()
    assert fonte.obter('horizontes')['completo']
    assert len(chamadas) == 2 * TOTAL


def test_falha_nao_vira_zero_ultimo_dado_identificado_e_recupera_so_base_com_erro(tmp_path):
    raiz = preparar_raiz(tmp_path)
    agora, falhar, chamadas = [100000], [False], []
    camada = CAMADAS[0]['bases'][0]['camada']
    def coletar(base, recorte):
        chamadas.append(base['camada'])
        if falhar[0] and base['camada'] == camada:
            raise OSError('fonte indisponível')
        return coleta_simulada(base, recorte)
    fonte = DadosTerritoriais(raiz, coletar=coletar, relogio=lambda: agora[0])
    fonte.atualizar()
    assert fonte.obter('horizontes')['completo']
    agora[0] += 86401
    falhar[0] = True
    fonte.atualizar()
    d = fonte.obter('horizontes')
    erro = next(b for b in d['bases'] if b['camada'] == camada)
    assert not d['completo'] and d['bases_prontas'] == TOTAL - 1
    assert erro['estado'] == 'erro' and erro['quantidade'] == 1 and erro['consultado_em']
    assert len(chamadas) == 2 * TOTAL
    fonte.atualizar()
    assert len(chamadas) == 2 * TOTAL
    agora[0] += 301
    falhar[0] = False
    fonte.atualizar()
    assert fonte.obter('horizontes')['completo']
    assert len(chamadas) == 2 * TOTAL + 1


def test_pacote_tem_so_contorno_externo_e_mina_sombreada():
    d = ler_influencia(RAIZ / 'dados/influencias/horizontes.geojson', 'horizontes')
    assert {f['properties']['id'] for f in d['features']} == {'mina', 'influencia'}
    assert len(d['features']) == 2
    influencia = next(f for f in d['features'] if f['properties']['id'] == 'influencia')
    assert influencia['properties']['identificador_original'] == 'aii_agua_solos'
    assert influencia['properties']['pagina_pdf'] == 18
    assert len(d['fonte']['sha256_pdf']) == 64
    assert shape(influencia['geometry']).is_valid


def test_api_catalogo_completo_independe_camadas_visiveis_e_rotas_antigas_sumiram(tmp_path):
    raiz = preparar_raiz(tmp_path)
    fonte = DadosTerritoriais(raiz, coletar=coleta_simulada)
    fonte.atualizar()
    cliente = TestClient(criar_app(raiz=raiz, territorios=fonte))
    d = cliente.get('/api/minas/horizontes/territorio?ativas=agua').json()
    assert d['completo'] and d['total_bases'] == TOTAL
    assert cliente.get('/api/minas/outra/territorio').status_code == 404
    assert cliente.get('/api/minas/horizontes/influencia').status_code == 200
    assert cliente.get('/api/minas/horizontes/territorio/inexistente').status_code == 404
    url = d['bases'][0]['dados_url']
    assert cliente.get(url).json()['dados']['features'][0]['properties']['extra'] == 'conservado'
    assert cliente.get(url + '/arquivo').status_code == 404
    for rota in ['/api/minas/horizontes/referencias', '/api/minas/horizontes/agua-influencia']:
        assert cliente.get(rota).status_code == 404
    assert cliente.post('/api/area/validar', json={}).status_code == 404


def feicao(chave, geom, props=None):
    return {'type': 'Feature', 'id': chave, 'geometry': mapping(geom), 'properties': props or {'extra': 7, 'nulo': None}}


def test_vetor_recorta_poligono_irregular_preserva_atributos_e_conta_multipartes_uma_vez():
    roi = Polygon([(0, 0), (4, 0), (0, 4)])
    doc = {'type': 'FeatureCollection', 'features': [
        feicao('a', LineString([(-1, 1), (4, 1)])),
        feicao('b', LineString([(3, 3), (4, 3)])),
        feicao('c', LineString([(-1, -1), (0, 0)])),
    ]}
    fs = recortar_vetores(doc, roi, ('LineString', 'MultiLineString'), ['extra', 'nulo'])
    assert len(fs) == 1 and fs[0]['properties'] == {'extra': 7, 'nulo': None}
    assert shape(fs[0]['geometry']).equals(LineString([(0, 1), (3, 1)]))
    assert recortar_vetores({'type': 'FeatureCollection', 'features': []}, roi, ('Polygon', 'MultiPolygon'), []) == []


@pytest.mark.parametrize('defeito', ['campo_omitido', 'duplicada', 'geometria_invalida'])
def test_vetor_incompleto_ou_invalido_nao_e_sucesso(defeito):
    f = feicao('a', LineString([(0, 0), (1, 1)]))
    fs = [f]
    if defeito == 'campo_omitido': del f['properties']['extra']
    if defeito == 'duplicada': fs.append(copy.deepcopy(f))
    if defeito == 'geometria_invalida': f['geometry'] = mapping(LineString([(0, 0), (0, 0)]))
    with pytest.raises(FonteIndisponivel):
        recortar_vetores({'type': 'FeatureCollection', 'features': fs}, Polygon([(-1, -1), (3, -1), (0, 3)]), ('LineString', 'MultiLineString'), ['extra', 'nulo'])


ESQUEMA = b'<xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema"><xsd:sequence><xsd:element name="id" type="xsd:int"/><xsd:element name="geom" type="gml:MultiCurvePropertyType"/><xsd:element name="extra" type="xsd:string"/></xsd:sequence></xsd:schema>'


def test_wfs_descobre_campos_e_nao_usa_lista_parcial_de_atributos(monkeypatch):
    chamadas = []
    def consultar(url, par, limite=None):
        chamadas.append(par)
        if par['request'] == 'DescribeFeatureType': return ESQUEMA
        assert 'propertyName' not in par
        return json.dumps({'type': 'FeatureCollection', 'features': [], 'numberMatched': 0,
                           'numberReturned': 0, 'crs': {'properties': {'name': 'EPSG:4326'}}}).encode()
    monkeypatch.setattr('geovale.fontes_territorio.consultar', consultar)
    resultado, _ = obter_wfs({'camada': 'IDE:teste'}, Polygon([(0, 0), (1, 0), (0, 1)]))
    assert [c['name'] for c in resultado['campos']] == ['id', 'extra']
    assert resultado['quantidade'] == 0
    assert chamadas[-1]['count'] == MAX_REGISTROS + 1
    assert chamadas[-1]['srsName'] == 'EPSG:4326'


@pytest.mark.parametrize('tipo', ['truncado', 'crs'])
def test_wfs_truncado_ou_crs_incompativel_falha(monkeypatch, tipo):
    def consultar(url, par, limite=None):
        if par['request'] == 'DescribeFeatureType': return ESQUEMA
        return json.dumps({'type': 'FeatureCollection', 'features': [], 'numberMatched': 1 if tipo == 'truncado' else 0,
                           'numberReturned': 0, 'crs': {'properties': {'name': 'EPSG:31983' if tipo == 'crs' else 'EPSG:4326'}}}).encode()
    monkeypatch.setattr('geovale.fontes_territorio.consultar', consultar)
    with pytest.raises(FonteIndisponivel): obter_wfs({'camada': 'IDE:teste'}, Polygon([(0, 0), (1, 0), (0, 1)]))


def raster_teste():
    valores = np.ones((8, 8), dtype='uint8')
    valores[3, 3] = 0
    valores[4, 4] = 2
    with MemoryFile() as memoria:
        with memoria.open(driver='GTiff', width=8, height=8, count=1, dtype='uint8', crs='EPSG:4674', transform=from_origin(-4, 4, 1, 1), nodata=0) as d:
            d.write(valores, 1)
        return memoria.read()


def test_raster_conserva_grade_valores_nodata_classes_e_arquivo_com_mascara():
    roi = Polygon([(-2, -2), (2, -2), (2, 2), (-2, 2)])
    legenda = {1: {'codigo': 1, 'nome': 'Classe 1', 'cor': '#ff0000'}, 2: {'codigo': 2, 'nome': 'Classe 2', 'cor': '#00ff00'}}
    d, artefato = recortar_raster(raster_teste(), roi, legenda)
    assert d['quantidade'] == 15 and d['celulas_no_recorte'] == 16 and d['celulas_sem_dados'] == 1
    assert sum(c['celulas'] for c in d['classes']) == 15
    assert d['resolucao'] == [1, 1] and d['crs'] == 'EPSG:4674'
    with MemoryFile(artefato) as m, m.open() as raster:
        valores = raster.read(1, masked=True)
        assert valores.count() == 15
        assert valores[4, 4] == 2 and valores.mask[0, 0]
        assert raster.transform == from_origin(-4, 4, 1, 1)


def test_raster_sem_legenda_da_classe_nao_inventa_categoria():
    with pytest.raises(FonteIndisponivel): recortar_raster(raster_teste(), Polygon([(-2, -2), (2, -2), (2, 2), (-2, 2)]), {})


def test_legenda_escolhe_apenas_estilo_oficial_padrao():
    xml = b'<sld:StyledLayerDescriptor xmlns:sld="http://www.opengis.net/sld"><sld:UserStyle><sld:IsDefault>1</sld:IsDefault><sld:ColorMapEntry quantity="1" color="#ff0000" label="Classe original"/></sld:UserStyle><sld:UserStyle><sld:ColorMapEntry quantity="1" color="#00ff00" label="Outra classificacao"/></sld:UserStyle></sld:StyledLayerDescriptor>'
    assert ler_legenda(xml)[1]['nome'] == 'Classe original'
    assert ler_legenda(xml)[1]['cor'] == '#ff0000'


def test_catalogo_duplicado_e_recorte_invalido_sao_rejeitados(tmp_path):
    with pytest.raises(ValueError): catalogar_bases([CAMADAS[0], CAMADAS[0]])
    raiz = preparar_raiz(tmp_path)
    arquivo = raiz / 'dados/influencias/horizontes.geojson'
    d = json.loads(arquivo.read_text()); d['features'].pop(); arquivo.write_text(json.dumps(d))
    with pytest.raises(ValueError): ler_influencia(arquivo, 'horizontes')


def test_dados_ficam_isolados_por_mina(tmp_path):
    raiz = preparar_raiz(tmp_path)
    arquivo = raiz / 'dados/influencias/horizontes.geojson'
    outra = json.loads(arquivo.read_text())
    outra['mina_id'] = 'outra'
    (raiz / 'dados/influencias/outra.geojson').write_text(json.dumps(outra))
    (raiz / 'dados/minas.json').write_text('[{"id":"horizontes"},{"id":"outra"}]')
    fonte = DadosTerritoriais(raiz, coletar=coleta_simulada)
    fonte.atualizar()
    assert fonte.obter('horizontes')['completo'] and fonte.obter('outra')['completo']
    with fonte.conectar() as db:
        db.execute('DELETE FROM bases WHERE mina=?', ('horizontes',))
    assert fonte.obter('horizontes')['bases_prontas'] == 0
    assert fonte.obter('outra')['bases_prontas'] == TOTAL


def test_lifespan_prepara_dados_sem_clique_e_encerra_agendamento(tmp_path):
    from threading import Event, Lock
    raiz = preparar_raiz(tmp_path)
    terminou_consultas, trava = Event(), Lock()
    chamadas = []
    def coletar(base, recorte):
        with trava:
            chamadas.append(base['id'])
            if len(chamadas) == 11:
                terminou_consultas.set()
        return coleta_simulada(base, recorte)
    fonte = DadosTerritoriais(raiz, coletar=coletar)
    with TestClient(criar_app(raiz=raiz, territorios=fonte)) as cliente:
        assert terminou_consultas.wait(timeout=5)
        with fonte._ciclo:
            pass
        assert cliente.get('/api/minas/horizontes/territorio').json()['completo']
    assert not fonte._thread.is_alive()


def test_relatorio_pdf_usa_catalogo_inteiro_sem_rede_e_preserva_dados_internos(tmp_path):
    raiz = preparar_raiz(tmp_path)
    def coletar(base, recorte):
        if base['processamento'] != 'wcs':
            return coleta_simulada(base, recorte)
        return recortar_raster(raster_teste(), Polygon([(-2, -2), (2, -2), (2, 2), (-2, 2)]),
                              {1: {'codigo': 1, 'nome': 'Classe 1', 'cor': '#ff0000'}, 2: {'codigo': 2, 'nome': 'Classe 2', 'cor': '#00ff00'}})
    fonte = DadosTerritoriais(raiz, coletar=coletar)
    cliente = TestClient(criar_app(raiz=raiz, territorios=fonte))
    assert cliente.get('/api/minas/horizontes/relatorio').status_code == 503
    fonte.atualizar()
    fonte.coletar = lambda *args: pytest.fail('Exportar não pode consultar fontes')
    resposta = cliente.get('/api/minas/horizontes/relatorio?ativas=agua')
    assert resposta.status_code == 200
    assert resposta.headers['content-disposition'] == 'inline; filename="geovale-horizontes.pdf"'
    assert resposta.headers['content-type'] == 'application/pdf'
    assert resposta.headers['cache-control'] == 'no-store'
    assert resposta.content.startswith(b'%PDF')
    pdf = PdfReader(BytesIO(resposta.content))
    assert pdf.metadata.author == 'GeoVale' and len(pdf.outline) == len(CAMADAS) + 2
    texto = '\n'.join(p.extract_text() for p in pdf.pages)
    assert 'VALE S.A.' not in texto
    assert 'Dados técnicos simulados' in texto and 'Valores fictícios' in texto
    assert 'Fonte' in texto and 'Minas-Rio' in texto and '15' in texto
    relatorio = fonte.relatorio('horizontes')
    assert relatorio['completo'] and len(relatorio['bases']) == TOTAL
    for base in relatorio['bases']:
        assert base['consultado_em'] and base['recorte']['assinatura']
        assert base['base']['nome'].replace('—', '-') in ' '.join(texto.split())
        if base['tipo'] == 'vetor':
            assert base['dados']['features'][0]['properties'] == {'extra': 'conservado', 'vazio': None}
        else:
            assert 'valores' not in base
            assert base['crs'] == 'EPSG:4674' and base['dimensoes'] == [8, 8]
            with MemoryFile(fonte.arquivo('horizontes', base['base']['id'])) as m, m.open() as raster:
                valores = raster.read(1, masked=True)
                assert valores.count() == base['quantidade'] == 15 and valores[4, 4] == 2
    baixar = cliente.get('/api/minas/horizontes/relatorio?baixar=true')
    assert baixar.content == resposta.content
    assert baixar.headers['content-disposition'] == 'attachment; filename="geovale-horizontes.pdf"'
    assert cliente.get('/api/minas/outra/relatorio').status_code == 404
    with fonte.conectar() as db:
        db.execute("UPDATE bases SET estado='erro' WHERE camada=?", (CAMADAS[0]['bases'][0]['camada'],))
    assert cliente.get('/api/minas/horizontes/relatorio').status_code == 503


def test_relatorio_rejeita_dados_vencidos_ou_de_outro_recorte(tmp_path):
    raiz = preparar_raiz(tmp_path)
    agora = [100000]
    fonte = DadosTerritoriais(raiz, coletar=coleta_simulada, relogio=lambda: agora[0])
    fonte.atualizar()
    agora[0] += 86401
    with pytest.raises(ValueError): fonte.relatorio('horizontes')
    agora[0] -= 86401
    arquivo = raiz / 'dados/influencias/horizontes.geojson'
    d = json.loads(arquivo.read_text()); d['fonte']['preparado_em'] = 'revisado'; arquivo.write_text(json.dumps(d))
    with pytest.raises(ValueError): fonte.relatorio('horizontes')


def test_trilhas_visuais_cortam_na_borda_irregular_sem_mudar_cor_ou_fonte():
    from geovale.trilhas import recortar_trilhas
    roi = Polygon([(0, 0), (4, 0), (0, 4)])
    dados = {'type': 'FeatureCollection', 'fonte': {'url': 'oficial'}, 'legenda': [
        {'id': 'dentro', 'nome': 'Dentro', 'cor': '#123456'}, {'id': 'fora', 'nome': 'Fora', 'cor': '#abcdef'}],
        'features': [
            feicao('a', LineString([(-1, 1), (4, 1)]), {'nome': 'Dentro', 'cor': '#123456', 'largura': 2}),
            feicao('b', LineString([(3, 3), (4, 3)]), {'nome': 'Fora', 'cor': '#abcdef', 'largura': 2}),
            feicao('c', LineString([(-1, -1), (0, 0)]), {'nome': 'Fora', 'cor': '#abcdef', 'largura': 2}),
        ]}
    saida = recortar_trilhas(dados, roi)
    assert len(saida['features']) == 1 and len(dados['features']) == 3
    assert shape(saida['features'][0]['geometry']).equals(LineString([(0, 1), (3, 1)]))
    assert saida['features'][0]['properties'] == dados['features'][0]['properties']
    assert saida['legenda'] == dados['legenda'][:1] and saida['fonte'] == dados['fonte']


def test_api_trilhas_da_influencia_nao_inclui_linhas_fora_do_poligono(tmp_path):
    from geovale.trilhas import TrilhasMunicipais
    from test_trilhas import trilha_valida, simbologia_valida
    raiz = preparar_raiz(tmp_path)
    fonte = TrilhasMunicipais(consultar=lambda _: trilha_valida(), consultar_simbolos=simbologia_valida)
    cliente = TestClient(criar_app(raiz=raiz, trilhas=fonte))
    resposta = cliente.get('/api/minas/horizontes/trilhas-influencia')
    assert resposta.status_code == 200
    roi = shape(next(f['geometry'] for f in ler_influencia(raiz / 'dados/influencias/horizontes.geojson', 'horizontes')['features'] if f['properties']['id'] == 'influencia'))
    assert resposta.json()['features']
    assert all(roi.covers(shape(f['geometry'])) for f in resposta.json()['features'])
    assert cliente.get('/api/minas/outra/trilhas-influencia').status_code == 404


def test_pdf_invalida_cache_se_cenario_muda_e_recusa_cenario_sem_rotulo_simulado(tmp_path):
    from geovale.relatorio import RelatoriosPDF
    raiz = preparar_raiz(tmp_path)
    fonte = DadosTerritoriais(raiz, coletar=coleta_simulada)
    fonte.atualizar()
    relatorios = RelatoriosPDF(fonte, raiz)
    primeiro = relatorios.obter('horizontes')
    assert relatorios.obter('horizontes') is primeiro
    p = raiz / 'dados/cenarios/horizontes.json'
    c = json.loads(p.read_text())
    c['dados'][0]['nome'] = 'Revisão fictícia demonstrativa'
    p.write_text(json.dumps(c))
    segundo = relatorios.obter('horizontes')
    assert primeiro != segundo
    assert 'Revisão fictícia demonstrativa' in ' '.join(' '.join(pg.extract_text() for pg in PdfReader(BytesIO(segundo)).pages).split())
    c['natureza'] = 'real'; p.write_text(json.dumps(c))
    with pytest.raises(ValueError): relatorios.obter('horizontes')
    cliente = TestClient(criar_app(raiz=raiz, territorios=fonte))
    assert cliente.get('/api/minas/horizontes/relatorio').status_code == 503


def test_dados_fixos_nao_coletam_nem_vencem(tmp_path):
    raiz = preparar_raiz(tmp_path)
    agora = [1000.]
    fonte = DadosTerritoriais(raiz, coletar=coleta_simulada, relogio=lambda: agora[0])
    fonte.atualizar()
    assert fonte.obter('horizontes')['completo']
    agora[0] += 2 * 24 * 3600
    assert not fonte.obter('horizontes')['completo']
    fixa = DadosTerritoriais(raiz, coletar=lambda *a: pytest.fail('dados fixos não coletam'), relogio=lambda: agora[0], fixos=True)
    fixa.iniciar()
    assert fixa._thread is None and fixa.obter('horizontes')['completo'] and fixa.relatorio('horizontes')['completo']
