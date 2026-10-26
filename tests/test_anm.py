"""Verifica procedência, isolamento e consistência do cadastro consultada na ANM."""
from concurrent.futures import ThreadPoolExecutor
import copy
import pytest
from fastapi.testclient import TestClient
from geovale.api.main import criar_app
from geovale.anm import ProcessosANM, preparar_processo
from geovale.mapa import FonteIndisponivel


def documento_anm():
    return {'features': [{'attributes': {'NUMERO':3964, 'ANO':1950, 'NOME':'VALE S.A.', 'FASE':'CONCESSÃO DE LAVRA', 'AREA_HA':471.39, 'SUBS':'FERRO', 'UF':'MG', 'HTML':'<script>interno</script>'}}]}


def test_cartao_recebe_apenas_atributos_sem_geometria():
    original = documento_anm()
    cliente = TestClient(criar_app(anm=ProcessosANM(consultar=lambda *_: original)))
    resposta = cliente.get('/api/minas/horizontes/processo-anm')
    assert resposta.status_code == 200
    dados = resposta.json()
    assert set(dados) == {'properties', 'fonte'}
    assert dados['properties'] == {'titular':'VALE S.A.','fase':'CONCESSÃO DE LAVRA','substancia':'FERRO','processo':'003.964/1950','numero':3964,'ano':1950,'area_ha':471.39,'uf':'MG'}
    assert dados['fonte']['url'].startswith('https://geo.anm.gov.br/')
    assert 'consultado_em' in dados['fonte']
    assert resposta.headers['cache-control'] == 'no-store'
    assert 'HTML' not in dados['properties']


def test_so_consulta_processo_associado_ao_catalogo_e_404_nao_acessa_a_fonte():
    chamadas=[]
    def consultar(numero, ano):
        chamadas.append((numero,ano))
        return documento_anm()
    cliente=TestClient(criar_app(anm=ProcessosANM(consultar)))
    assert cliente.get('/api/minas/desconhecida/processo-anm').status_code == 404
    assert chamadas == []
    assert cliente.get('/api/minas/horizontes/processo-anm?numero=9&ano=2020').status_code == 200
    assert chamadas == [(3964,1950)]


def test_cache_concorrencia_expiracao_e_copia_defensiva():
    tempo=[0];chamadas=[]
    def consultar(*_):
        chamadas.append(1)
        return documento_anm()
    fonte=ProcessosANM(consultar,lambda:tempo[0])
    with ThreadPoolExecutor(4) as pool:
        resultados=list(pool.map(lambda _:fonte.obter(3964,1950),range(4)))
    assert len(chamadas)==1
    resultados[0]['properties']['titular']='Alterado no cliente'
    assert fonte.obter(3964,1950)['properties']['titular']=='VALE S.A.'
    tempo[0]=601
    fonte.obter(3964,1950)
    assert len(chamadas)==2


@pytest.mark.parametrize('caso',['numero','ano','booleano','uf','titular','fase','area','duplicado','vazio','parcial'])
def test_respostas_incompativeis_nao_viram_dados_da_mina(caso):
    dados=copy.deepcopy(documento_anm());p=dados['features'][0]['attributes']
    if caso=='numero':p['NUMERO']=9
    elif caso=='ano':p['ANO']=2020
    elif caso=='booleano':p['NUMERO']=True
    elif caso=='uf':p['UF']='SP'
    elif caso=='titular':p['NOME']=None
    elif caso=='fase':p['FASE']=''
    elif caso=='area':p['AREA_HA']=float('inf')
    elif caso=='duplicado':dados['features'].append(copy.deepcopy(dados['features'][0]))
    elif caso=='vazio':dados['features']=[]
    elif caso=='parcial':dados['exceededTransferLimit']=True
    with pytest.raises(FonteIndisponivel):preparar_processo(dados,3964,1950)


def test_falha_e_recuperacao_nao_expoem_detalhes_nem_interrompem_o_mapa():
    falhar=[True]
    def consultar(*_):
        if falhar[0]:raise OSError('token e detalhe interno')
        return documento_anm()
    cliente=TestClient(criar_app(anm=ProcessosANM(consultar)))
    erro=cliente.get('/api/minas/horizontes/processo-anm')
    assert erro.status_code==503 and 'token' not in erro.text
    assert cliente.get('/api/mapa').status_code==200
    assert cliente.get('/api/saude').status_code==200
    falhar[0]=False
    assert cliente.get('/api/minas/horizontes/processo-anm').status_code==200

def test_consulta_externa_solicita_somente_atributos(monkeypatch):
    import io
    import json
    from urllib.parse import parse_qs, urlsplit
    import geovale.anm as modulo
    chamadas = []
    def abrir(url, timeout):
        chamadas.append((parse_qs(urlsplit(url).query), timeout))
        return io.BytesIO(json.dumps(documento_anm()).encode())
    monkeypatch.setattr(modulo, 'urlopen', abrir)
    modulo.consultar_processo(3964, 1950)
    parametros, timeout = chamadas[0]
    assert parametros['returnGeometry'] == ['false']
    assert parametros['f'] == ['json']
    assert parametros['where'] == ['NUMERO = 3964 AND ANO = 1950']
    assert 'outSR' not in parametros and timeout == 15
