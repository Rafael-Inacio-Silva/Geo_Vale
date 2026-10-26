"""Consulta cadastral de processos da ANM, sem inferir operação ou perímetro físico da mina."""

from copy import deepcopy
from datetime import datetime, timezone
import json
import math
from threading import Lock
from time import monotonic
from urllib.parse import urlencode
from urllib.request import urlopen
from geovale.area import validar_area
from geovale.mapa import FonteIndisponivel

SERVICO = 'https://geo.anm.gov.br/arcgis/rest/services/SIGMINE/dados_anm/MapServer/0'


def consultar_processo(numero, ano):
    """Consulta o serviço fixo com identidade numérica do catálogo e saída em WGS84."""
    parametros = {
        'where': f'NUMERO = {numero} AND ANO = {ano}',
        'outFields': 'PROCESSO,NUMERO,ANO,NOME,FASE,AREA_HA,SUBS,UF,DSProcesso',
        'returnGeometry': 'true', 'returnZ': 'false', 'outSR': '4326',
        'resultRecordCount': '2', 'f': 'geojson',
    }
    with urlopen(SERVICO + '/query?' + urlencode(parametros), timeout=15) as resposta:
        bruto = resposta.read(2 * 1024 * 1024 + 1)
    if len(bruto) > 2 * 1024 * 1024:
        raise FonteIndisponivel()
    return json.loads(bruto)


def preparar_processo(documento, numero, ano):
    """Confere identidade, atributos e polígono simples suportado, sem reparo ou simplificação."""
    try:
        if documento.get('type') != 'FeatureCollection' or documento.get('exceededTransferLimit'):
            raise ValueError()
        feicoes = documento['features']
        if not isinstance(feicoes, list) or len(feicoes) != 1:
            raise ValueError()
        feicao = feicoes[0]
        propriedades = feicao['properties']
        if feicao['type'] != 'Feature' or type(propriedades['NUMERO']) is not int or type(propriedades['ANO']) is not int:
            raise ValueError()
        if propriedades['NUMERO'] != numero or propriedades['ANO'] != ano or propriedades['UF'] != 'MG':
            raise ValueError()
        if (documento.get('properties') or {}).get('exceededTransferLimit'):
            raise ValueError()
        if 'crs' in documento and documento['crs'].get('properties', {}).get('name') not in ('EPSG:4326', 'urn:ogc:def:crs:OGC:1.3:CRS84', 'urn:ogc:def:crs:EPSG::4326'):
            raise ValueError()
        campos = {}
        for origem, destino in (('NOME', 'titular'), ('FASE', 'fase'), ('SUBS', 'substancia')):
            texto = propriedades[origem]
            if not isinstance(texto, str) or not texto.strip() or len(texto) > 254:
                raise ValueError()
            campos[destino] = texto.strip()
        area = propriedades['AREA_HA']
        if type(area) not in (int, float) or not 0 < area < 1000000 or not math.isfinite(area):
            raise ValueError()
        desenho = validar_area(feicao)
        if any(not (-51.3 <= x <= -38.7 and -23.5 <= y <= -14) for x, y in desenho['geometry']['coordinates'][0]):
            raise ValueError()
        desenho['properties'].update(campos)
        desenho['properties'].update({
            'origem': 'processo_anm', 'processo': f'{numero:06d}'[:3] + '.' + f'{numero:06d}'[3:] + f'/{ano}',
            'numero': numero, 'ano': ano, 'area_ha': area, 'uf': 'MG',
        })
        return desenho
    except (ValueError, KeyError, TypeError, AttributeError, OverflowError):
        raise FonteIndisponivel() from None


class ProcessosANM:
    """Mantém respostas conferidas em memória por dez minutos, sem salvar arquivos."""

    def __init__(self, consultar=consultar_processo, relogio=monotonic):
        self.consultar = consultar
        self.relogio = relogio
        self.cache = {}
        self.trava = Lock()

    def obter(self, numero, ano):
        """Retorna somente o processo associado à mina pelo catálogo local."""
        if type(numero) is not int or type(ano) is not int or not 1 <= numero <= 999999 or not 1900 <= ano <= 2100:
            raise FonteIndisponivel()
        chave = (numero, ano)
        with self.trava:
            anterior = self.cache.get(chave)
            if anterior and self.relogio() - anterior[0] < 600:
                return deepcopy(anterior[1])
            try:
                dados = preparar_processo(self.consultar(numero, ano), numero, ano)
            except Exception:
                raise FonteIndisponivel() from None
            dados['fonte'] = {'nome': 'Agência Nacional de Mineração — SIGMINE', 'url': SERVICO, 'consultado_em': datetime.now(timezone.utc).isoformat(), 'crs': 'EPSG:4326'}
            self.cache[chave] = (self.relogio(), dados)
            return deepcopy(dados)
