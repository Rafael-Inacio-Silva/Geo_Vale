"""Reproduz o contorno externo de influência e o sombreado OSM a partir das evidências locais."""
import json
import math
from pathlib import Path
from shapely.geometry import Polygon, mapping, shape
from shapely import orient_polygons

RAIZ = Path(__file__).resolve().parents[1]

def converter_utm(leste,norte):
 """Converte UTM 23S/GRS80 em longitude e latitude para a visualização aproximada."""
 a=6378137.; f=1/298.257222101; e2=f*(2-f); ep=e2/(1-e2); k=.9996
 x=leste-500000; m=(norte-10000000)/k
 mu=m/(a*(1-e2/4-3*e2**2/64-5*e2**3/256)); e1=(1-math.sqrt(1-e2))/(1+math.sqrt(1-e2))
 p=mu+(3*e1/2-27*e1**3/32)*math.sin(2*mu)+(21*e1**2/16-55*e1**4/32)*math.sin(4*mu)+(151*e1**3/96)*math.sin(6*mu)+(1097*e1**4/512)*math.sin(8*mu)
 n=a/math.sqrt(1-e2*math.sin(p)**2); t=math.tan(p)**2; c=ep*math.cos(p)**2; r=a*(1-e2)/(1-e2*math.sin(p)**2)**1.5; d=x/(n*k)
 lat=p-(n*math.tan(p)/r)*(d*d/2-(5+3*t+10*c-4*c*c-9*ep)*d**4/24+(61+90*t+298*c+45*t*t-252*ep-3*c*c)*d**6/720)
 lon=math.radians(-45)+(d-(1+2*t+c)*d**3/6+(5-2*c+28*t-3*c*c+8*ep+24*t*t)*d**5/120)/math.cos(p)
 return [round(math.degrees(lon),7),round(math.degrees(lat),7)]

def preparar():
    """Transforma a grade SIRGAS 2000 / UTM 23S em longitude/latitude e confere contornos."""
    pasta = RAIZ / 'dados/influencias'
    receita = json.loads((pasta / 'digitalizacao.json').read_text())
    pacote = json.loads((pasta / 'horizontes.geojson').read_text())
    osm = json.loads((pasta / 'mineracao-osm.geojson').read_text())
    if osm['properties']['osm_id'] != 315221699 or not shape(osm['geometry']).is_valid:
        raise ValueError('Referência OSM incompatível')
    referencia = {
        'type': 'Feature', 'geometry': osm['geometry'],
        'properties': {'id': 'mina', 'identificador_original': 'mina_horizontes', 'nome': 'Área de mineração Horizontes · OSM',
            'cor': '#00594f', 'tipo': 'mina', 'origem': 'referencia_osm', 'aproximada': True,
            'finalidade': 'contexto_cartografico',
            'fonte': osm['properties']},
    }
    feicoes = [referencia]
    for chave, traco in receita['tracos'].items():
        grade = receita['grade'][str(traco['pagina_pdf'])]
        def projetar(ponto):
            """Interpola a grade lida em pixels antes da conversão geográfica."""
            (x0, e0), (x1, e1) = grade['x']
            (y0, n0), (y1, n1) = grade['y']
            return converter_utm(e0 + (ponto[0]-x0)*(e1-e0)/(x1-x0), n0 + (ponto[1]-y0)*(n1-n0)/(y1-y0))
        poligono = Polygon([projetar(p) for p in traco['pontos']])
        if poligono.geom_type not in ('Polygon', 'MultiPolygon') or not poligono.is_valid:
            raise ValueError(f'Geometria incompatível: {chave}')
        propriedades = {k: v for k, v in traco.items() if k != 'pontos'}
        propriedades.update(id='influencia', identificador_original=chave, tipo='influencia', nome='Área de influência · recorte do MVP', origem='referencia_documental', aproximada=True,
            finalidade='caracterizacao_territorial_mvp')
        feicoes.append({'type': 'Feature', 'properties': propriedades, 'geometry': mapping(orient_polygons(poligono))})
    pacote['features'] = feicoes
    (pasta / 'horizontes.geojson').write_text(json.dumps(pacote, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    preparar()
