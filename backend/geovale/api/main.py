"""API local e entrega da interface de navegação do GeoVale."""

import json
from pathlib import Path

from fastapi import FastAPI, Request
from shapely.errors import ShapelyError
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from geovale.camadas import CAMADAS
from geovale.referencias import ler_referencias
from geovale.anm import ProcessosANM
from geovale.municipio import LimitesMunicipais
from geovale.area import AreaInvalida, validar_area
from geovale.trilhas import TrilhasMunicipais
from geovale.mapa import FonteIndisponivel, LimiteEstadual

RAIZ = Path(__file__).resolve().parents[3]


def criar_app(limite=None, raiz=RAIZ, trilhas=None, anm=None, municipios=None):
    """Expõe mapa, temas, trilhas, município, cadastro ANM e validação individual de áreas."""
    app = FastAPI(title='GeoVale — mapa territorial', version='3.4.0', docs_url=None, redoc_url=None, openapi_url=None)
    fonte = limite if limite is not None else LimiteEstadual()
    fonte_trilhas = trilhas if trilhas is not None else TrilhasMunicipais()
    fonte_anm = anm if anm is not None else ProcessosANM()
    fonte_municipios = municipios if municipios is not None else LimitesMunicipais()
    minas = json.loads((raiz / 'dados/minas.json').read_text(encoding='utf-8'))

    @app.get('/api/saude')
    def saude():
        """Indica disponibilidade do aplicativo, independentemente da fonte externa."""
        return {'status': 'ok', 'versao': '3.4.0'}

    @app.get('/api/mapa')
    def configuracao():
        """Entrega uma mina, os fundos e o catálogo fixo dos cinco temas e trilhas municipais."""
        return {
            'estado': {'nome': 'Minas Gerais', 'centro': [-18.6, -44.5], 'zoom': 6},
            'minas': minas,
            'camadas': CAMADAS,
            'fundos': [
                {
                    'id': 'mapa', 'nome': 'Mapa', 'zoom_maximo': 19,
                    'url': 'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
                    'credito': '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
                },
                {
                    'id': 'satelite', 'nome': 'Satélite', 'zoom_maximo': 19,
                    'url': 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
                    'credito': 'Tiles &copy; Esri — Source: Esri, Maxar, Earthstar Geographics, and the GIS User Community',
                },
            ],
        }

    @app.get('/api/mapa/limite-mg')
    def limite_mg():
        """Fornece o limite oficial simplificado para navegação, obtido pelo WFS."""
        try:
            return JSONResponse(fonte.obter(), headers={'Cache-Control': 'no-store'})
        except FonteIndisponivel:
            return JSONResponse(status_code=503, content={
                'mensagem': 'O contorno de Minas Gerais está indisponível. Tente novamente.',
            }, headers={'Cache-Control': 'no-store'})

    @app.get('/api/mapa/trilhas')
    def trilhas_visiveis(bbox: str):
        """Consulta a camada municipal fixa somente na extensão visível pedida."""
        try:
            return JSONResponse(fonte_trilhas.obter(bbox), headers={'Cache-Control': 'no-store'})
        except ValueError:
            return JSONResponse(status_code=422, content={'mensagem': 'A extensão solicitada é inválida.'})
        except FonteIndisponivel:
            return JSONResponse(status_code=503, content={'mensagem': 'As trilhas estão indisponíveis. Tente novamente.'})

    @app.get('/api/minas/{mina_id}/processo-anm')
    def processo_anm(mina_id: str):
        """Lê o processo fixado no catálogo, sem aceitar consultas ou URLs arbitrárias."""
        mina = next((item for item in minas if item['id'] == mina_id), None)
        if mina is None or not mina.get('processo_anm'):
            return JSONResponse(status_code=404, content={'mensagem': 'Mina não encontrada.'})
        try:
            processo = mina['processo_anm']
            return JSONResponse(fonte_anm.obter(processo['numero'], processo['ano']), headers={'Cache-Control': 'no-store'})
        except FonteIndisponivel:
            return JSONResponse(status_code=503, content={'mensagem': 'Os dados da ANM estão indisponíveis. Tente novamente.'}, headers={'Cache-Control': 'no-store'})

    @app.get('/api/minas/{mina_id}/referencias')
    def referencias_territoriais(mina_id: str):
        """Entrega somente a digitalização documental preparada para a mina do MVP."""
        if mina_id != 'horizontes' or not any(item['id'] == mina_id for item in minas):
            return JSONResponse(status_code=404, content={'mensagem': 'Mina não encontrada.'})
        try:
            return JSONResponse(ler_referencias(raiz / 'dados/referencias/horizontes.geojson'), headers={'Cache-Control': 'no-store'})
        except (OSError, ValueError, KeyError, TypeError, ShapelyError):
            return JSONResponse(status_code=503, content={'mensagem': 'As referências estão indisponíveis. Tente novamente.'})

    @app.get('/api/minas/{mina_id}/limite-municipal')
    def limite_municipal(mina_id: str):
        """Consulta apenas o código IBGE associado à mina do catálogo."""
        mina = next((item for item in minas if item['id'] == mina_id), None)
        if mina is None or not mina.get('codigo_municipio_ibge'):
            return JSONResponse(status_code=404, content={'mensagem': 'Mina não encontrada.'})
        try:
            return JSONResponse(fonte_municipios.obter(mina['codigo_municipio_ibge']), headers={'Cache-Control': 'no-store'})
        except FonteIndisponivel:
            return JSONResponse(status_code=503, content={'mensagem': 'O contorno municipal está indisponível. Tente novamente.'}, headers={'Cache-Control': 'no-store'})

    @app.post('/api/area/validar')
    async def validar_recorte(request: Request):
        """Valida sem gravar o desenho e limita a entrada a 128 KiB."""
        bruto = bytearray()
        async for parte in request.stream():
            bruto.extend(parte)
            if len(bruto) > 128 * 1024:
                return JSONResponse(status_code=413, content={'mensagem': 'O desenho excede o tamanho permitido.'})
        try:
            documento = json.loads(bruto)
            return JSONResponse(validar_area(documento), headers={'Cache-Control': 'no-store'})
        except AreaInvalida as erro:
            return JSONResponse(status_code=422, content={'mensagem': str(erro)})
        except (ValueError, RecursionError):
            return JSONResponse(status_code=422, content={'mensagem': 'Não foi possível ler o contorno desenhado.'})

    compilado = raiz / 'frontend/dist'
    if (compilado / 'assets').is_dir():
        app.mount('/assets', StaticFiles(directory=compilado / 'assets'), name='assets')

    @app.get('/', include_in_schema=False)
    def inicio():
        """Entrega a página inicial compilada sem capturar rotas desconhecidas."""
        if not (compilado / 'index.html').is_file():
            return JSONResponse(status_code=503, content={'mensagem': 'Compile a interface antes de iniciar o GeoVale.'})
        return FileResponse(compilado / 'index.html', headers={'Cache-Control': 'no-cache'})

    return app


app = criar_app()
