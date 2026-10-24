"""API da demonstração local, sem tela de login e com isolamento das análises por sessão."""
from pathlib import Path
from copy import deepcopy
from datetime import datetime,timezone,timedelta
from hashlib import sha256
from threading import RLock
from uuid import uuid4
import json,os,secrets

from fastapi import FastAPI,Request,HTTPException
from fastapi.responses import JSONResponse,FileResponse,Response
from starlette.concurrency import run_in_threadpool
from starlette.staticfiles import StaticFiles
from starlette.middleware.trustedhost import TrustedHostMiddleware

from geovale.geografia.entrada import ErroEntrada
from geovale.decisao.metodos import ErroDecisao
from geovale.decisao.territorio import DADOS,carregar_caso,resumo_entrada,analisar_territorio
from .armazenamento import Revisoes
from .entrada_http import _ler_arquivo
from .servico import iniciar,publicar,registrar_ahp,comparar,retrato,conferir_versao


async def ler_json(request:Request) -> dict:
    """Limita JSON antes de interpretar e rejeita chaves duplicadas e números não finitos."""
    raw=bytearray()
    async for bloco in request.stream():
        raw.extend(bloco)
        if len(raw)>16384:raise HTTPException(413,'A configuração enviada excede o limite.')
    def unico(pares):
        """Impede que duas chaves iguais tenham interpretações diferentes na trilha de cálculo."""
        d={}
        for k,v in pares:
            if k in d:raise ValueError('Chave repetida')
            d[k]=v
        return d
    def invalido(_):
        """Recusa extensões NaN e Infinity do decodificador JSON."""
        raise ValueError('Número não finito')
    try:d=json.loads(raw,object_pairs_hook=unico,parse_constant=invalido)
    except (ValueError,UnicodeError,RecursionError) as e:raise HTTPException(400,'Configuração JSON inválida.') from e
    if not isinstance(d,dict):raise HTTPException(422,'Envie uma configuração em objeto JSON.')
    return d


