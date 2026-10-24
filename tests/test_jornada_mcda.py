"""Fluxo completo dos mapas reais, isolamento de sessão, revisões e relatórios sem ML."""
from copy import deepcopy
from pathlib import Path
import json,sqlite3
import pytest
from fastapi.testclient import TestClient
from geovale.mvp.api import criar_app
from geovale.decisao.territorio import DADOS,resumo_entrada,analisar_territorio,carregar_caso
from geovale.decisao.metodos import ErroDecisao

CAB={'X-GeoVale':'1'}


@pytest.fixture
def app(tmp_path):
    """Cada teste recebe banco independente sem tocar no histórico da demonstração."""
    return criar_app(tmp_path/'teste.sqlite3')


def enviar(cliente,codigo='il_006'):
    """Percorre upload real sem acionar processamento de relevo antes do botão."""
    return cliente.post('/api/areas',headers=CAB,files={'arquivo':('mapa.geojson',(DADOS/codigo/'area.geojson').read_bytes(),'application/geo+json')})


def acao(cliente,e,nome,**campos):
    """Usa a versão recebida, permitindo verificar conflitos e alterações posteriores."""
    return cliente.post(f'/api/areas/{e["id"]}/{nome}',headers=CAB,json={'versao':e['versao'],**campos})


def completo(cliente,codigo='il_006'):
    """Constrói uma comparação aceita com o mesmo caminho da interface."""
    e=enviar(cliente,codigo).json();e=acao(cliente,e,'analisar').json()
    r=acao(cliente,e,'comparar',pesos=e['pesos'],origem='ahp');assert r.status_code==200,r.text
    return r.json()


@pytest.mark.parametrize('codigo,nome,area',[('il_006','Rapatee',162.29),('il_071','Burning Star 3',530.55)])
def test_mapa_real_completo_e_relatorios_mesma_revisao(app,codigo,nome,area):
    """Dois casos reais produzem índices reproduzíveis e dois relatórios do mesmo resultado salvo."""
    with TestClient(app) as c:
        r=enviar(c,codigo);assert r.status_code==201
        e=r.json();assert e['nome']==nome and e['area_ha']==pytest.approx(area,abs=.01)
        assert not e['analisada'] and e['resultado'] is None and 'matriz' not in e
        a=acao(c,e,'analisar');assert a.status_code==200,a.text;e=a.json()
        assert e['analisada'] and e['resumo']['ano_cobertura']==2024 and len(e['resumo']['pendencias'])==5
        r=acao(c,e,'comparar',pesos=e['pesos'],origem='ahp');assert r.status_code==200;e=r.json()
        assert len(e['resultado']['ranking'])==3 and all(0<=r['indice']<=1 for r in e['resultado']['ranking'])
        assert 'calculo' not in e['resultado'] and 'fontes' not in e and 'ml' not in e
        salvo=acao(c,e,'salvar');assert salvo.status_code==200;e=salvo.json();assert e['salvo_revisao']==1
        htmls=[]
        for tipo in ('simples','tecnico'):
            r=c.get(f'/api/areas/{e["id"]}/revisoes/1/{tipo}');assert r.status_code==200
            assert 'data:image/png;base64,' in r.text and 'Revisão 1' in r.text and nome in r.text
            assert 'Não avalia custos' in r.text and 'não autoriza uso' in r.text
            htmls.append(r.text)
        assert 'Cálculo TOPSIS completo' not in htmls[0] and 'Cálculo TOPSIS completo' in htmls[1]
        assert 'razao_consistencia' in htmls[1]
        assert acao(c,e,'salvar').json()['salvo_revisao']==1


