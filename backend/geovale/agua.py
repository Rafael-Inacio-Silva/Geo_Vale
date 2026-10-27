"""Caracterização preliminar da água no recorte documental fixo, por WFS e interseção."""
import hashlib
import json
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
from datetime import datetime, timezone
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from shapely import get_parts, union_all
from shapely.geometry import mapping, shape

from geovale.mapa import FonteIndisponivel

SERVICO = 'https://geoserver.meioambiente.mg.gov.br/ows'
MAX_FEICOES = 2000
MAX_BYTES = 12 * 1024 * 1024
BASES = (
    {'id': 'trechos', 'nome': 'Principais trechos hidrográficos',
     'camada': 'IDE:ide_0104_mg_hidrografia_principal_lin', 'chave': 'id',
     'campos': 'geom,id,noriocomp,dsversao,datverbase',
     'tipos': ('LineString', 'MultiLineString'),
     'metadado': 'https://idesisema.meioambiente.mg.gov.br/geonetwork/srv/por/catalog.search#/metadata/ebb215b7-10a5-481b-8cb2-823b4cf3d5e4'},
    {'id': 'massas', 'nome': "Massas d’água",
     'camada': 'IDE:ide_0103_mg_massa_dagua_bho_pol', 'chave': 'id_0',
     'campos': 'geom,id_0,nmoriginal,nmalternat,detipomass,deversao',
     'tipos': ('Polygon', 'MultiPolygon'),
     'metadado': 'https://idesisema.meioambiente.mg.gov.br/geonetwork/srv/por/catalog.search#/metadata/537a07b7-4a29-422d-bdde-43ae8af87b61'},
)


def consultar_base(base, limites):
    """Consulta apenas duas bases fixas, com projeção, campos, extensão e limites explícitos."""
    parametros = {
        'service': 'WFS', 'version': '2.0.0', 'request': 'GetFeature',
        'typeNames': base['camada'], 'outputFormat': 'application/json',
        'srsName': 'EPSG:4326', 'count': MAX_FEICOES + 1,
        'sortBy': base['chave'], 'propertyName': base['campos'],
        'CQL_FILTER': f"BBOX(geom,{','.join(map(str, limites))},'EPSG:4326')",
    }
    pedido = Request(SERVICO + '?' + urlencode(parametros), headers={
        'Accept': 'application/json', 'User-Agent': 'GeoVale/3.5 (caracterizacao territorial)',
    })
    with urlopen(pedido, timeout=15) as resposta:
        bruto = resposta.read(MAX_BYTES + 1)
    if len(bruto) > MAX_BYTES:
        raise FonteIndisponivel('Resposta de água excede o limite de tamanho.')
    return json.loads(bruto)


def texto_publicado(valor):
    """Conserva texto cadastral limitado; não preenche lacunas com inferências."""
    return valor.strip()[:300] if isinstance(valor, str) and valor.strip() else None


def partes_dimensionais(geometria, tipos):
    """Descarta somente contatos pontuais/lineares sem a dimensão esperada da base."""
    if geometria.is_empty:
        return []
    if geometria.geom_type in tipos:
        return [geometria]
    if geometria.geom_type == 'GeometryCollection':
        return [parte for grupo in get_parts(geometria) for parte in partes_dimensionais(grupo, tipos)]
    return []