def criar_app(caminho_banco:Path|None=None,dados:Path=DADOS) -> FastAPI:
    """Monta jornada única para execução local; publicação externa exige configuração própria de acesso."""
    app=FastAPI(title='GeoVale',version='2.0.0',docs_url=None,redoc_url=None,openapi_url=None)
    raiz=Path(__file__).resolve().parents[3]
    banco=Revisoes(caminho_banco or Path(os.environ.get('GEOVALE_BANCO',str(raiz/'.local/geovale.sqlite3'))))
    registros={};trava=RLock()
    app.state.registros=registros
    app.state.revisoes=banco
    app.add_middleware(TrustedHostMiddleware,allowed_hosts=['localhost','127.0.0.1','testserver'])
    origens={'http://localhost:5173','http://127.0.0.1:5173','http://localhost:8000','http://127.0.0.1:8000','http://testserver'}

    @app.middleware('http')
    async def sessao(request:Request,call_next):
        """Cria sessão sem login; bloqueia mutações de outras origens e mantém cookie fora do JavaScript."""
        if request.method in ('POST','PUT','PATCH','DELETE'):
            if request.headers.get('X-GeoVale')!='1' or (request.headers.get('origin') and request.headers['origin'] not in origens | {str(request.base_url).rstrip('/')} ):
                return JSONResponse({'mensagem':'Origem da operação não autorizada.'},status_code=403)
        token=request.cookies.get('geovale_sessao','')
        if len(token)!=64 or any(c not in '0123456789abcdef' for c in token):token=secrets.token_hex(32)
        request.state.dono=sha256(token.encode()).hexdigest()
        r=await call_next(request)
        r.set_cookie('geovale_sessao',token,httponly=True,samesite='strict',secure=False,max_age=86400)
        r.headers.update({'Cache-Control':'no-store','X-Content-Type-Options':'nosniff','Referrer-Policy':'no-referrer'})
        return r

    @app.exception_handler(ErroEntrada)
    async def entrada_invalida(request:Request,exc:ErroEntrada):
        """Mostra causa compreensível sem copiar o conteúdo enviado para a mensagem."""
        return JSONResponse({'mensagem':exc.mensagem,'codigo':exc.codigo},status_code=exc.status)

    @app.exception_handler(ErroDecisao)
    async def decisao_invalida(request:Request,exc:ErroDecisao):
        """Mantém dados incompletos como erro explícito, sem resultado substituto."""
        return JSONResponse({'mensagem':str(exc)},status_code=422)

    @app.exception_handler(HTTPException)
    async def http_invalido(request:Request,exc:HTTPException):
        """Uniformiza erros para a interface sem exigir leitura de logs."""
        return JSONResponse({'mensagem':str(exc.detail)},status_code=exc.status_code)

    def estudar(identificador:str,request:Request) -> dict:
        """Restringe rascunhos ao proprietário e não distingue inexistente de não autorizado."""
        e=registros.get(identificador)
        if e is None or e['dono']!=request.state.dono:raise HTTPException(404,'Análise não encontrada nesta sessão.')
        return e

    @app.get('/api/saude')
    async def saude():
        """Confirma o escopo ativo sem inicializar modelos ou solicitar credenciais."""
        return {'estado':'disponivel','versao':'2.0.0','metodo':'GIS + AHP + TOPSIS','modo':'demonstracao_local','ml':False}

    @app.get('/api/areas/{identificador}/imagem')
    async def imagem_area(identificador:str,request:Request):
        """Exibe o fundo da área enviada apenas à sua sessão, sem catálogo ou download de mapas."""
        with trava:
            codigo=estudar(identificador,request)['entrada']['caso']
        if not codigo:raise HTTPException(404,'Imagem de referência indisponível para esta área.')
        carregar_caso(codigo,dados)
        return FileResponse(dados/codigo/'imagem.jpg',media_type='image/jpeg')

    def registrar_entrada(entrada:dict,request:Request) -> dict:
        """Registra o arquivo enviado com sessão, expiração e limites de áreas temporárias."""
        with trava:
            expiracao=datetime.now(timezone.utc)-timedelta(hours=2)
            for k in list(registros):
                if datetime.fromisoformat(registros[k]['criado_em'])<expiracao:del registros[k]
            if len(registros)>=100 or sum(v['dono']==request.state.dono for v in registros.values())>=20:
                raise HTTPException(429,'A sessão atingiu o limite de áreas temporárias.')
            e=iniciar(entrada,str(uuid4()),request.state.dono);registros[e['id']]=e
            return publicar(e)

    @app.post('/api/areas',status_code=201)
    async def enviar(request:Request):
        """Valida e mostra a poligonal antes de executar qualquer extração de terreno ou comparação."""
        conteudo,nome=await _ler_arquivo(request)
        entrada=await run_in_threadpool(resumo_entrada,conteudo,nome,dados)
        return registrar_entrada(entrada,request)

    @app.get('/api/areas/{identificador}')
    async def consultar(identificador:str,request:Request):
        """Recupera o estado atual depois de um conflito ou interrupção de conexão."""
        with trava:return publicar(estudar(identificador,request))

    @app.post('/api/areas/{identificador}/analisar')
    async def analisar(identificador:str,request:Request):
        """Calcula geografia fora do loop HTTP e aceita somente a versão consultada da entrada."""
        corpo=await ler_json(request)
        with trava:
            e=estudar(identificador,request);conferir_versao(e,corpo);versao=e['versao'];entrada=deepcopy(e['entrada'])
        a=await run_in_threadpool(analisar_territorio,entrada,dados)
        with trava:
            e=estudar(identificador,request)
            if e['versao']!=versao:raise HTTPException(409,'A análise mudou durante o processamento. Consulte a versão atual.')
            e.update(analise=a,resultado=None,salvo_revisao=None,versao=versao+1)
            return publicar(e)

    @app.post('/api/areas/{identificador}/prioridades')
    async def prioridades(identificador:str,request:Request):
        """Calcula pesos a partir das comparações de prioridades com checagem de consistência."""
        corpo=await ler_json(request)
        with trava:
            e=estudar(identificador,request);registrar_ahp(e,corpo);return publicar(e)

    @app.post('/api/areas/{identificador}/comparar')
    async def comparacao(identificador:str,request:Request):
        """Calcula ranking e sensibilidade; falha não substitui resultado ou revisão anterior."""
        corpo=await ler_json(request)
        with trava:
            e=estudar(identificador,request);comparar(e,corpo);return publicar(e)

    @app.post('/api/areas/{identificador}/salvar')
    async def salvar(identificador:str,request:Request):
        """Salva um retrato exato e libera relatórios da revisão, sem recalcular durante a exportação."""
        corpo=await ler_json(request)
        with trava:
            e=estudar(identificador,request);conferir_versao(e,corpo)
            if not e['resultado']:raise ErroDecisao('Compare as opções antes de salvar o resultado.')
            if e['salvo_revisao'] is None:e['salvo_revisao']=banco.salvar(identificador,request.state.dono,retrato(e))
            return publicar(e)

    @app.get('/api/areas/{identificador}/revisoes/{revisao}/{tipo}')
    async def relatorio(identificador:str,revisao:int,tipo:str,request:Request):
        """Gera simples ou técnico a partir da mesma revisão persistida, inclusive depois de reiniciar a API."""
        if tipo not in ('simples','tecnico'):raise HTTPException(404,'Tipo de relatório desconhecido.')
        r=banco.ler(identificador,revisao,request.state.dono)
        if r is None:raise HTTPException(404,'Revisão não encontrada nesta sessão.')
        from .relatorios import gerar_relatorio
        html=await run_in_threadpool(gerar_relatorio,r,tipo,revisao,dados)
        return Response(html,media_type='text/html; charset=utf-8',headers={'Content-Disposition':f'attachment; filename="GeoVale-{tipo}-r{revisao}.html"'})

    distribuicao=raiz/'frontend/dist'
    if (distribuicao/'index.html').is_file():
        app.mount('/',StaticFiles(directory=distribuicao,html=True),name='interface')
    return app
