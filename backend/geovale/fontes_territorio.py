"""Obtém atributos vetoriais completos e células matriciais no recorte comum do MVP."""
import hashlib
import json
import math
import re
import xml.etree.ElementTree as ET
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import numpy as np
from rasterio.features import geometry_mask
from rasterio.io import MemoryFile
from rasterio.warp import transform_bounds, transform_geom
from shapely import force_2d, get_coordinates, union_all
from shapely.geometry import mapping, shape

from geovale.camadas import SERVICO_WMS
from geovale.mapa import FonteIndisponivel
from geovale.trilhas import SERVICO as SERVICO_TRILHAS
from geovale.geometria import partes_da_dimensao

MAX_BYTES = 32 * 1024 * 1024
MAX_REGISTROS = 2000
MAX_CELULAS = 4_000_000


def consultar(url, parametros, limite=MAX_BYTES):
    """Lê serviços públicos definidos pelo catálogo interno com prazo e tamanho limitados."""
    pedido = Request(url + '?' + urlencode(parametros, doseq=True), headers={
        'User-Agent': 'GeoVale/4.0 (caracterizacao territorial)', 'Accept': '*/*',
    })
    with urlopen(pedido, timeout=25) as resposta:
        bruto = resposta.read(limite + 1)
    if len(bruto) > limite:
        raise FonteIndisponivel('O recorte excede o tamanho permitido.')
    return bruto


def ler_json(bruto):
    """Rejeita números não finitos ou estrutura inesperada na fonte."""
    dados = json.loads(bruto, parse_constant=lambda valor: (_ for _ in ()).throw(ValueError(valor)))
    if not isinstance(dados, dict):
        raise FonteIndisponivel('Resposta de dados incompatível.')
    return dados


def recortar_vetores(documento, recorte, tipos, campos, z_zero=False):
    """Preserva todos os atributos publicados e recorta cada registro sem duplicar sua contagem.

    `z_zero` aceita somente cota publicada exatamente igual a zero, removida antes da validação; outra cota falha.
    """
    if documento.get('type') != 'FeatureCollection' or not isinstance(documento.get('features'), list):
        raise FonteIndisponivel('Coleção vetorial inválida.')
    saida, ids = [], set()
    for f in documento['features']:
        identidade = f.get('id')
        if f.get('type') != 'Feature' or type(identidade) not in (str, int) or str(identidade) in ids:
            raise FonteIndisponivel('Registro sem identidade única.')
        ids.add(str(identidade))
        props = f.get('properties')
        if not isinstance(props, dict) or set(props) != set(campos):
            raise FonteIndisponivel('Os atributos recebidos não correspondem ao esquema completo.')
        geom = shape(f['geometry'])
        if z_zero and geom.has_z and not get_coordinates(geom, include_z=True)[:, 2].any():
            geom = force_2d(geom)
        if geom.geom_type not in tipos or geom.is_empty or not geom.is_valid or geom.has_z:
            raise FonteIndisponivel('Geometria inválida; nenhum reparo automático foi aplicado.')
        x0, y0, x1, y1 = geom.bounds
        if not (-180 <= x0 <= x1 <= 180 and -85 <= y0 <= y1 <= 85):
            raise FonteIndisponivel('Coordenadas incompatíveis.')
        cortada = union_all(partes_da_dimensao(geom.intersection(recorte), tipos))
        if cortada.is_empty:
            continue
        if not cortada.is_valid or cortada.geom_type not in tipos:
            raise FonteIndisponivel('Interseção vetorial inválida.')
        saida.append({'type': 'Feature', 'id': identidade, 'properties': props, 'geometry': mapping(cortada)})
    saida.sort(key=lambda f: str(f['id']))
    return saida


def esquema_wfs(bruto):
    """Descobre o campo geométrico e todos os atributos diretamente do DescribeFeatureType."""
    raiz = ET.fromstring(bruto)
    sequencia = raiz.find('.//{http://www.w3.org/2001/XMLSchema}sequence')
    if sequencia is None:
        raise FonteIndisponivel('Esquema WFS indisponível.')
    campos = [dict(v.attrib) for v in sequencia]
    geometrias = [v for v in campos if v.get('type', '').startswith('gml:')]
    if len(geometrias) != 1:
        raise FonteIndisponivel('Campo geométrico ambíguo.')
    g = geometrias[0]
    if not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*', g['name']):
        raise FonteIndisponivel('Nome de campo inválido.')
    tipo = g['type']
    tipos = ('Polygon', 'MultiPolygon') if any(v in tipo for v in ('Surface', 'Polygon')) else ('LineString', 'MultiLineString') if any(v in tipo for v in ('Curve', 'Line')) else ('Point', 'MultiPoint') if 'Point' in tipo else ()
    if not tipos:
        raise FonteIndisponivel('Tipo vetorial não suportado.')
    return g['name'], tipos, [c for c in campos if c is not g]


