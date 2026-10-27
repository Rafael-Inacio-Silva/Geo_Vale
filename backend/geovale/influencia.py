"""Lê o único recorte de caracterização e a mina sombreada, com evidência local."""
import json
from shapely.geometry import shape


def ler_influencia(caminho, mina_id):
    """Confere identidade, procedência e contornos sem reparar ou redefinir limites."""
    dados = json.loads(caminho.read_text(encoding='utf-8'))
    if dados['type'] != 'FeatureCollection' or dados['mina_id'] != mina_id:
        raise ValueError('Influência incompatível')
    if len(dados['features']) != 2 or {f['properties']['id'] for f in dados['features']} != {'mina', 'influencia'}:
        raise ValueError('Pacote de influência incompleto')
    for feicao in dados['features']:
        p = feicao['properties']
        geom = shape(feicao['geometry'])
        origem = 'referencia_osm' if p['id'] == 'mina' else 'referencia_documental'
        if feicao['type'] != 'Feature' or p['origem'] != origem or p['aproximada'] is not True:
            raise ValueError('Procedência incompatível')
        if geom.geom_type not in ('Polygon', 'MultiPolygon') or geom.is_empty or not geom.is_valid:
            raise ValueError('Contorno inválido')
        x0, y0, x1, y1 = geom.bounds
        if not (-180 <= x0 < x1 <= 180 and -85 <= y0 < y1 <= 85):
            raise ValueError('Extensão incompatível')
    if dados['fonte']['crs_saida'] != 'EPSG:4326' or not dados['fonte']['sha256_pdf']:
        raise ValueError('Evidência incompleta')
    return dados
