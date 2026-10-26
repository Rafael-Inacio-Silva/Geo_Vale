"""Verifica os recortes locais, sua procedência e independência de fornecedores externos."""
import copy
import json
from fastapi.testclient import TestClient
from shapely.geometry import shape, Point
from geovale.api.main import criar_app, RAIZ
from geovale.area import validar_area
from geovale.referencias import ler_referencias


def test_referencias_locais_com_procedencia_e_todos_os_recortes(monkeypatch):
    def proibido(*args, **kwargs):
        raise AssertionError('Não deve consultar fonte externa')
    monkeypatch.setattr('urllib.request.urlopen', proibido)
    cliente = TestClient(criar_app())
    assert cliente.get('/api/minas/desconhecida/referencias').status_code == 404
    resposta = cliente.get('/api/minas/horizontes/referencias?url=https://exemplo.com')
    assert resposta.status_code == 200
    dados = resposta.json()
    assert dados['fonte']['crs_original'] == 'EPSG:31983'
    assert dados['fonte']['crs_saida'] == 'EPSG:4326'
    assert len(dados['fonte']['sha256_pdf']) == 64
    assert {f['properties']['id'] for f in dados['features']} == {'mina_horizontes', 'ada_unificada', 'aid_hidrogeologia', 'aid_agua_solos', 'aii_agua_solos'}
    for f in dados['features']:
        assert f['properties']['aproximada'] is True
        assert shape(f['geometry']).is_valid
    referencia = next(f for f in dados['features'] if f['properties']['id'] == 'mina_horizontes')
    assert referencia['properties']['origem'] == 'referencia_osm'
    assert referencia['properties']['fonte']['osm_id'] == 315221699
    assert referencia['geometry'] == json.loads((RAIZ / 'dados/referencias/mineracao-osm.geojson').read_text())['geometry']
    assert all(f['properties']['pagina_pdf'] == 18 for f in dados['features'] if f != referencia)
    assert len(referencia['geometry']['coordinates'][0]) - 1 == referencia['properties']['vertices']
    # Ajustar a referência é um recorte pessoal, sem preservar rótulo documental oficial.
    manual = validar_area(referencia)
    assert manual['geometry'] == referencia['geometry']
    assert manual['properties']['origem'] == 'desenho_manual'
    assert 'figura' not in manual['properties']
    aii = next(f for f in dados['features'] if f['properties']['id'] == 'aii_agua_solos')
    assert shape(aii['geometry']).covers(shape(referencia['geometry']).centroid)
    mina = cliente.get('/api/mapa').json()['minas'][0]
    assert shape(referencia['geometry']).contains(Point(mina['longitude'], mina['latitude']))


def test_pacote_invalido_retorna_falha_sem_inventar_contorno(tmp_path):
    (tmp_path / 'dados/referencias').mkdir(parents=True)
    (tmp_path / 'dados/minas.json').write_text('[{"id":"horizontes"}]')
    cliente = TestClient(criar_app(raiz=tmp_path))
    assert cliente.get('/api/minas/horizontes/referencias').status_code == 503
    original = ler_referencias(RAIZ / 'dados/referencias/horizontes.geojson')
    quebrado = copy.deepcopy(original)
    quebrado['features'].pop()
    arquivo = tmp_path / 'dados/referencias/horizontes.geojson'
    arquivo.write_text(json.dumps(quebrado))
    assert cliente.get('/api/minas/horizontes/referencias').status_code == 503
    arquivo.write_text(json.dumps(original))
    assert cliente.get('/api/minas/horizontes/referencias').status_code == 200