def obter_wfs(base, recorte):
    """Consulta todos os campos por WFS, verificando que o retorno não foi truncado."""
    esquema = consultar(SERVICO_WMS, {'service': 'WFS', 'version': '2.0.0', 'request': 'DescribeFeatureType', 'typeNames': base['camada']}, 1024 * 1024)
    geometria, tipos, campos = esquema_wfs(esquema)
    bruto = consultar(SERVICO_WMS, {
        'service': 'WFS', 'version': '2.0.0', 'request': 'GetFeature', 'typeNames': base['camada'],
        'outputFormat': 'application/json', 'srsName': 'EPSG:4326', 'count': MAX_REGISTROS + 1,
        'CQL_FILTER': f"BBOX({geometria},{','.join(map(str, recorte.bounds))},'EPSG:4326')",
    })
    dados = ler_json(bruto)
    n, devolvidos = dados.get('numberMatched'), dados.get('numberReturned')
    if (type(n) is not int or type(devolvidos) is not int or not 0 <= n <= MAX_REGISTROS
            or n != devolvidos or n != len(dados.get('features', []))):
        raise FonteIndisponivel('Resposta vetorial incompleta ou excede o limite de registros.')
    crs = dados.get('crs', {}).get('properties', {}).get('name')
    if crs not in ('urn:ogc:def:crs:EPSG::4326', 'EPSG:4326', 'urn:ogc:def:crs:OGC:1.3:CRS84'):
        raise FonteIndisponivel('CRS vetorial incompatível.')
    # Campo publicado só no GeoJSON é aceito apenas quando declarado no catálogo.
    extras = [e for e in base.get('campos_extras', []) if e not in {c['name'] for c in campos}]
    campos = campos + [{'name': e, 'origem': 'GeoJSON do serviço; ausente do DescribeFeatureType'} for e in extras]
    registros = recortar_vetores(dados, recorte, tipos, [c['name'] for c in campos], z_zero=base.get('z_zero', False))
    aviso = 'Atributos preservados da fonte. Áreas, comprimentos e datas cadastrais não foram recalculados para o recorte.'
    if base.get('z_zero'):
        aviso += ' Cota publicada igual a zero removida; geometria tratada em 2D.'
    return {'tipo': 'vetor', 'quantidade': len(registros), 'registros_consultados': n,
            'campos': campos, 'dados': {'type': 'FeatureCollection', 'features': registros},
            'sha256_resposta': hashlib.sha256(bruto).hexdigest(), 'servico': 'WFS 2.0.0',
            'crs': 'EPSG:4326', 'aviso': aviso}, None


def obter_trilhas(base, recorte):
    """Consulta todos os campos municipais e confere IDs/contagem antes da interseção."""
    metadados = ler_json(consultar(SERVICO_TRILHAS, {'f': 'json'}, 1024 * 1024))
    campos = metadados['fields']
    oid = metadados['objectIdField']
    parametros = {'f': 'json', 'where': '1=1', 'geometry': ','.join(map(str, recorte.bounds)),
                  'geometryType': 'esriGeometryEnvelope', 'inSR': '4326', 'spatialRel': 'esriSpatialRelIntersects'}
    contagem = ler_json(consultar(SERVICO_TRILHAS + '/query', {**parametros, 'returnCountOnly': 'true'}, 1024 * 1024))
    n = contagem.get('count')
    if type(n) is not int or not 0 <= n <= MAX_REGISTROS:
        raise FonteIndisponivel('Contagem municipal inválida.')
    bruto = consultar(SERVICO_TRILHAS + '/query', {**parametros, 'f': 'geojson', 'outFields': '*',
        'outSR': '4326', 'returnGeometry': 'true', 'resultRecordCount': MAX_REGISTROS + 1, 'orderByFields': oid})
    dados = ler_json(bruto)
    if (dados.get('exceededTransferLimit') or (dados.get('properties') or {}).get('exceededTransferLimit')
            or n != len(dados.get('features', []))):
        raise FonteIndisponivel('Resposta municipal incompleta.')
    ids = []
    for f in dados.get('features', []):
        id_fonte = f.get('properties', {}).get(oid)
        if type(id_fonte) is not int:
            raise FonteIndisponivel('Identidade municipal inválida.')
        f['id'] = id_fonte
        ids.append(id_fonte)
    # GeoJSON ArcGIS publica os campos do objeto; não se omitem campos do esquema.
    registros = recortar_vetores(dados, recorte, ('LineString', 'MultiLineString'), [c['name'] for c in campos])
    return {'tipo': 'vetor', 'quantidade': len(registros), 'registros_consultados': n,
            'campos': campos, 'dados': {'type': 'FeatureCollection', 'features': registros},
            'sha256_resposta': hashlib.sha256(bruto).hexdigest(), 'servico': 'ArcGIS REST',
            'crs': 'EPSG:4326', 'edicao_fonte': metadados.get('editingInfo'),
            'aviso': 'Cadastro municipal de trilhas; não comprova permissão de acesso ou segurança. Atributos publicados conservados.'}, None


