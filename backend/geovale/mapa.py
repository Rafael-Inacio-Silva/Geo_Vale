"""Consulta limitada à camada estadual oficial e cache temporário em memória."""

import json
import threading
import time
from copy import deepcopy
from datetime import datetime, timezone
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from shapely import get_parts, make_valid, union_all
from shapely.geometry import mapping, shape

CAMADA_MG = 'IDE:ide_1101_mg_unidade_federacao_pol'
URL_LIMITE = 'https://geoserver.meioambiente.mg.gov.br/ows?' + urlencode({
    'service': 'WFS', 'version': '2.0.0', 'request': 'GetFeature',
    'typeNames': CAMADA_MG, 'outputFormat': 'application/json',
    'srsName': 'EPSG:4326', 'count': 1,
})
METADADO_MG = ('https://idesisema.meioambiente.mg.gov.br/geonetwork/srv/por/'
               'catalog.search#/metadata/ce121547-8e95-4cc0-a6b9-e12a59c74f28')
LIMITE_BYTES = 6 * 1024 * 1024


class FonteIndisponivel(Exception):
    """Uma fonte geográfica não entregou dados utilizáveis."""


def consultar_fonte():
    """Obtém somente uma feição estadual, com timeout e tamanho limitados."""
    pedido = Request(URL_LIMITE, headers={
        'Accept': 'application/json', 'User-Agent': 'GeoVale/3.3 (consulta territorial)',
    })
    with urlopen(pedido, timeout=15) as resposta:
        conteudo = resposta.read(LIMITE_BYTES + 1)
    if len(conteudo) > LIMITE_BYTES:
        raise FonteIndisponivel('Resposta da fonte excede o tamanho permitido.')
    return json.loads(conteudo)


def preparar_limite(documento):
    """Confere identidade, posição e geometria e simplifica apenas para exibição."""
    if documento.get('type') != 'FeatureCollection' or len(documento.get('features', [])) != 1:
        raise FonteIndisponivel('Quantidade ou tipo de feições inesperado.')
    feicao = documento['features'][0]
    if str(feicao.get('properties', {}).get('geocodigo')) != '31':
        raise FonteIndisponivel('A fonte não identificou Minas Gerais.')
    crs = documento.get('crs', {}).get('properties', {}).get('name', '')
    if crs and not crs.endswith(('4326', 'CRS84')):
        raise FonteIndisponivel('Referência espacial inesperada.')
    geometria = shape(feicao['geometry'])
    if geometria.geom_type not in ('Polygon', 'MultiPolygon') or geometria.is_empty:
        raise FonteIndisponivel('Geometria estadual inválida.')
    oeste, sul, leste, norte = geometria.bounds
    if not (-52 < oeste < -49 and -24 < sul < -22 and -41 < leste < -39 and -15 < norte < -13):
        raise FonteIndisponivel('Extensão estadual inesperada.')
    ajustada = not geometria.is_valid
    if ajustada:
        partes = [parte for parte in get_parts(make_valid(geometria))
                  if parte.geom_type in ('Polygon', 'MultiPolygon')]
        geometria = union_all(partes)
    exibicao = geometria.simplify(0.001, preserve_topology=True)
    if exibicao.is_empty or not exibicao.is_valid or exibicao.geom_type not in ('Polygon', 'MultiPolygon'):
        raise FonteIndisponivel('Não foi possível preparar o contorno para exibição.')
    return {
        'type': 'FeatureCollection',
        'features': [{
            'type': 'Feature', 'properties': {'nome': 'Minas Gerais', 'codigo_uf': '31'},
            'geometry': mapping(exibicao),
        }],
        'fonte': {
            'nome': 'IDE-Sisema', 'camada': CAMADA_MG, 'url': URL_LIMITE,
            'metadado': METADADO_MG, 'crs': 'EPSG:4326',
            'consultado_em': datetime.now(timezone.utc).isoformat(),
            'simplificacao_graus': 0.001,
            'ajuste_topologico_visual': ajustada,
        },
        'aviso': None,
    }


class LimiteEstadual:
    """Compartilha a última resposta válida por uma hora, sem download estadual em lote."""

    def __init__(self, consultar=consultar_fonte, relogio=time.monotonic):
        self._consultar = consultar
        self._relogio = relogio
        self._trava = threading.Lock()
        self._dados = None
        self._validade = 0.0

    def obter(self):
        """Consulta a API quando necessário e preserva o contorno válido em falha temporária."""
        with self._trava:
            agora = self._relogio()
            if self._dados is not None and agora < self._validade:
                return deepcopy(self._dados)
            try:
                novos = preparar_limite(self._consultar())
            except Exception as erro:
                if self._dados is None:
                    raise FonteIndisponivel('Não foi possível consultar o limite estadual.') from erro
                dados = deepcopy(self._dados)
                dados['aviso'] = 'Exibindo o último contorno disponível. A fonte está temporariamente indisponível.'
                return dados
            self._dados = novos
            self._validade = agora + 3600
            return deepcopy(novos)
