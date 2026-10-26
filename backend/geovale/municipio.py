"""Limite municipal simplificado do IBGE, consultado somente para a mina selecionada."""
import gzip
import io
import json
import threading
import time
from copy import deepcopy
from datetime import datetime, timezone
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from shapely.geometry import shape
from geovale.mapa import FonteIndisponivel

SERVICO = 'https://servicodados.ibge.gov.br/api/v3/malhas/municipios/'
LIMITE_BYTES = 2 * 1024 * 1024


def consultar_municipio(codigo):
    """Solicita uma malha na maior qualidade da API simplificada, sem lote estadual."""
    url = SERVICO + codigo + '?' + urlencode({'formato': 'application/vnd.geo+json', 'qualidade': 'maxima'})
    pedido = Request(url, headers={'Accept': 'application/vnd.geo+json', 'User-Agent': 'GeoVale/3.3'})
    with urlopen(pedido, timeout=15) as resposta:
        bruto = resposta.read(LIMITE_BYTES + 1)
    if len(bruto) > LIMITE_BYTES:
        raise FonteIndisponivel('Limite municipal excede o tamanho permitido.')
    # O serviço pode entregar gzip mesmo sem Accept-Encoding.
    if bruto[:2] == b'\x1f\x8b':
        with gzip.GzipFile(fileobj=io.BytesIO(bruto)) as arquivo:
            bruto = arquivo.read(LIMITE_BYTES + 1)
    if len(bruto) > LIMITE_BYTES:
        raise FonteIndisponivel('Malha descompactada excede o tamanho permitido.')
    return json.loads(bruto)


def preparar_municipio(documento, codigo):
    """Confere identidade, topologia e posição sem corrigir ou inventar o limite."""
    if documento.get('type') != 'FeatureCollection' or len(documento.get('features', [])) != 1:
        raise FonteIndisponivel('Quantidade de municípios inesperada.')
    feicao = documento['features'][0]
    if str(feicao.get('properties', {}).get('codarea')) != codigo:
        raise FonteIndisponivel('Município diferente do catálogo.')
    crs = documento.get('crs', {}).get('properties', {}).get('name', '')
    if crs and not crs.endswith(('4326', 'CRS84')):
        raise FonteIndisponivel('Referência espacial inesperada.')
    geometria = shape(feicao['geometry'])
    if geometria.geom_type not in ('Polygon', 'MultiPolygon') or geometria.is_empty or not geometria.is_valid:
        raise FonteIndisponivel('Limite municipal inválido.')
    oeste, sul, leste, norte = geometria.bounds
    if not (-51.3 < oeste < leste < -38.7 and -23.5 < sul < norte < -14):
        raise FonteIndisponivel('Limite municipal fora de Minas Gerais.')
    return {
        'type': 'FeatureCollection',
        'features': [{'type': 'Feature', 'geometry': deepcopy(feicao['geometry']), 'properties': {'codigo_ibge': codigo}}],
        'fonte': {'nome': 'IBGE — API de malhas simplificadas', 'url': SERVICO + codigo,
                  'qualidade': 'maxima', 'ano_referencia': None,
                  'consultado_em': datetime.now(timezone.utc).isoformat()},
    }


class LimitesMunicipais:
    """Cache por código, em memória por uma hora, com falha explícita e sem persistência."""
    def __init__(self, consultar=consultar_municipio, relogio=time.monotonic):
        self._consultar = consultar
        self._relogio = relogio
        self._trava = threading.Lock()
        self._cache = {}

    def obter(self, codigo):
        if not isinstance(codigo, str) or len(codigo) != 7 or not codigo.isascii() or not codigo.isdigit() or not codigo.startswith('31'):
            raise FonteIndisponivel('Código municipal inválido.')
        with self._trava:
            agora = self._relogio()
            existente = self._cache.get(codigo)
            if existente and agora < existente[0]:
                return deepcopy(existente[1])
            try:
                dados = preparar_municipio(self._consultar(codigo), codigo)
            except Exception as erro:
                raise FonteIndisponivel('Não foi possível consultar o município.') from erro
            self._cache[codigo] = (agora + 3600, dados)
            return deepcopy(dados)