def test_ahp_inconsistente_nao_altera_estado_e_pesos_manual_invalida_resultado(app):
    """Não aceita prioridades cíclicas, totais incorretos ou versão antiga; nova avaliação vira revisão nova."""
    with TestClient(app) as c:
        e=completo(c);e=acao(c,e,'salvar').json();ident=e['id']
        ruim=acao(c,e,'prioridades',comparacoes=[9,1/9,9]);assert ruim.status_code==422
        assert c.get(f'/api/areas/{ident}').json()==e
        assert acao(c,e,'comparar',pesos=[30,30,30],origem='manual').status_code==422
        anterior=deepcopy(e)
        e=acao(c,e,'prioridades',comparacoes=[2,6,3]).json()
        assert e['resultado'] is None and e['salvo_revisao'] is None and e['pesos']==[60,30,10]
        assert acao(c,anterior,'comparar',pesos=[60,30,10],origem='manual').status_code==422
        e=acao(c,e,'comparar',pesos=e['pesos'],origem='ahp').json()
        e=acao(c,e,'salvar').json();assert e['salvo_revisao']==2
        r=c.get(f'/api/areas/{ident}/revisoes/1/simples');assert r.status_code==200
        assert '33.34%' in r.text


def test_sessao_isolada_sem_login_e_sem_leitura_cruzada(app):
    """A ausência de login não torna áreas e relatórios acessíveis por outras sessões."""
    with TestClient(app) as a,TestClient(app) as b:
        e=completo(a);e=acao(a,e,'salvar').json()
        assert b.get(f'/api/areas/{e["id"]}').status_code==404
        assert b.get(f'/api/areas/{e["id"]}/revisoes/1/tecnico').status_code==404
        assert b.post(f'/api/areas/{e["id"]}/analisar',headers=CAB,json={'versao':e['versao']}).status_code==404
        cookies=a.get('/api/saude').headers['set-cookie'].lower()
        assert 'httponly' in cookies and 'samesite=strict' in cookies


def test_orig_supressao_campos_e_rotas_antigas_fechadas(app):
    """Bloqueia origem externa, corpo sem cabeçalho e rotas antigas de diagnóstico."""
    with TestClient(app) as c:
        assert c.post('/api/areas',files={'arquivo':('x.geojson',b'{}')}).status_code==403
        assert c.post('/api/areas',headers={**CAB,'Origin':'https://outro.example'},files={'arquivo':('x.geojson',b'{}')}).status_code==403
        assert c.get('/api/v1/analises').status_code==404
        assert c.get('/api/casos/../../AGENTS.md').status_code==404
        assert c.get('/api/saude').json()['ml'] is False


def test_nome_de_arquivo_nao_identifica_mina_e_fora_cobertura_nao_classifica(app):
    """Mudar o nome não muda fonte; contorno desconhecido não recebe nota por aproximação."""
    with TestClient(app) as c:
        e=c.post('/api/areas',headers=CAB,files={'arquivo':('Burning-Star.geojson',(DADOS/'il_006/area.geojson').read_bytes())}).json()
        assert e['nome']=='Rapatee'
        d={'type':'FeatureCollection','features':[{'type':'Feature','properties':{},'geometry':{'type':'Polygon','coordinates':[[[0,0],[.01,0],[.01,.01],[0,.01],[0,0]]]}}]}
        e=c.post('/api/areas',headers=CAB,files={'arquivo':('Rapatee.geojson',json.dumps(d).encode())}).json()
        assert not e['cobertura_disponivel'] and acao(c,e,'analisar').status_code==422
        assert acao(c,e,'comparar',pesos=[40,30,30],origem='manual').status_code==422


def test_integridade_da_fonte_impede_resultado(tmp_path):
    """Não carrega uma fonte corrompida mesmo se seu nome e seu manifesto existirem."""
    import shutil
    shutil.copytree(DADOS/'il_006',tmp_path/'il_006')
    with (tmp_path/'il_006/relevo.tif').open('ab') as p:p.write(b'adulterado')
    with pytest.raises(ErroDecisao):carregar_caso('il_006',tmp_path)


def test_geografia_recalculada_dos_rasters_e_hipoteses_explicitas():
    """As notas derivam das medições locais e o sistema preserva a ausência de parecer de segurança."""
    e=resumo_entrada((DADOS/'il_006/area.geojson').read_bytes(),'mina.geojson');a=analisar_territorio(e)
    assert len(a['matriz'])==3 and all(len(l)==3 for l in a['matriz'])
    assert a['relevo']['fracao_valida']>=.9 and a['cobertura']['area']['fracao_valida']>=.9
    assert sum(a['cobertura']['area']['percentuais'].values())==pytest.approx(100)
    assert a['triagem']['decisao_de_uso']=='pendente_de_estudos'
    assert all('não calibrados' in r['natureza_regra'] for r in a['regras'])


