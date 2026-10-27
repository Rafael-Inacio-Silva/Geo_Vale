"""Consulta de leitura da camada pública de trilhas da Prefeitura de Nova Lima."""

from collections import OrderedDict
from copy import deepcopy
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import json
import math
from threading import Lock
from time import monotonic
from urllib.parse import urlencode
from urllib.request import urlopen
from shapely import union_all
from shapely.geometry import shape, mapping
from geovale.geometria import partes_da_dimensao
from geovale.mapa import FonteIndisponivel

SERVICO = 'https://services3.arcgis.com/8p5P2iPRkT0RXnI3/arcgis/rest/services/Trilhas/FeatureServer/0'
SIMBOLOGIA = 'https://pmnl.maps.arcgis.com/sharing/rest/content/items/2504a27b4e684bfdbe0210fa7af1971d/data?f=json'
COBERTURA = (-44.005239, -20.211133, -43.749500, -19.923717)


def preparar_extensao(texto):
    """Valida o envelope pedido e limita a consulta à extensão publicada pela fonte."""
    try:
        partes = texto.split(',')
        if len(partes) != 4 or len(texto) > 150:
            raise ValueError()
        oeste, sul, leste, norte = map(float, partes)
        if not all(math.isfinite(v) for v in (oeste, sul, leste, norte)):
            raise ValueError()
        if not -180 <= oeste < leste <= 180 or not -85 <= sul < norte <= 85:
            raise ValueError()
    except (ValueError, TypeError, AttributeError):
        raise ValueError('A extensão solicitada é inválida.') from None
    if leste <= COBERTURA[0] or oeste >= COBERTURA[2] or norte <= COBERTURA[1] or sul >= COBERTURA[3]:
        return None
    return (max(oeste, COBERTURA[0]), max(sul, COBERTURA[1]), min(leste, COBERTURA[2]), min(norte, COBERTURA[3]))


def consultar_trilhas(extensao):
    """Consulta somente o serviço fixo e limita tempo, tamanho e quantidade da resposta."""
    parametros = {
        'f': 'geojson', 'where': '1=1', 'geometry': ','.join(map(str, extensao)),
        'geometryType': 'esriGeometryEnvelope', 'inSR': '4326', 'outSR': '4326',
        'spatialRel': 'esriSpatialRelIntersects', 'outFields': 'OBJECTID,Name',
        'returnGeometry': 'true', 'resultRecordCount': 2000, 'orderByFields': 'OBJECTID',
    }
    with urlopen(SERVICO + '/query?' + urlencode(parametros), timeout=15) as resposta:
        bruto = resposta.read(6 * 1024 * 1024 + 1)
    if len(bruto) > 6 * 1024 * 1024:
        raise FonteIndisponivel()
    return json.loads(bruto)


def consultar_simbologia():
    """Lê as categorias oficiais do item da camada, separadas das geometrias."""
    with urlopen(SIMBOLOGIA, timeout=15) as resposta:
        bruto = resposta.read(1024 * 1024 + 1)
    if len(bruto) > 1024 * 1024:
        raise FonteIndisponivel()
    return json.loads(bruto)


def preparar_simbologia(documento):
    """Valida cores, nomes e símbolos lineares, sem importar configuração executável."""
    try:
        camadas = [camada for camada in documento['layers'] if camada.get('id') == 0]
        if len(camadas) != 1:
            raise ValueError()
        renderer = camadas[0]['layerDefinition']['drawingInfo']['renderer']
        categorias = renderer['uniqueValueInfos']
        if renderer['type'] != 'uniqueValue' or renderer['field1'] != 'Name' or not isinstance(categorias, list) or not 1 <= len(categorias) <= 2000:
            raise ValueError()
        simbolos = {}
        for categoria in categorias:
            valor, nome, simbolo = categoria['value'], categoria['label'], categoria['symbol']
            if not all(isinstance(v, str) and 0 < len(v) <= 254 for v in (valor, nome)):
                raise ValueError()
            if simbolo['type'] != 'esriSLS' or simbolo['style'] != 'esriSLSSolid':
                raise ValueError()
            rgba, largura = simbolo['color'], simbolo['width']
            if not isinstance(rgba, list) or len(rgba) != 4 or any(type(v) is not int or not 0 <= v <= 255 for v in rgba):
                raise ValueError()
            if type(largura) not in (int, float) or not 0 < largura <= 20:
                raise ValueError()
            chave = valor.casefold()
            if chave in simbolos:
                raise ValueError()
            simbolos[chave] = {'id': valor, 'nome': nome, 'cor': '#' + ''.join(f'{v:02x}' for v in rgba[:3]), 'opacidade': rgba[3] / 255, 'largura': largura * 96 / 72}
        return simbolos
    except (KeyError, TypeError, AttributeError, ValueError):
        raise FonteIndisponivel() from None


