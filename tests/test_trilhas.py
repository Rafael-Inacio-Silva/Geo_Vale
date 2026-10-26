"""Verifica a segunda fonte temática com consultas limitadas e dados públicos simulados."""
import copy
import pytest
from fastapi.testclient import TestClient
from geovale.api.main import criar_app
from geovale.mapa import FonteIndisponivel
from geovale.trilhas import TrilhasMunicipais, preparar_extensao, preparar_trilhas, preparar_simbologia, aplicar_simbologia


def trilha_valida():
    return {'type':'FeatureCollection','features':[{'type':'Feature','geometry':{'type':'LineString','coordinates':[[-43.93,-20.13],[-43.91,-20.11]]},'properties':{'OBJECTID':1,'Name':'Acesso de teste','PopupInfo':'<script>fonte</script>'}}]}


def simbologia_valida():
    return {'layers': [{'id': 0, 'layerDefinition': {'drawingInfo': {'renderer': {
        'type': 'uniqueValue', 'field1': 'Name', 'uniqueValueInfos': [
            {'value': 'Acesso de teste', 'label': 'Acesso de teste', 'symbol': {'type': 'esriSLS', 'style': 'esriSLSSolid', 'width': 1.5, 'color': [190, 185, 219, 255]}},
            {'value': 'Outra trilha', 'label': 'Nome publicado de outra trilha', 'symbol': {'type': 'esriSLS', 'style': 'esriSLSSolid', 'width': 1.5, 'color': [255, 238, 101, 255]}},
        ],
    }}}}]}


def test_extensao_e_cache_limitam_consultas_e_nao_retornam_campos_desnecessarios():
    chamadas = []
    tempo = [0]
    def consultar(bbox):
        chamadas.append(bbox)
        return trilha_valida()
    fonte = TrilhasMunicipais(consultar, lambda: tempo[0], consultar_simbolos=simbologia_valida)
    primeira = fonte.obter('-44.1,-20.3,-43.7,-19.9')
    assert chamadas == [preparar_extensao('-44.1,-20.3,-43.7,-19.9')]
    assert primeira['features'][0]['properties'] == {'id':1,'nome':'Acesso de teste','cor':'#beb9db','opacidade':1,'largura':2}
    primeira['features'].clear()
    assert len(fonte.obter('-44.1,-20.3,-43.7,-19.9')['features']) == 1
    assert len(chamadas) == 1
    tempo[0] = 601
    fonte.obter('-44.1,-20.3,-43.7,-19.9')
    assert len(chamadas) == 2
    assert fonte.obter('0,0,1,1')['fora_cobertura'] is True
    assert len(chamadas) == 2


@pytest.mark.parametrize('bbox',['nan,0,1,1','-44,-20,-45,-19','-181,-20,-43,-19','a,b,c,d','0,0,1','0,0,0,1'])
def test_extensoes_invalidas_nao_consultam_fonte(bbox):
    with pytest.raises(ValueError):TrilhasMunicipais(consultar=lambda _: pytest.fail('Consulta indevida')).obter(bbox)


@pytest.mark.parametrize('caso',['erro','ponto','fora','parcial'])
def test_fonte_incompativel_nao_e_apresentada_como_trilhas(caso):
    dados = copy.deepcopy(trilha_valida())
    if caso == 'erro':dados = {'error':{'message':'token interno'}}
    elif caso == 'ponto':dados['features'][0]['geometry'] = {'type':'Point','coordinates':[-43.9,-20.1]}
    elif caso == 'fora':dados['features'][0]['geometry']['coordinates'] = [[0,0],[1,1]]
    else:dados['exceededTransferLimit'] = True
    with pytest.raises(FonteIndisponivel):preparar_trilhas(dados)


def test_api_informa_falha_sem_vazar_detalhes_e_permite_recuperar():
    falhar = [True]
    def consultar(_):
        if falhar[0]:raise OSError('detalhe privado')
        return trilha_valida()
    cliente = TestClient(criar_app(trilhas=TrilhasMunicipais(consultar, consultar_simbolos=simbologia_valida)))
    erro = cliente.get('/api/mapa/trilhas?bbox=-43.94,-20.14,-43.90,-20.10')
    assert erro.status_code == 503 and 'privado' not in erro.text
    assert cliente.get('/api/mapa').status_code == 200
    falhar[0] = False
    assert len(cliente.get('/api/mapa/trilhas?bbox=-43.94,-20.14,-43.90,-20.10').json()['features']) == 1
    assert cliente.get('/api/mapa/trilhas?bbox=errado').status_code == 422
    assert cliente.get('/api/mapa/trilhas?bbox=0,0,1,1').json()['fora_cobertura'] is True


