"""Lê referência vetorial OSM e influências digitalizadas locais, sem consulta externa."""
import json
from shapely.geometry import shape

IDENTIDADES = {'mina_horizontes', 'ada_unificada', 'aid_hidrogeologia', 'aid_agua_solos', 'aii_agua_solos'}


def ler_referencias(caminho):
    """Confere o pacote versionado sem reparar geometria na entrega ao navegador."""
    dados = json.loads(caminho.read_text(encoding='utf-8'))
    if dados['type'] != 'FeatureCollection' or dados['mina_id'] != 'horizontes':
        raise ValueError('Referências incompatíveis')
    if len(dados['features']) != 5 or {f['properties']['id'] for f in dados['features']} != IDENTIDADES:
        raise ValueError('Referências incompletas')
    for feicao in dados['features']:
        geometria = shape(feicao['geometry'])
        p = feicao['properties']
        if feicao['type'] != 'Feature' or p['origem'] != ('referencia_osm' if p['id'] == 'mina_horizontes' else 'referencia_documental') or p['aproximada'] is not True:
            raise ValueError('Procedência incompatível')
        if geometria.geom_type not in ('Polygon', 'MultiPolygon') or geometria.is_empty or not geometria.is_valid:
            raise ValueError('Contorno inválido')
        x0, y0, x1, y1 = geometria.bounds
        if not (-44.1 < x0 < x1 < -43.7 and -20.4 < y0 < y1 < -19.9):
            raise ValueError('Extensão incompatível')
        if p['id'] == 'mina_horizontes' and (geometria.geom_type != 'Polygon' or len(geometria.interiors) or len(geometria.exterior.coords) > 501):
            raise ValueError('Referência não editável')
    if dados['fonte']['crs_saida'] != 'EPSG:4326' or not dados['fonte']['sha256_pdf']:
        raise ValueError('Fonte incompleta')
    return dados
