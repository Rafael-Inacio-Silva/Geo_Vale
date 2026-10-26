"""Confere limites e integridade do desenho manual antes da confirmação."""
import copy
import math
import pytest
from fastapi.testclient import TestClient
from geovale.api.main import criar_app
from geovale.area import AreaInvalida, validar_area


def area_valida():
    return {'type': 'Feature', 'geometry': {'type': 'Polygon', 'coordinates': [[[-43.93,-20.13],[-43.91,-20.13],[-43.91,-20.11],[-43.93,-20.13]]]}, 'properties': {'origem': 'oficial'}}


def test_confirmacao_preserva_coordenadas_e_identifica_origem_manual():
    documento = area_valida()
    resposta = TestClient(criar_app()).post('/api/area/validar', json=documento)
    assert resposta.status_code == 200
    dados = resposta.json()
    assert dados['geometry'] == documento['geometry']
    assert dados['properties'] == {'origem': 'desenho_manual', 'finalidade': 'area_de_estudo', 'vertices': 3}
    assert TestClient(criar_app()).get('/api/area').status_code == 404


@pytest.mark.parametrize('caso', ['linha','aberto','poucos','cruzado','colinear','buraco','infinito','nan','booleano','longitude','latitude','inteiro_excessivo','forma_invalida'])
def test_contorno_invalido_nao_e_corrigido_silenciosamente(caso):
    documento = copy.deepcopy(area_valida())
    anel = documento['geometry']['coordinates'][0]
    if caso == 'linha':documento['geometry']['type'] = 'LineString'
    elif caso == 'aberto':anel.pop()
    elif caso == 'poucos':documento['geometry']['coordinates'] = [[[-43.9,-20.1],[-43.8,-20.1],[-43.9,-20.1]]]
    elif caso == 'cruzado':documento['geometry']['coordinates'] = [[[-43.93,-20.13],[-43.91,-20.11],[-43.93,-20.11],[-43.91,-20.13],[-43.93,-20.13]]]
    elif caso == 'colinear':documento['geometry']['coordinates'] = [[[-43.9,-20],[-43.8,-20],[-43.7,-20],[-43.9,-20]]]
    elif caso == 'buraco':documento['geometry']['coordinates'].append(anel[:])
    elif caso == 'infinito':anel[1][0] = float('inf')
    elif caso == 'nan':anel[1][0] = float('nan')
    elif caso == 'booleano':anel[1][0] = True
    elif caso == 'inteiro_excessivo':anel[1][0] = 10**1000
    elif caso == 'longitude':anel[1][0] = 181
    elif caso == 'latitude':anel[1][1] = 90
    else:documento = {'type':'Feature','geometry':None}
    with pytest.raises(AreaInvalida):validar_area(documento)


def test_limite_de_vertices_e_carga_http():
    documento = area_valida()
    anel = [[-43.9 + .01*math.cos(i*2*math.pi/500), -20.1 + .01*math.sin(i*2*math.pi/500)] for i in range(500)]
    documento['geometry']['coordinates'] = [anel + [anel[0]]]
    assert validar_area(documento)['properties']['vertices'] == 500
    documento['geometry']['coordinates'][0].insert(1,[-43.889,-20.099])
    with pytest.raises(AreaInvalida):validar_area(documento)
    cliente = TestClient(criar_app())
    assert cliente.post('/api/area/validar', content=b'x'*131073).status_code == 413
    assert cliente.post('/api/area/validar', content=b'{').status_code == 422
    assert cliente.post('/api/area/validar', json={'type':'Feature','geometry':{'type':'Point','coordinates':[0,0]}}).status_code == 422