def test_simbolos_oficiais_preservam_cores_e_rotulos_e_legenda_so_do_recorte():
    dados = trilha_valida()
    dados['features'][0]['properties']['Name'] = 'ACESSO DE TESTE'
    fonte = TrilhasMunicipais(consultar=lambda _: dados, consultar_simbolos=simbologia_valida)
    resposta = TestClient(criar_app(trilhas=fonte)).get('/api/mapa/trilhas?bbox=-43.94,-20.14,-43.90,-20.10')
    assert resposta.status_code == 200
    documento = resposta.json()
    assert documento['features'][0]['properties']['nome'] == 'ACESSO DE TESTE'
    assert documento['features'][0]['properties']['cor'] == '#beb9db'
    assert documento['legenda'] == [{'id':'Acesso de teste','nome':'Acesso de teste','cor':'#beb9db','opacidade':1,'largura':2}]
    assert fonte.obter('0,0,1,1')['legenda'] == []


def test_cache_reaproveita_simbologia_entre_enquadramentos_e_renova_apos_prazo():
    tempo = [0]
    consultas = []
    def consultar_simbolos():
        consultas.append(tempo[0])
        return simbologia_valida()
    fonte = TrilhasMunicipais(lambda _: trilha_valida(), lambda: tempo[0], consultar_simbolos)
    primeira = fonte.obter('-43.94,-20.14,-43.90,-20.10')
    primeira['legenda'][0]['cor'] = '#000000'
    assert fonte.obter('-43.94,-20.14,-43.90,-20.10')['legenda'][0]['cor'] == '#beb9db'
    fonte.obter('-43.95,-20.15,-43.90,-20.10')
    assert consultas == [0]
    tempo[0] = 601
    fonte.obter('-43.95,-20.15,-43.90,-20.10')
    assert consultas == [0,601]


@pytest.mark.parametrize('caso', ['campo','tipo','sem_categoria','cor','alpha','largura','duplicada','estilo'])
def test_simbologia_invalida_nao_inventa_cores(caso):
    documento = simbologia_valida()
    renderer = documento['layers'][0]['layerDefinition']['drawingInfo']['renderer']
    primeira = renderer['uniqueValueInfos'][0]
    if caso == 'campo':renderer['field1'] = 'OutroCampo'
    elif caso == 'tipo':renderer['type'] = 'simple'
    elif caso == 'sem_categoria':renderer['uniqueValueInfos'] = []
    elif caso == 'cor':primeira['symbol']['color'][0] = 256
    elif caso == 'alpha':primeira['symbol']['color'][3] = True
    elif caso == 'largura':primeira['symbol']['width'] = float('nan')
    elif caso == 'duplicada':renderer['uniqueValueInfos'].append(copy.deepcopy(primeira))
    elif caso == 'estilo':primeira['symbol']['style'] = 'script'
    with pytest.raises(FonteIndisponivel):preparar_simbologia(documento)


def test_categoria_ausente_na_configuracao_nao_recebe_cor_de_outra_trilha():
    dados = preparar_trilhas(trilha_valida())
    dados['features'][0]['properties']['nome'] = 'Sem configuração oficial'
    with pytest.raises(FonteIndisponivel):aplicar_simbologia(dados, preparar_simbologia(simbologia_valida()))


def test_falha_na_simbologia_e_recuperacao_nao_afetam_outros_contratos():
    falhar = [True]
    def consultar_simbolos():
        if falhar[0]:raise OSError('mensagem interna')
        return simbologia_valida()
    cliente = TestClient(criar_app(trilhas=TrilhasMunicipais(lambda _: trilha_valida(), consultar_simbolos=consultar_simbolos)))
    erro = cliente.get('/api/mapa/trilhas?bbox=-43.94,-20.14,-43.90,-20.10')
    assert erro.status_code == 503 and 'interna' not in erro.text
    assert cliente.get('/api/mapa').status_code == 200
    falhar[0] = False
    assert cliente.get('/api/mapa/trilhas?bbox=-43.94,-20.14,-43.90,-20.10').json()['legenda'][0]['cor'] == '#beb9db'