def test_sqlite_revisoes_immutaveis_e_reabertura(app):
    """Relatório continua disponível após reinício com a mesma sessão e banco; UPDATE é recusado."""
    with TestClient(app) as c:
        e=completo(c);e=acao(c,e,'salvar').json();token=c.cookies.get('geovale_sessao')
    novo=criar_app(app.state.revisoes.caminho)
    with TestClient(novo) as c:
        c.cookies.set('geovale_sessao',token)
        assert c.get(f'/api/areas/{e["id"]}/revisoes/1/simples').status_code==200
    with app.state.revisoes.conectar() as con:
        with pytest.raises(sqlite3.IntegrityError):con.execute("UPDATE estudos_mcda_v2 SET sha256='alterado'")


def test_fonte_ausente_retorna_mensagem_compreensivel(tmp_path):
    """Arquivo ausente bloqueia a jornada sem gerar nota substituta ou erro interno."""
    from shutil import copytree
    from geovale.decisao.territorio import DADOS
    dados=tmp_path/'dados'
    copytree(DADOS,dados)
    (dados/'il_006/relevo.tif').unlink()
    with TestClient(criar_app(tmp_path/'banco.sqlite3',dados)) as cliente:
        r=enviar(cliente)
        assert r.status_code==422
        assert 'ausente' in r.json()['mensagem']


@pytest.mark.parametrize('caminho',['/api/casos','/api/casos/il_006/mapa','/api/casos/il_071/mapa','/api/casos/il_006/imagem','/api/casos/il_071/imagem'])
def test_catalogo_e_downloads_de_exemplos_retirados(app,caminho):
    """O servidor não lista minas nem distribui contornos ou fotos por rotas de exemplos."""
    with TestClient(app) as cliente:
        assert cliente.get(caminho).status_code==404


@pytest.mark.parametrize('codigo',['il_006','il_071'])
def test_imagem_so_aparece_apos_upload_e_apenas_na_sessao_proprietaria(app,codigo):
    """Preserva a foto aérea dos dois mapas sem reintroduzir um catálogo público."""
    with TestClient(app) as proprietario,TestClient(app) as outra_sessao:
        e=enviar(proprietario,codigo).json()
        url=e['imagem']['url']
        assert url==f'/api/areas/{e["id"]}/imagem'
        imagem=proprietario.get(url)
        assert imagem.status_code==200 and imagem.headers['content-type']=='image/jpeg'
        assert imagem.content[:2]==b'\xff\xd8'
        assert outra_sessao.get(url).status_code==404


def test_contorno_sem_fontes_nao_tem_imagem_nem_convite_a_exemplos(app):
    """Área desconhecida preserva mapa vetorial e erro de cobertura sem oferecer exemplos no site."""
    documento={'type':'FeatureCollection','features':[{'type':'Feature','properties':{},'geometry':{'type':'Polygon','coordinates':[[[0,0],[.01,0],[.01,.01],[0,.01],[0,0]]]}}]}
    with TestClient(app) as cliente:
        e=cliente.post('/api/areas',headers=CAB,files={'arquivo':('minha-area.geojson',json.dumps(documento).encode())}).json()
        assert e['imagem'] is None
        assert cliente.get(f'/api/areas/{e["id"]}/imagem').status_code==404
        erro=acao(cliente,e,'analisar')
        assert erro.status_code==422 and 'fontes territoriais' in erro.json()['mensagem']


@pytest.mark.parametrize('metodo',['GET','POST'])
def test_sem_carregamento_embutido_de_poligonal(app,metodo):
    """Uma URL antiga não cria áreas nem permite contornar o envio do arquivo."""
    with TestClient(app) as cliente:
        resposta=cliente.request(metodo,'/api/areas/exemplo',headers=CAB)
        assert resposta.status_code in (404,405)
        assert not app.state.registros


