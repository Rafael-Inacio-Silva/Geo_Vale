"""API local e entrega da interface de navegação do GeoVale."""

import json
import sqlite3
import zlib
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from shapely.errors import ShapelyError
from shapely.geometry import shape
from fastapi.responses import FileResponse, JSONResponse, Response
from fastapi.staticfiles import StaticFiles

from geovale.territorio import DadosTerritoriais
from geovale.camadas import CAMADAS
from geovale.influencia import ler_influencia
from geovale.anm import ProcessosANM
from geovale.municipio import LimitesMunicipais
from geovale.trilhas import TrilhasMunicipais, recortar_trilhas
from geovale.mapa import FonteIndisponivel, LimiteEstadual

RAIZ = Path(__file__).resolve().parents[3]


def criar_app(limite=None, raiz=RAIZ, trilhas=None, anm=None, municipios=None, territorios=None):
    """Expõe navegação, fontes territoriais e caracterização automática por mina."""
    fonte_territorios = territorios if territorios is not None else DadosTerritoriais(raiz)

    @asynccontextmanager
    async def ciclo_vida(app):
        fonte_territorios.iniciar()
        try:
            yield
        finally:
            fonte_territorios.encerrar()

    app = FastAPI(title='GeoVale — mapa territorial', version='4.0.0', docs_url=None, redoc_url=None, openapi_url=None, lifespan=ciclo_vida)
    fonte = limite if limite is not None else LimiteEstadual()
    fonte_trilhas = trilhas if trilhas is not None else TrilhasMunicipais()
    fonte_anm = anm if anm is not None else ProcessosANM()
    fonte_municipios = municipios if municipios is not None else LimitesMunicipais()
    minas = json.loads((raiz / 'dados/minas.json').read_text(encoding='utf-8'))

    @app.get('/api/saude')
    def saude():
        """Indica disponibilidade do aplicativo, independentemente da fonte externa."""
        return {'status': 'ok', 'versao': '4.0.0'}

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

    @app.get('/api/minas/{mina_id}/influencia')
    def influencia_mina(mina_id: str):
        """Entrega o recorte comum aproximado e a mina cartográfica sombreada."""
        if not any(item['id'] == mina_id for item in minas):
            return JSONResponse(status_code=404, content={'mensagem': 'Mina não encontrada.'})
        try:
            dados = ler_influencia(raiz / 'dados/influencias' / f'{mina_id}.geojson', mina_id)
            return JSONResponse(dados, headers={'Cache-Control': 'no-store'})
        except (OSError, ValueError, KeyError, TypeError, ShapelyError, sqlite3.Error, zlib.error):
            return JSONResponse(status_code=503, content={'mensagem': 'O contorno de influência está indisponível. Tente novamente.'})

    @app.get('/api/minas/{mina_id}/trilhas-influencia')
    def trilhas_influencia(mina_id: str):
        """Entrega trilhas visuais somente dentro do contorno local validado."""
        if not any(item['id'] == mina_id for item in minas):
            return JSONResponse(status_code=404, content={'mensagem': 'Mina não encontrada.'})
        try:
            dados = ler_influencia(raiz / 'dados/influencias' / f'{mina_id}.geojson', mina_id)
            recorte = shape(next(f['geometry'] for f in dados['features'] if f['properties']['id'] == 'influencia'))
            trilhas = fonte_trilhas.obter(','.join(map(str, recorte.bounds)))
            return JSONResponse(recortar_trilhas(trilhas, recorte), headers={'Cache-Control': 'no-store'})
        except (FonteIndisponivel, OSError, ValueError, KeyError, TypeError, ShapelyError):
            return JSONResponse(status_code=503, content={'mensagem': 'As trilhas estão indisponíveis. Tente novamente.'})

    @app.get('/api/minas/{mina_id}/relatorio')
    def relatorio_territorio(mina_id: str):
        """Baixa um JSON completo com atributos, geometrias, matrizes, fontes e datas guardados."""
        if not any(item['id'] == mina_id for item in minas):
            return JSONResponse(status_code=404, content={'mensagem': 'Mina não encontrada.'})
        try:
            dados = fonte_territorios.relatorio(mina_id)
            bruto = json.dumps(dados, ensure_ascii=False, allow_nan=False).encode()
            if len(bruto) > 64 * 1024 * 1024:
                return JSONResponse(status_code=413, content={'mensagem': 'O relatório excede o limite de exportação.'})
            return Response(bruto, media_type='application/json', headers={'Content-Disposition': f'attachment; filename="geovale-{mina_id}.json"', 'Cache-Control': 'no-store'})
        except (OSError, ValueError, KeyError, TypeError, ShapelyError, sqlite3.Error, zlib.error):
            return JSONResponse(status_code=503, content={'mensagem': 'O relatório completo ainda não está disponível. Tente novamente.'})

    @app.get('/api/minas/{mina_id}/territorio')
    def territorio_mina(mina_id: str):
        """Lê o catálogo inteiro já associado à mina, sem parâmetros de visibilidade."""
        if not any(item['id'] == mina_id for item in minas):
            return JSONResponse(status_code=404, content={'mensagem': 'Mina não encontrada.'})
        try:
            return JSONResponse(fonte_territorios.obter(mina_id), headers={'Cache-Control': 'no-store'})
        except (OSError, ValueError, KeyError, TypeError, ShapelyError, sqlite3.Error, zlib.error):
            return JSONResponse(status_code=503, content={'mensagem': 'Os dados do território estão indisponíveis. A preparação automática continua.'}, headers={'Cache-Control': 'no-store'})

    @app.get('/api/minas/{mina_id}/territorio/{base_id}')
    def registros_territorio(mina_id: str, base_id: str):
        """Lê todos os atributos/recortes persistidos de uma base identificada no catálogo."""
        if not any(item['id'] == mina_id for item in minas):
            return JSONResponse(status_code=404, content={'mensagem': 'Mina não encontrada.'})
        try:
            dados = fonte_territorios.registros(mina_id, base_id)
            if dados is None:
                return JSONResponse(status_code=503, content={'mensagem': 'Esta base ainda está sendo preparada.'})
            return JSONResponse(dados, headers={'Cache-Control': 'no-store'})
        except KeyError:
            return JSONResponse(status_code=404, content={'mensagem': 'Base não encontrada.'})
        except (OSError, ValueError, TypeError, ShapelyError, sqlite3.Error, zlib.error):
            return JSONResponse(status_code=503, content={'mensagem': 'Os registros estão temporariamente indisponíveis.'})

    @app.get('/api/minas/{mina_id}/territorio/{base_id}/arquivo')
    def arquivo_territorio(mina_id: str, base_id: str):
        """Entrega os valores matriciais guardados em GeoTIFF, sem nova extração externa."""
        if not any(item['id'] == mina_id for item in minas):
            return JSONResponse(status_code=404, content={'mensagem': 'Mina não encontrada.'})
        try:
            bruto = fonte_territorios.arquivo(mina_id, base_id)
            if bruto is None:
                return JSONResponse(status_code=404, content={'mensagem': 'Arquivo matricial não disponível.'})
            return Response(bruto, media_type='image/tiff', headers={'Content-Disposition': f'attachment; filename="territorio-{base_id}.tif"', 'Cache-Control': 'no-store'})
        except KeyError:
            return JSONResponse(status_code=404, content={'mensagem': 'Base não encontrada.'})
        except (OSError, ValueError, TypeError, ShapelyError, sqlite3.Error, zlib.error):
            return JSONResponse(status_code=503, content={'mensagem': 'O arquivo está temporariamente indisponível.'})

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
