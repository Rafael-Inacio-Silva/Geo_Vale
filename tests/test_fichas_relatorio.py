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


def resposta_api(nome,itens):
    """Imita o Responses devolvendo `itens` como saída estruturada."""
    return BytesIO(json.dumps({'status':'completed','output':[{'type':'reasoning'},{'type':'message','content':[{'type':'output_text','text':json.dumps({nome:itens})}]}]}).encode())


def test_sem_chave_leitura_e_explicacao_ficam_por_regras_sem_alterar_fatos():
    fatos=[{'id':'agua','nome':'Água','dados':[{'id':'a','nome':'Rios','valor':'2','origem':'Cadastro','comentario':'São registros, não rios distintos.'}]}]
    antes=json.dumps(fatos)
    c=Comentarista(ambiente={},abrir=lambda *a,**k:pytest.fail('Não há IA configurada'))
    saida=c.gerar(fatos)
    assert saida['metodo']=='regras' and saida['ia']==[] and saida['comentarios']=={'a':'São registros, não rios distintos.'}
    assert json.dumps(fatos)==antes
    assert c.explicar({'setores':[]},{'S1':'Regra.'})=={'metodo':'regras','textos':{'S1':'Regra.'}}


def test_ia_le_cada_ficha_com_guia_e_so_numeros_fornecidos():
    fatos=[{'id':'relevo','nome':'Relevo','dados':[{'id':'d','nome':'Declividade','valor':'Forte ondulado (20% - 45%): 66,9%','origem':'Topodata','comentario':'76,2% acima de 20%.'}]},
           {'id':'agua','nome':'Água','dados':[{'id':'q','nome':'Q7,10','valor':'1,311 m³/s','origem':'Igam','comentario':'Referência de outorga.'}]}]
    textos={'d':'O entorno tem 76,2% acima de 20% de declividade: favorece conservação e limita solar.','q':'A Q7,10 de 1,311 m³/s indica o volume de 9 piscinas.'}
    def abrir(req,timeout):
        payload=json.loads(req.data)
        assert payload['model']=='gpt-4.1-mini' and payload['store'] is False and payload['text']['format']['strict'] is True
        entrada=json.loads(payload['input']);dado=entrada['dados'][0]['id']
        assert entrada['guia'] in payload['instructions'] and ('Topodata' in entrada['guia'] if dado=='d' else 'Igam 48/2019' in entrada['guia'])
        return resposta_api('leituras',[{'dado':dado,'texto':textos[dado]}])
    saida=Comentarista({'OPENAI_API_KEY':'credencial-ficticia'},abrir).gerar(fatos)
    assert saida['ia']==['relevo'] and saida['comentarios']=={'d':textos['d'],'q':'Referência de outorga.'}
    for ruim in ['O entorno tem 76,2% acima de 20%? (fique objetivo) favorece conservação.','O entorno tem 76,2% acima de 20%: esses प्रकार favorecem conservação.','O entorno tem 76,2% acima de 20%; estavel: true.','O entorno tem 76,2% acima de 20%; alto_pct.']:
        textos['d']=ruim
        assert Comentarista({'OPENAI_API_KEY':'credencial-ficticia'},abrir).gerar(fatos)['ia']==[]


def test_ia_explica_sugestao_so_com_setores_completos_e_numeros_fornecidos():
    entrada={'setores':[{'id':'S1','ranking':[{'uso':'Conservação','nota':'78'}],'pesos_pct':{'relevo':'34'}}]}
    def abrir(texto,setor='S1'):
        def resposta(req,timeout):
            payload=json.loads(req.data)
            assert payload['model']=='gpt-4.1-mini' and req.full_url=='https://api.openai.com/v1/responses'
            assert payload['store'] is False and payload['text']['format']['strict'] is True and payload['temperature']==.2 and 'reasoning' not in payload
            assert payload['text']['format']['schema']['properties']['explicacoes']['items']['properties']['setor']['enum']==['S1']
            return resposta_api('explicacoes',[{'setor':setor,'texto':texto}])
        return resposta
    env={'OPENAI_API_KEY':'credencial-ficticia-do-teste'}
    padrao={'S1':'Conservação lidera pela regra.'}
    assert Comentarista(env,abrir('No S1, conservação lidera com 78 porque o relevo pesa 34%.')).explicar(entrada,padrao)['metodo']=='ia'
    assert Comentarista(env,abrir('No S1, conservação lidera com 91 e custa pouco.')).explicar(entrada,padrao)['textos']==padrao
    assert Comentarista(env,abrir('No S2, conservação lidera com 78 pelo relevo.',setor='S2')).explicar(entrada,padrao)['metodo']=='regras'
    assert Comentarista(env,abrir('No S1, conservação lidera com 78, vantagem de 34 pontos.')).explicar(entrada,padrao)['metodo']=='regras'


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


def test_explicacao_da_tela_usa_a_mesma_ia_e_reaproveita_a_resposta():
    chamadas=[]
    def abrir(req,timeout):
        chamadas.append(1)
        return resposta_api('explicacoes',[{'setor':'S1','texto':'Conservação e restauração: encosta forte favorece deixar a mata voltar.'}])
    c=Comentarista({'OPENAI_API_KEY':'credencial-ficticia'},abrir)
    entrada={'setores':[{'id':'S1','uso sugerido':'Conservação e restauração','a favor':['60% do setor tem declividade acima de 20%']}]}
    primeira=c.explicar(entrada,{'S1':'Regra.'},{'S1':'Os demais ficam atrás: solar.'})
    assert primeira=={'metodo':'ia','principal':{'S1':'Conservação e restauração: encosta forte favorece deixar a mata voltar.'},
                      'textos':{'S1':'Conservação e restauração: encosta forte favorece deixar a mata voltar. Os demais ficam atrás: solar.'}}
    assert c.explicar(entrada,{'S1':'Regra.'},{'S1':'Os demais ficam atrás: solar.'})==primeira and len(chamadas)==1


def test_rota_de_explicacao_sem_chave_devolve_regras(tmp_path):
    raiz=preparar_raiz(tmp_path);fonte=DadosTerritoriais(raiz,coletar=coleta_simulada)
    cliente=TestClient(criar_app(raiz=raiz,territorios=fonte))
    assert cliente.get('/api/minas/outra/sugestao/explicacao').status_code==404
    assert cliente.get('/api/minas/horizontes/sugestao/explicacao?pesos=1').status_code==422


def test_video_pos_mineracao_vem_do_arquivo_da_mina_com_suporte_a_trecho(tmp_path):
    raiz=preparar_raiz(tmp_path);fonte=DadosTerritoriais(raiz,coletar=coleta_simulada)
    cliente=TestClient(criar_app(raiz=raiz,territorios=fonte))
    assert cliente.get('/api/minas/horizontes/video').status_code==404
    (raiz/'dados/videos').mkdir(parents=True);(raiz/'dados/videos/horizontes.mp4').write_bytes(b'0123456789')
    inteiro=cliente.get('/api/minas/horizontes/video')
    assert inteiro.status_code==200 and inteiro.headers['content-type']=='video/mp4' and inteiro.content==b'0123456789'
    trecho=cliente.get('/api/minas/horizontes/video',headers={'Range':'bytes=2-5'})
    assert trecho.status_code==206 and trecho.content==b'2345'
    assert cliente.get('/api/minas/outra/video').status_code==404
