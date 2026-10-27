"""Regressões de medidas, separação de comentários e prévia independente do navegador."""
from io import BytesIO
import json
from PIL import Image
from pypdf import PdfReader
import pytest
from fastapi.testclient import TestClient
from geovale.api.main import criar_app
from geovale.comentarios import Comentarista
from geovale.fichas import medidas, projetar
from geovale.territorio import DadosTerritoriais
from test_territorio import preparar_raiz, coleta_simulada


def test_medidas_usam_metros_e_dissolvem_area_sobreposta():
    pol={'type':'Polygon','coordinates':[[[-43.94,-20.1],[-43.93,-20.1],[-43.93,-20.09],[-43.94,-20.09],[-43.94,-20.1]]]}
    fs=[{'geometry':pol},{'geometry':pol}]
    m=medidas(fs)
    assert m['ha']==pytest.approx(projetar(pol).area/10000)
    assert 100<m['ha']<130 and m['km']==0
    linha={'type':'LineString','coordinates':[[-43.94,-20.1],[-43.93,-20.1]]}
    assert .9<medidas([{'geometry':linha}])['km']<1.1


def test_comentarios_das_fichas_sao_regras_mesmo_com_chave_e_nao_alteram_fatos():
    fatos=[{'dados':[{'id':'a','nome':'Rios','valor':'2','origem':'Cadastro','comentario':'São registros, não rios distintos.'}]}]
    antes=json.dumps(fatos)
    c=Comentarista(ambiente={'OPENAI_API_KEY':'credencial-ficticia'},abrir=lambda *a,**k:pytest.fail('Fichas não chamam IA'))
    saida=c.gerar(fatos)
    assert saida['metodo']=='regras' and saida['comentarios']=={'a':'São registros, não rios distintos.'}
    assert json.dumps(fatos)==antes
    sem_chave=Comentarista(ambiente={},abrir=lambda *a,**k:pytest.fail('Não há IA configurada')).explicar({'setores':[]},{'S1':'Regra.'})
    assert sem_chave['metodo']=='regras' and 'não configurada' in sem_chave['rotulo'] and sem_chave['textos']=={'S1':'Regra.'}


def test_ia_explica_sugestao_so_com_setores_completos_e_numeros_fornecidos():
    entrada={'setores':[{'id':'S1','ranking':[{'uso':'Conservação','nota':'78'}],'pesos_pct':{'relevo':'34'}}]}
    def abrir(texto,setor='S1'):
        def resposta(req,timeout):
            payload=json.loads(req.data)
            assert payload['model']=='gpt-5-nano' and req.full_url=='https://api.openai.com/v1/responses'
            assert payload['store'] is False and payload['text']['format']['strict'] is True and 'temperature' not in payload
            assert payload['text']['format']['schema']['properties']['explicacoes']['items']['properties']['setor']['enum']==['S1']
            return BytesIO(json.dumps({'status':'completed','output':[{'type':'reasoning'},{'type':'message','content':[{'type':'output_text','text':json.dumps({'explicacoes':[{'setor':setor,'texto':texto}]})}]}]}).encode())
        return resposta
    env={'OPENAI_API_KEY':'credencial-ficticia-do-teste'}
    padrao={'S1':'Conservação lidera pela regra.'}
    assert Comentarista(env,abrir('No S1, conservação lidera com 78 porque o relevo pesa 34%.')).explicar(entrada,padrao)['metodo']=='ia'
    assert Comentarista(env,abrir('No S1, conservação lidera com 91 e custa pouco.')).explicar(entrada,padrao)['textos']==padrao
    assert Comentarista(env,abrir('No S2, conservação lidera com 78 pelo relevo.',setor='S2')).explicar(entrada,padrao)['metodo']=='regras'


def test_previa_renderiza_png_da_mesma_versao_e_preserva_documento_aberto(tmp_path):
    raiz=preparar_raiz(tmp_path);fonte=DadosTerritoriais(raiz,coletar=coleta_simulada);fonte.atualizar()
    cliente=TestClient(criar_app(raiz=raiz,territorios=fonte))
    pdf=cliente.get('/api/minas/horizontes/relatorio');assert pdf.status_code==200
    versao=pdf.headers['X-Relatorio-Versao'];query='?versao='+versao
    manifesto=cliente.get('/api/minas/horizontes/relatorio/previa'+query)
    paginas=len(PdfReader(BytesIO(pdf.content)).pages)
    assert manifesto.status_code==200 and len(manifesto.json()['paginas'])==paginas>=9
    for numero in [1,4,paginas]:
        img=cliente.get('/api/minas/horizontes/relatorio/paginas/'+str(numero)+query)
        assert img.status_code==200 and img.headers['content-type']=='image/png'
        with Image.open(BytesIO(img.content)) as im:
            assert im.width>900 and im.height>1300
    assert cliente.get('/api/minas/horizontes/relatorio/paginas/0'+query).status_code==404
    assert cliente.get('/api/minas/horizontes/relatorio/previa?versao=inexistente').status_code==409
    assert cliente.get('/api/minas/outra/relatorio/previa'+query).status_code==404

    caminho=raiz/'dados/cenarios/horizontes.json'
    cenario=json.loads(caminho.read_text());cenario['dados'][0]['valor']=1.7;caminho.write_text(json.dumps(cenario))
    novo=cliente.get('/api/minas/horizontes/relatorio');assert novo.headers['X-Relatorio-Versao']!=versao
    assert cliente.get('/api/minas/horizontes/relatorio/paginas/1'+query).status_code==200


def test_chave_local_e_lida_sem_reinicio_e_nao_entra_na_assinatura(tmp_path):
    pasta=tmp_path/'.local';pasta.mkdir();arquivo=pasta/'ia.env';arquivo.write_text('OPENAI_API_KEY=\n')
    c=Comentarista(raiz=tmp_path);antes=c.assinatura
    assert not c.chave
    arquivo.write_text('OPENAI_API_KEY=credencial-ficticia\n')
    assert c.chave=='credencial-ficticia' and c.assinatura!=antes
    assert 'credencial-ficticia' not in json.dumps(c.assinatura)
