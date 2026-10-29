"""Identidade municipal, seleção restrita e independência de falhas do IBGE."""
import copy
from concurrent.futures import ThreadPoolExecutor
import pytest
from fastapi.testclient import TestClient
from geovale.api.main import criar_app
from geovale.mapa import FonteIndisponivel
from geovale.municipio import LimitesMunicipais, preparar_municipio


def documento():
    return {'type': 'FeatureCollection', 'features': [{'type': 'Feature', 'properties': {'codarea': '3144805'}, 'geometry': {'type': 'Polygon', 'coordinates': [[[-44,-20.2],[-43.8,-20.2],[-43.8,-19.9],[-44,-20.2]]]}}]}


def test_consulta_apenas_municipio_da_mina_sem_aceitar_codigo_externo():
    chamadas=[]
    def consultar(codigo):
        chamadas.append(codigo)
        return documento()
    cliente=TestClient(criar_app(municipios=LimitesMunicipais(consultar)))
    assert cliente.get('/api/mapa').json()['minas'][0]['codigo_municipio_ibge']=='3144805'
    assert chamadas==[]
    assert cliente.get('/api/minas/outra/limite-municipal').status_code==404
    assert chamadas==[]
    resposta=cliente.get('/api/minas/horizontes/limite-municipal?codigo=3550308')
    assert resposta.status_code==200 and chamadas==['3144805']
    dados=resposta.json()
    assert dados['features'][0]['geometry']==documento()['features'][0]['geometry']
    assert dados['fonte']['qualidade']=='maxima' and dados['fonte']['ano_referencia'] is None
    assert resposta.headers['cache-control']=='no-store'


@pytest.mark.parametrize('caso',['identidade','vazio','duplicado','ponto','cruzado','fora_mg','crs'])
def test_recusa_limites_incompativeis(caso):
    dados=documento();f=dados['features'][0]
    if caso=='identidade': f['properties']['codarea']='3550308'
    elif caso=='vazio': dados['features']=[]
    elif caso=='duplicado': dados['features'].append(copy.deepcopy(f))
    elif caso=='ponto': f['geometry']={'type':'Point','coordinates':[-43.9,-20]}
    elif caso=='cruzado': f['geometry']['coordinates']=[[[-44,-20.2],[-43.8,-19.9],[-44,-19.9],[-43.8,-20.2],[-44,-20.2]]]
    elif caso=='fora_mg': f['geometry']['coordinates']=[[[0,0],[1,0],[1,1],[0,0]]]
    elif caso=='crs': dados['crs']={'properties':{'name':'EPSG:31983'}}
    with pytest.raises(FonteIndisponivel): preparar_municipio(dados,'3144805')


def test_cache_concorrente_defensivo_e_expiracao():
    chamadas=[];tempo=[0]
    def consultar(_): chamadas.append(1);return documento()
    fonte=LimitesMunicipais(consultar,lambda:tempo[0])
    with ThreadPoolExecutor(4) as pool: resultados=list(pool.map(lambda _:fonte.obter('3144805'),range(4)))
    assert len(chamadas)==1
    resultados[0]['features'].clear()
    assert len(fonte.obter('3144805')['features'])==1
    tempo[0]=3601;fonte.obter('3144805')
    assert len(chamadas)==2


def test_falha_nao_expoe_detalhes_e_permite_recuperar_sem_interromper_mapa():
    falha=[True]
    def consultar(_):
        if falha[0]:raise OSError('segredo interno')
        return documento()
    cliente=TestClient(criar_app(municipios=LimitesMunicipais(consultar)))
    resposta=cliente.get('/api/minas/horizontes/limite-municipal')
    assert resposta.status_code==503 and 'segredo' not in resposta.text
    assert cliente.get('/api/mapa').status_code==200
    falha[0]=False
    assert cliente.get('/api/minas/horizontes/limite-municipal').status_code==200


def test_dados_fixos_leem_malha_salva_sem_consultar_o_ibge(monkeypatch):
    monkeypatch.setenv('GEOVALE_DADOS_FIXOS', '1')
    monkeypatch.setattr('geovale.municipio.urlopen', lambda *a, **k: pytest.fail('consultou o IBGE'))
    resposta = TestClient(criar_app()).get('/api/minas/horizontes/limite-municipal')
    assert resposta.status_code == 200
    dados = resposta.json()
    assert dados['features'][0]['properties']['codigo_ibge'] == '3144805'
    assert dados['fonte']['consultado_em'].startswith('2026-10-29')
