"""Monta o recorte de uma mina sem estudo de influência público: faixa declarada em volta do contorno OSM da cava.

    PYTHONPATH=backend .venv-geovale/bin/python ferramentas/preparar_faixa.py <mina_id> <osm_way> [distancia_m]

Baixa o way pela API do OpenStreetMap, guarda o snapshot com hash e gera dados/influencias/<mina_id>.geojson
com as duas Features esperadas pela API: `mina` (contorno OSM) e `influencia` (faixa medida em SIRGAS 2000 / UTM 23S).
"""
import hashlib
import json
import sys
from datetime import date
from pathlib import Path
from urllib.request import Request, urlopen

from rasterio.warp import transform_geom
from shapely.geometry import Polygon, mapping, shape
from shapely import orient_polygons

RAIZ = Path(__file__).resolve().parents[1]
UTM = 'EPSG:31983'
CONAMA = 'https://assiste.icmbio.gov.br/cepsul/images/stories/legislacao/Resolucao/2010/res_conama_428-2010_licenc_amb_uc.pdf'


def baixar_way(numero):
    url = f'https://api.openstreetmap.org/api/0.6/way/{numero}/full.json'
    with urlopen(Request(url, headers={'User-Agent': 'GeoVale/4.7'}), timeout=30) as resposta:
        bruto = resposta.read()
    elementos = json.loads(bruto)['elements']
    nos = {e['id']: (e['lon'], e['lat']) for e in elementos if e['type'] == 'node'}
    way = next(e for e in elementos if e['type'] == 'way' and e['id'] == numero)
    poligono = Polygon([nos[n] for n in way['nodes']])
    if way['nodes'][0] != way['nodes'][-1] or not poligono.is_valid or way['tags'].get('landuse') != 'quarry':
        raise ValueError('Way OSM não é um contorno de cava válido')
    fonte = {'osm_type': 'way', 'osm_id': numero, 'osm_version': way['version'], 'osm_timestamp': way['timestamp'], 'tags': way['tags'],
             'url': f'https://www.openstreetmap.org/way/{numero}', 'api_url': url, 'consultado_em': date.today().isoformat(),
             'licenca': 'ODbL 1.0', 'licenca_url': 'https://www.openstreetmap.org/copyright', 'sha256_resposta': hashlib.sha256(bruto).hexdigest()}
    return poligono, fonte


def arredondar(geometria):
    return json.loads(json.dumps(geometria), parse_float=lambda v: round(float(v), 7))


def preparar(mina_id, numero, distancia):
    cava, fonte_osm = baixar_way(numero)
    utm = shape(transform_geom('EPSG:4326', UTM, mapping(cava)))
    faixa = shape(transform_geom(UTM, 'EPSG:4326', mapping(utm.buffer(distancia, quad_segs=16))))
    nome = fonte_osm['tags'].get('name', mina_id)
    km = f'{distancia / 1000:g}'.replace('.', ',')
    pacote = {
        'type': 'FeatureCollection', 'mina_id': mina_id,
        'fonte': {
            'titulo': f'Faixa de {km} km em volta da cava (OSM way {numero})',
            'url': fonte_osm['url'], 'distancia_m': distancia, 'preparado_em': date.today().isoformat(),
            'crs_original': UTM, 'crs_saida': 'EPSG:4326',
            'referencia': {'titulo': 'Resolução CONAMA nº 428/2010, art. 1º, § 2º (regra transitória): faixa de 3 mil metros usada como entorno de influência de empreendimentos sobre unidades de conservação sem zona de amortecimento; aqui, só como escala de referência',
                           'url': CONAMA},
            'metodo': f'Buffer de {distancia} m do contorno OSM da cava, medido em SIRGAS 2000 / UTM 23S. Não foi localizado estudo público com área de influência desta mina.',
            'recorte_curto': f'faixa de {km} km em volta da cava',
            'origem_texto': f'Faixa declarada de {km} km em volta da cava — sem estudo público de influência',
            'credito': 'faixa declarada do GeoVale',
            'aviso': f'Recorte comum aproximado do MVP: faixa de {km} km em volta do contorno colaborativo OpenStreetMap da cava. '
                     'Não é área de influência de estudo ambiental nem limite de recuperação ou fechamento.'},
        'features': [
            {'type': 'Feature', 'geometry': arredondar(mapping(orient_polygons(faixa))),
             'properties': {'id': 'influencia', 'identificador_original': f'faixa_{distancia}m', 'tipo': 'influencia', 'nome': 'Área de influência · recorte do MVP',
                            'cor': '#e9a000', 'origem': 'faixa_declarada', 'aproximada': True, 'finalidade': 'caracterizacao_territorial_mvp'}},
            {'type': 'Feature', 'geometry': arredondar(mapping(cava)),
             'properties': {'id': 'mina', 'identificador_original': f'mina_{mina_id}', 'nome': f'Área de mineração {nome} · OSM', 'cor': '#00594f',
                            'tipo': 'mina', 'origem': 'referencia_osm', 'aproximada': True, 'finalidade': 'contexto_cartografico', 'fonte': fonte_osm}},
        ],
    }
    destino = RAIZ / 'dados/influencias' / f'{mina_id}.geojson'
    destino.write_text(json.dumps(pacote, ensure_ascii=False, indent=1), encoding='utf-8')
    print(destino.name, f'{utm.area / 1e4:.1f} ha de cava,', f'{utm.buffer(distancia, quad_segs=16).area / 1e4:.0f} ha de recorte; centro', cava.centroid.coords[0])


if __name__ == '__main__':
    preparar(sys.argv[1], int(sys.argv[2]), float(sys.argv[3]) if len(sys.argv) > 3 else 3000.0)