@pytest.mark.parametrize('tipo',['Polygon','MultiPolygon'])
def test_envio_com_posicoes_2d_e_3d_abre_sem_alterar_documento(app,tipo):
    """Altitudes opcionais misturadas não impedem visualizar a superfície aceita pelo validador."""
    anel=[[0,0,5],[.01,0],[.01,.01,9],[0,.01],[0,0,5]]
    coordenadas=[anel] if tipo=='Polygon' else [[anel]]
    documento={'type':'FeatureCollection','features':[{'type':'Feature','properties':None,'geometry':{'type':tipo,'coordinates':coordenadas}}]}
    with TestClient(app) as cliente:
        r=cliente.post('/api/areas',headers=CAB,files={'arquivo':('area.geojson',json.dumps(documento).encode())})
        assert r.status_code==201,r.text
        e=r.json();assert e['area_ha']>0 and not e['cobertura_disponivel']
        original=app.state.registros[e['id']]['entrada']['documento']
        assert original==documento
        assert all(len(p)==2 for p in (e['geometria']['coordinates'][0] if tipo=='Polygon' else e['geometria']['coordinates'][0][0]))


@pytest.mark.parametrize('acao_nome,campos',[
    ('comparar',{'pesos':[10**400,0,0],'origem':'manual'}),
    ('prioridades',{'comparacoes':[10**400,1,1]})])
def test_inteiros_extremos_retornam_erro_sem_alterar_analise(app,acao_nome,campos):
    """Números JSON grandes demais geram erro compreensível, preservando o estado anterior."""
    with TestClient(app) as cliente:
        e=enviar(cliente).json();e=acao(cliente,e,'analisar').json()
        r=acao(cliente,e,acao_nome,**campos)
        assert r.status_code==422 and 'mensagem' in r.json()
        assert cliente.get(f'/api/areas/{e["id"]}').json()==e


def test_altitude_fora_da_representacao_numerica_e_recusada(app):
    """Uma altitude inteira excessiva não escapa como falha interna depois da validação."""
    documento={'type':'FeatureCollection','features':[{'type':'Feature','properties':None,'geometry':{'type':'Polygon','coordinates':[[[0,0],[.01,0,10**400],[.01,.01],[0,.01],[0,0]]]}}]}
    with TestClient(app) as cliente:
        r=cliente.post('/api/areas',headers=CAB,files={'arquivo':('area.geojson',json.dumps(documento).encode())})
        assert r.status_code==422 and r.json()['codigo']=='NUMERO_INVALIDO'
        assert not app.state.registros


@pytest.mark.parametrize('tipo',['simples','tecnico'])
@pytest.mark.parametrize('atualizar_manifesto',[False,True])
def test_relatorio_recusa_imagem_diferente_da_revisao_salva(tmp_path,tipo,atualizar_manifesto):
    """Relatório não troca a fotografia congelada por bytes alterados, mesmo com novo manifesto válido."""
    from shutil import copytree
    from hashlib import sha256
    dados=tmp_path/'dados';copytree(DADOS,dados)
    app=criar_app(tmp_path/'relatorio.sqlite3',dados)
    with TestClient(app) as cliente:
        e=completo(cliente);e=acao(cliente,e,'salvar').json()
        imagem=dados/'il_006/imagem.jpg';imagem.write_bytes(imagem.read_bytes()+b'alteracao')
        if atualizar_manifesto:
            caminho=dados/'il_006/manifesto.json';manifesto=json.loads(caminho.read_text())
            manifesto['sha256']['imagem.jpg']=sha256(imagem.read_bytes()).hexdigest()
            caminho.write_text(json.dumps(manifesto))
        r=cliente.get(f'/api/areas/{e["id"]}/revisoes/1/{tipo}')
        assert r.status_code==422 and 'mensagem' in r.json()
        assert app.state.revisoes.ler(e['id'],1,app.state.registros[e['id']]['dono']) is not None