def ler_legenda(bruto):
    """Utiliza somente o estilo padrão oficial, preservando códigos, cores e rótulos."""
    raiz = ET.fromstring(bruto)
    estilos = raiz.findall('.//{http://www.opengis.net/sld}UserStyle')
    padroes = [e for e in estilos if e.findtext('{http://www.opengis.net/sld}IsDefault') in ('1', 'true')]
    estilo = padroes[0] if len(padroes) == 1 else estilos[0] if len(estilos) == 1 else None
    if estilo is None:
        raise FonteIndisponivel('Estilo matricial padrão ambíguo.')
    legenda = {}
    for entrada in estilo.iter():
        if not entrada.tag.endswith('ColorMapEntry'):
            continue
        codigo = float(entrada.attrib['quantity'])
        cor = entrada.attrib.get('color', '')
        if not codigo.is_integer() or int(codigo) in legenda or not re.fullmatch(r'#[0-9a-fA-F]{6}', cor):
            raise FonteIndisponivel('Legenda matricial inválida.')
        legenda[int(codigo)] = {'codigo': int(codigo), 'nome': entrada.attrib.get('label', '').strip(), 'cor': cor}
    if not legenda:
        raise FonteIndisponivel('Legenda matricial vazia.')
    return legenda


def recortar_raster(bruto, recorte, legenda):
    """Retém todas as células cujo centro está no recorte, na grade nativa e sem reamostragem."""
    with MemoryFile(bruto) as memoria, memoria.open() as origem:
        if origem.driver != 'GTiff' or origem.count != 1 or origem.width * origem.height > MAX_CELULAS:
            raise FonteIndisponivel('Cobertura matricial excede o limite ou formato esperado.')
        if origem.crs is None or origem.nodata != 0 or origem.dtypes[0] != 'uint8':
            raise FonteIndisponivel('CRS ou banda categórica incompatível.')
        if origem.crs.to_epsg() != 4674:
            raise FonteIndisponivel('A cobertura não manteve a grade nativa SIRGAS 2000.')
        geom = transform_geom('EPSG:4326', origem.crs, mapping(recorte))
        x0, y0, x1, y1 = shape(geom).bounds
        b = origem.bounds
        if not (b.left <= x0 < x1 <= b.right and b.bottom <= y0 < y1 <= b.top):
            raise FonteIndisponivel('A cobertura recebida não cobre o recorte completo.')
        dentro = geometry_mask([geom], origem.shape, origem.transform, all_touched=False, invert=True)
        valores = origem.read(1)
        validos = dentro & (origem.read_masks(1) != 0)
        codigos, contagens = np.unique(valores[validos], return_counts=True)
        total = int(validos.sum())
        classes = []
        for codigo, quantidade in zip(codigos, contagens):
            codigo = int(codigo)
            if codigo not in legenda:
                raise FonteIndisponivel('A fonte retornou classe ausente na legenda oficial.')
            classes.append({**legenda[codigo], 'celulas': int(quantidade), 'percentual_celulas_validas': round(int(quantidade) * 100 / total, 4)})
        perfil = origem.profile.copy()
        perfil.update(driver='GTiff', compress='deflate', nodata=0)
        tags, tags_banda = origem.tags(), origem.tags(1)
        recortados = valores.copy()
        recortados[~validos] = 0
        with MemoryFile() as destino:
            with destino.open(**perfil) as arquivo:
                arquivo.write(recortados, 1)
                arquivo.write_mask(validos.astype('uint8') * 255)
                arquivo.update_tags(**tags)
                arquivo.update_tags(1, **tags_banda)
            artefato = destino.read()
        resultado = {'tipo': 'raster', 'quantidade': total, 'classes': classes,
                     'celulas_no_recorte': int(dentro.sum()), 'celulas_sem_dados': int((dentro & ~validos).sum()),
                     'crs': origem.crs.to_string(), 'resolucao': list(origem.res), 'dimensoes': list(origem.shape),
                     'transformacao': list(origem.transform), 'limites': list(origem.bounds),
                     'tags': tags, 'tags_banda': tags_banda, 'dtype': origem.dtypes[0], 'nodata': origem.nodata,
                     'unidades_publicadas': list(origem.units), 'descricao_bandas': list(origem.descriptions),
                     'aviso': 'Células selecionadas pelo centro na grade nativa. Percentuais de células válidas, não percentuais de área. Sem avaliação da condição atual da cava.'}
        return resultado, artefato


