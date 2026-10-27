"""Mapas temáticos do PDF a partir das geometrias e GeoTIFFs persistidos."""
import numpy as np
from PIL import Image
from rasterio.io import MemoryFile
from rasterio.transform import from_bounds
from rasterio.warp import reproject, transform_geom
from rasterio.enums import Resampling
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Flowable
from shapely.geometry import mapping, shape

CORES={'relevo':'#b06f36','agua':'#237bba','solos':'#a87554','vegetacao':'#538343','entorno':'#a44663','barragens':'#c8462b','trilhas':'#8a4fa0'}
ORDEM_VETORES={'solos':0,'vegetacao':1,'relevo':2,'entorno':3,'trilhas':4,'agua':5,'barragens':6}


class MapaTerritorial(Flowable):
    """Compõe somente dados do recorte; reprojeção matricial ocorre apenas na imagem de apresentação."""
    def __init__(self,dados,tema=None,altura=240,pontos=(),setores=()):
        super().__init__();self.width=511.27559055118115;self.height=altura;self.tema=tema;self.dados=dados;self.pontos=pontos
        self.setores=[(rotulo,transform_geom('EPSG:4326','EPSG:31983',g),cor) for rotulo,g,cor in setores]
        self.feicoes={f['properties']['id']:transform_geom('EPSG:4326','EPSG:31983',f['geometry']) for f in dados['influencia']['features']}
        minerada=dados.get('area_minerada')
        self.minerada=(transform_geom('EPSG:4326','EPSG:31983',minerada['geojson']),minerada['cor']) if minerada else None
        # A ficha simulada mostra só a drenagem enquadrada como referência dos pontos de água.
        self.bases=([b for b in dados['bases'] if 'enq_corpos' in b['base']['camada']] if tema=='tecnicos' else [] if tema=='sugestao'
                    else [b for b in dados['bases'] if tema is None or b['base']['tema_id']==tema])

    def draw(self):
        t=self.canv;t.saveState();t.setFillColor(colors.HexColor('#f3f6f2'));t.roundRect(0,0,self.width,self.height,8,fill=1,stroke=0)
        contorno=self.feicoes['influencia'];coords=contorno['coordinates']
        ps=[p for a in coords for p in a] if contorno['type']=='Polygon' else [p for pol in coords for a in pol for p in a]
        x0,y0=min(p[0] for p in ps),min(p[1] for p in ps);x1,y1=max(p[0] for p in ps),max(p[1] for p in ps)
        escala=min((self.width-65)/(x1-x0),(self.height-58)/(y1-y0));dx=(self.width-(x1-x0)*escala)/2;dy=36+(self.height-58-(y1-y0)*escala)/2
        def xy(ponto):return dx+(ponto[0]-x0)*escala,dy+(ponto[1]-y0)*escala
        def caminho(g):
            p=t.beginPath();tipo,c=g['type'],g['coordinates']
            partes=c if tipo=='MultiLineString' else [c] if tipo=='LineString' else [a for pol in c for a in pol] if tipo=='MultiPolygon' else c
            for linha in partes:
                for i,ponto in enumerate(linha):
                    x,y=xy(ponto)
                    if i==0:p.moveTo(x,y)
                    else:p.lineTo(x,y)
                if 'Polygon' in tipo:p.close()
            return p
        t.setFillColor(colors.HexColor('#fff0b8'));t.drawPath(caminho(contorno),fill=1,stroke=0,fillMode=0)
        t.saveState();t.clipPath(caminho(contorno),stroke=0,fill=0)
        for b in sorted(self.bases,key=lambda b:0 if b['base']['tema_id']=='relevo' else 1):
            if b['tipo']!='raster':continue
            bruto=self.dados.get('rasters',{}).get(b['base']['id'])
            if not bruto:continue
            # Grade de desenho limitada; dados de análise e contagens permanecem nativos.
            w=600;h=max(1,round(w*(y1-y0)/(x1-x0)));destino=np.zeros((h,w),dtype='uint8');trans=from_bounds(x0,y0,x1,y1,w,h)
            with MemoryFile(bruto) as m,m.open() as src:
                reproject(src.read(1),destino,src_transform=src.transform,src_crs=src.crs,src_nodata=0,
                          dst_transform=trans,dst_crs='EPSG:31983',dst_nodata=0,resampling=Resampling.nearest)
            rgba=np.zeros((h,w,4),dtype='uint8')
            for c in b.get('classes',[]):
                cor=c['cor'].lstrip('#');rgb=[int(cor[i:i+2],16) for i in (0,2,4)]
                rgba[destino==c['codigo']]=rgb+[100 if self.tema is None else 210]
            t.drawImage(ImageReader(Image.fromarray(rgba)),dx,dy,width=(x1-x0)*escala,height=(y1-y0)*escala,mask='auto')
        if self.minerada:
            g,cor=self.minerada;t.setStrokeColor(colors.HexColor(cor));t.setFillColor(colors.HexColor(cor));t.setLineWidth(.6)
            t.setFillAlpha(.2 if self.tema=='tecnicos' else 0);t.drawPath(caminho(g),fill=int(self.tema=='tecnicos'),stroke=1,fillMode=0);t.setFillAlpha(1)
        marcadores=[]
        for b in sorted(self.bases,key=lambda b:ORDEM_VETORES.get(b['base']['tema_id'],0)):
            if b['tipo']!='vetor':continue
            tema=b['base']['tema_id'];cor=colors.HexColor(CORES.get(tema,'#536d64'));t.setStrokeColor(cor);t.setFillColor(cor);t.setLineWidth(.65)
            for f in b['dados']['features']:
                g=transform_geom('EPSG:4326','EPSG:31983',f['geometry'])
                if 'Point' in g['type']:
                    # Rótulo curto igual ao prefixo publicado no nome (ex.: código SIGIBAR das barragens).
                    rotulo=str(f['properties'].get('name') or '').split(' - ')[0] if self.tema else ''
                    marcadores+=[(xy(p),cor,rotulo) for p in ([g['coordinates']] if g['type']=='Point' else g['coordinates'])];continue
                pol='Polygon' in g['type']
                # Simplificação de 3 m só no desenho (abaixo de 0,1 pt nesta escala); medidas usam a geometria guardada.
                t.setFillAlpha(.12 if self.tema is None else .22);t.drawPath(caminho(mapping(shape(g).simplify(3))),fill=int(pol),stroke=1,fillMode=0)
        for _,g,cor in self.setores:
            t.setFillColor(colors.HexColor(cor));t.setStrokeColor(colors.white);t.setLineWidth(.6);t.setFillAlpha(.75);t.drawPath(caminho(g),fill=1,stroke=1,fillMode=0)
        t.setFillAlpha(1);t.restoreState();t.setStrokeColor(colors.HexColor('#ffc329'));t.setLineWidth(1.3);t.drawPath(caminho(contorno),stroke=1,fill=0)
        t.setFillColor(colors.HexColor('#8bb8a8'));t.setStrokeColor(colors.HexColor('#00594f'));t.setLineWidth(1.5)
        t.setFillAlpha(.65);t.drawPath(caminho(self.feicoes['mina']),fill=1,stroke=1,fillMode=0);t.setFillAlpha(1)
        def etiqueta(x,y,texto):
            largura=t.stringWidth(texto,'GeoNegrito',6.5)
            t.setFillColor(colors.white);t.setFillAlpha(.85);t.rect(x+4,y+.5,largura+3,8,fill=1,stroke=0);t.setFillAlpha(1)
            t.setFillColor(colors.HexColor('#00594f'));t.setFont('GeoNegrito',6.5);t.drawString(x+5.5,y+2.4,texto)
        for (x,y),cor,rotulo in marcadores:
            t.setFillColor(cor);t.setStrokeColor(colors.white);t.setLineWidth(.8);t.circle(x,y,3.4,fill=1,stroke=1)
            if rotulo:etiqueta(x,y,rotulo)
        for rotulo,g,_ in self.setores:
            p=shape(g).representative_point();etiqueta(*xy((p.x,p.y)),rotulo)
        vistos=set()
        for rotulo,lon,lat in self.pontos:
            if rotulo in vistos:continue
            vistos.add(rotulo);x,y=xy(transform_geom('EPSG:4326','EPSG:31983',{'type':'Point','coordinates':[lon,lat]})['coordinates'])
            t.setFillColor(colors.white);t.setStrokeColor(colors.HexColor('#00594f'));t.setLineWidth(1.2);t.circle(x,y,3.6,fill=1,stroke=1)
            etiqueta(x,y,rotulo+'*')
        t.setFillColor(colors.HexColor('#00594f'));t.setStrokeColor(colors.HexColor('#00594f'));t.setLineWidth(1);t.setFont('GeoNegrito',8);t.drawString(self.width-27,self.height-18,'N')
        t.line(self.width-24,self.height-37,self.width-24,self.height-23);t.line(self.width-24,self.height-23,self.width-28,self.height-29);t.line(self.width-24,self.height-23,self.width-20,self.height-29)
        t.setFont('GeoRegular',6.5);t.line(12,27,12+1000*escala,27);t.drawString(16+1000*escala,24,'1 km - UTM 23S')
        legenda='Influência: amarelo | '+('Área minerada (MapBiomas): contorno vinho | ' if self.minerada else '')+'Mina OSM: verde | '
        if self.tema=='sugestao':
            legenda='Setores pelo 1º uso: verde conservação | laranja ecoturismo | marrom silvicultura | azul solar | Influência: amarelo | Mina OSM: verde'
            t.drawString(12,11,legenda)
        else:
            t.drawString(12,11,legenda+('Todos os temas sobrepostos' if self.tema is None else 'Pontos simulados *' if self.tema=='tecnicos' else 'Somente o tema desta ficha'))
        t.restoreState()