def aplicar_simbologia(dados, simbolos):
    """Relaciona o Name ao símbolo oficial e inclui apenas categorias do recorte pedido."""
    presentes = set()
    for feicao in dados['features']:
        propriedades = feicao['properties']
        chave = propriedades['nome'].casefold()
        if chave not in simbolos:
            raise FonteIndisponivel()
        simbolo = simbolos[chave]
        propriedades.update({campo: simbolo[campo] for campo in ('cor', 'opacidade', 'largura')})
        presentes.add(chave)
    dados['legenda'] = [deepcopy(simbolo) for chave, simbolo in simbolos.items() if chave in presentes]
    return dados


def preparar_trilhas(documento):
    """Retém somente linhas válidas, identificação e nome da base, sem HTML da fonte."""
    if not isinstance(documento, dict) or documento.get('type') != 'FeatureCollection':
        raise FonteIndisponivel()
    if documento.get('exceededTransferLimit') or (documento.get('properties') or {}).get('exceededTransferLimit'):
        raise FonteIndisponivel()
    feicoes = documento.get('features')
    if not isinstance(feicoes, list) or len(feicoes) > 2000:
        raise FonteIndisponivel()
    saida = []
    for feicao in feicoes:
        if not isinstance(feicao, dict) or feicao.get('type') != 'Feature':
            raise FonteIndisponivel()
        geom = feicao.get('geometry')
        if not isinstance(geom, dict) or geom.get('type') not in ('LineString', 'MultiLineString'):
            raise FonteIndisponivel()
        try:
            linha = shape(geom)
            if linha.is_empty or not linha.is_valid:
                raise ValueError()
            oeste, sul, leste, norte = linha.bounds
            if not (COBERTURA[0] - .01 <= oeste <= leste <= COBERTURA[2] + .01 and COBERTURA[1] - .01 <= sul <= norte <= COBERTURA[3] + .01):
                raise ValueError()
        except Exception:
            raise FonteIndisponivel() from None
        props = feicao.get('properties') or {}
        nome = str(props.get('Name') or 'Trilha sem nome')[:254]
        saida.append({'type': 'Feature', 'geometry': geom, 'properties': {'nome': nome, 'id': props.get('OBJECTID')}})
    return {'type': 'FeatureCollection', 'features': saida}


class TrilhasMunicipais:
    """Mantém até 16 envelopes válidos em memória por dez minutos, sem dados em disco."""

    def __init__(self, consultar=consultar_trilhas, relogio=monotonic, consultar_simbolos=consultar_simbologia):
        self.consultar = consultar
        self.relogio = relogio
        self.consultar_simbolos = consultar_simbolos
        self.simbologia = None
        self.cache = OrderedDict()
        self.trava = Lock()

    def obter(self, texto):
        """Busca o recorte visível; fora da cobertura devolve vazio explicitamente identificado."""
        extensao = preparar_extensao(texto)
        if extensao is None:
            return {'type': 'FeatureCollection', 'features': [], 'legenda': [], 'fora_cobertura': True}
        with self.trava:
            anterior = self.cache.get(extensao)
            if anterior and self.relogio() - anterior[0] < 600:
                self.cache.move_to_end(extensao)
                return deepcopy(anterior[1])
            try:
                if self.simbologia is None or self.relogio() - self.simbologia[0] >= 600:
                    with ThreadPoolExecutor(max_workers=2) as consultas:
                        geometrias = consultas.submit(self.consultar, extensao)
                        simbolos = consultas.submit(self.consultar_simbolos)
                        dados = preparar_trilhas(geometrias.result())
                        categorias = preparar_simbologia(simbolos.result())
                    self.simbologia = (self.relogio(), categorias)
                else:
                    dados = preparar_trilhas(self.consultar(extensao))
                dados = aplicar_simbologia(dados, self.simbologia[1])
            except Exception:
                raise FonteIndisponivel() from None
            dados['fora_cobertura'] = False
            dados['fonte'] = {'nome': 'Prefeitura de Nova Lima — Trilhas (Decreto 6773/2016)', 'url': SERVICO, 'simbologia_url': SIMBOLOGIA, 'consultado_em': datetime.now(timezone.utc).isoformat()}
            self.cache[extensao] = (self.relogio(), dados)
            self.cache.move_to_end(extensao)
            while len(self.cache) > 16:
                self.cache.popitem(last=False)
            return deepcopy(dados)


def recortar_trilhas(dados, recorte):
    """Recorta linhas visuais pelo polígono irregular, preservando nomes e símbolos oficiais."""
    saida = deepcopy(dados)
    saida['features'] = []
    nomes = set()
    for feicao in dados['features']:
        linha = union_all(partes_da_dimensao(shape(feicao['geometry']).intersection(recorte), ('LineString', 'MultiLineString')))
        if linha.is_empty:
            continue
        saida['features'].append({**deepcopy(feicao), 'geometry': mapping(linha)})
        nomes.add(feicao['properties']['nome'].casefold())
    saida['legenda'] = [c for c in saida['legenda'] if c['nome'].casefold() in nomes or c['id'].casefold() in nomes]
    return saida