def obter_wcs(base, recorte):
    """Obtém cobertura categórica nativa com margem de dois pixels e sua legenda padrão."""
    cobertura = base['camada'].replace(':', '__')
    descricao = consultar(SERVICO_WMS, {'service': 'WCS', 'version': '2.0.1', 'request': 'DescribeCoverage', 'coverageId': cobertura}, 1024 * 1024)
    raiz = ET.fromstring(descricao)
    envelope = raiz.find('.//{http://www.opengis.net/gml/3.2}Envelope')
    if envelope is None or envelope.attrib.get('axisLabels') != 'Lat Long' or not envelope.attrib.get('srsName', '').endswith('/4674'):
        raise FonteIndisponivel('Eixos ou CRS da cobertura incompatíveis.')
    vetores = raiz.findall('.//{http://www.opengis.net/gml/3.2}offsetVector')
    deslocamentos = [[float(v) for v in e.text.split()] for e in vetores]
    if len(deslocamentos) != 2 or not all(len(v) == 2 for v in deslocamentos):
        raise FonteIndisponivel('Grade matricial inválida.')
    res_y = max(abs(v[0]) for v in deslocamentos)
    res_x = max(abs(v[1]) for v in deslocamentos)
    if not all(math.isfinite(v) and 0 < v < .01 for v in (res_x, res_y)):
        raise FonteIndisponivel('Resolução matricial incompatível.')
    x0, y0, x1, y1 = transform_bounds('EPSG:4326', 'EPSG:4674', *recorte.bounds)
    if ((x1 - x0) / res_x + 6) * ((y1 - y0) / res_y + 6) > MAX_CELULAS:
        raise FonteIndisponivel('Recorte excede o limite de células.')
    bruto = consultar(SERVICO_WMS, {'service': 'WCS', 'version': '2.0.1', 'request': 'GetCoverage',
        'coverageId': cobertura, 'format': 'image/tiff',
        'subset': [f'Lat({y0 - 2 * res_y},{y1 + 2 * res_y})', f'Long({x0 - 2 * res_x},{x1 + 2 * res_x})']})
    estilo = consultar(SERVICO_WMS, {'service': 'WMS', 'version': '1.1.1', 'request': 'GetStyles', 'layers': base['camada']}, 1024 * 1024)
    resultado, artefato = recortar_raster(bruto, recorte, ler_legenda(estilo))
    if not np.allclose(resultado['resolucao'], [res_x, res_y], rtol=1e-6, atol=1e-12):
        raise FonteIndisponivel('Cobertura foi reamostrada de forma inesperada.')
    resultado.update(servico='WCS 2.0.1', sha256_resposta=hashlib.sha256(bruto).hexdigest(),
                     sha256_artefato=hashlib.sha256(artefato).hexdigest(), descricao_cobertura_xml=descricao.decode(), estilo_padrao_xml=estilo.decode())
    return resultado, artefato


def coletar_base(base, recorte):
    """Seleciona o adaptador declarativo do catálogo; a visibilidade no mapa não participa."""
    tipo = base['processamento']
    if tipo == 'wcs':
        return obter_wcs(base, recorte)
    if tipo == 'wfs':
        return obter_wfs(base, recorte)
    if tipo == 'arcgis':
        return obter_trilhas(base, recorte)
    raise FonteIndisponivel('Base sem adaptador de dados suportado.')