def recortar_base(documento, base, recorte):
    """Valida completude, identidade e geometrias, contando cada registro uma única vez."""
    feicoes = documento['features']
    quantidade = documento['numberMatched']
    retornadas = documento['numberReturned']
    if (documento['type'] != 'FeatureCollection' or not isinstance(feicoes, list)
            or type(quantidade) is not int or type(retornadas) is not int
            or quantidade != retornadas or retornadas != len(feicoes)
            or not 0 <= quantidade <= MAX_FEICOES):
        raise FonteIndisponivel('Resposta incompleta ou excede o limite de registros.')
    crs = documento['crs']['properties']['name']
    if crs not in ('urn:ogc:def:crs:EPSG::4326', 'EPSG:4326', 'urn:ogc:def:crs:OGC:1.3:CRS84'):
        raise FonteIndisponivel('Referência espacial incompatível.')
    saida, identidades, versoes = [], set(), set()
    for feicao in feicoes:
        propriedades = feicao['properties']
        chave = propriedades[base['chave']]
        identidade = feicao['id']
        if (feicao['type'] != 'Feature' or type(chave) is not int or chave < 0
                or identidade != base['camada'].split(':')[1] + '.' + str(chave)
                or identidade in identidades):
            raise FonteIndisponivel('Identidade cadastral inválida ou duplicada.')
        identidades.add(identidade)
        geometria = shape(feicao['geometry'])
        if (geometria.geom_type not in base['tipos'] or geometria.is_empty or not geometria.is_valid
                or not (-180 <= geometria.bounds[0] <= geometria.bounds[2] <= 180
                        and -85 <= geometria.bounds[1] <= geometria.bounds[3] <= 85)):
            raise FonteIndisponivel('Geometria de água inválida; nenhum reparo automático foi aplicado.')
        cortada = union_all(partes_dimensionais(geometria.intersection(recorte), base['tipos']))
        if cortada.is_empty:
            continue
        if not cortada.is_valid or cortada.geom_type not in base['tipos']:
            raise FonteIndisponivel('Não foi possível recortar a geometria de água.')
        if base['id'] == 'trechos':
            nome = texto_publicado(propriedades['noriocomp'])
            tipo = None
            versao = texto_publicado(propriedades['dsversao'])
            revisao = texto_publicado(propriedades['datverbase'])
        else:
            nome = texto_publicado(propriedades['nmoriginal']) or texto_publicado(propriedades['nmalternat'])
            tipo = texto_publicado(propriedades['detipomass'])
            versao = texto_publicado(propriedades['deversao'])
            revisao = None
        if versao:
            versoes.add(versao)
        saida.append({'type': 'Feature', 'id': identidade, 'geometry': mapping(cortada),
                      'properties': {'id_fonte': identidade, 'base': base['id'], 'nome': nome,
                                     'tipo_publicado': tipo, 'versao_base': versao, 'revisao_base': revisao}})
    saida.sort(key=lambda f: f['properties']['id_fonte'])
    return saida, {'id': base['id'], 'nome': base['nome'], 'camada': base['camada'],
                   'metadado': base['metadado'], 'servico': SERVICO,
                   'registros_consultados': quantidade, 'registros_no_recorte': len(saida),
                   'versoes_publicadas': sorted(versoes),
                   'revisoes_publicadas': sorted({f['properties']['revisao_base'] for f in saida if f['properties']['revisao_base']})}


class ExtracaoAgua:
    """Mantém um único resultado completo por dez minutos, sem persistência nem execução periódica."""

    def __init__(self, consultar=consultar_base, relogio=time.monotonic):
        self._consultar = consultar
        self._relogio = relogio
        self._trava = threading.Lock()
        self._cache = None
        self._chave = None
        self._validade = 0

    def obter(self, referencias):
        """Recorta água superficial na AID águas/solos; filtros visuais e desenhos não alteram o recorte."""
        feicao = next(f for f in referencias['features'] if f['properties']['id'] == 'aid_agua_solos')
        chave = hashlib.sha256(json.dumps(feicao, sort_keys=True).encode()).hexdigest()
        chave_cache = (chave, referencias['fonte']['url'], referencias['fonte']['sha256_pdf'])
        with self._trava:
            if self._cache is not None and self._chave == chave_cache and self._relogio() < self._validade:
                return deepcopy(self._cache)
            try:
                recorte = shape(feicao['geometry'])
                if recorte.is_empty or not recorte.is_valid or recorte.geom_type not in ('Polygon', 'MultiPolygon'):
                    raise FonteIndisponivel('Recorte documental inválido.')
                with ThreadPoolExecutor(max_workers=2) as executor:
                    pedidos = [executor.submit(self._consultar, base, recorte.bounds) for base in BASES]
                    documentos = [pedido.result() for pedido in pedidos]
                feicoes, fontes = [], []
                for base, documento in zip(BASES, documentos):
                    cortadas, fonte = recortar_base(documento, base, recorte)
                    feicoes.extend(cortadas)
                    fontes.append(fonte)
                resultado = {'type': 'FeatureCollection', 'features': feicoes, 'mina_id': 'horizontes',
                             'consultado_em': datetime.now(timezone.utc).isoformat(), 'fontes': fontes,
                             'resumo': {fonte['id']: fonte['registros_no_recorte'] for fonte in fontes},
                             'recorte': {'id': 'aid_agua_solos', 'nome': 'Águas e solos · AID',
                                         'aproximado': True, 'figura': '2.3', 'pagina_pdf': 18,
                                         'data_mapa': '2023-11-02', 'fonte': referencias['fonte']['url'],
                                         'sha256_pdf': referencias['fonte']['sha256_pdf'], 'sha256_recorte': chave},
                             'metodo': 'Interseção vetorial em EPSG:4326; cada registro da fonte é contado uma vez.',
                             'aviso': 'Caracterização preliminar em contorno aproximado do projeto Tamanduá/Horizontes. Não avalia qualidade da água, impacto, segurança ou aptidão.'}
            except Exception as erro:
                raise FonteIndisponivel('A extração completa de água está indisponível.') from erro
            self._cache, self._chave = resultado, chave_cache
            self._validade = self._relogio() + 600
            return deepcopy(resultado)
