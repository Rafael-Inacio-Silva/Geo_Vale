"""Caracterização local de dois recortes reais; indicadores não certificam uso, custo ou segurança."""
from pathlib import Path
import hashlib
import json
import numpy as np
import rasterio
from rasterio.features import geometry_mask
from pyproj import Transformer
from shapely import transform, normalize
from shapely.geometry import shape, box, mapping

from geovale.geografia.entrada import validar_geojson
from .metodos import ErroDecisao

RAIZ = Path(__file__).resolve().parents[3]
DADOS = RAIZ/'dados/demonstracao'
CODIGOS = ('il_006', 'il_071')
CLASSES = {11:'Água',21:'Ocupação aberta',22:'Ocupação baixa',23:'Ocupação média',24:'Ocupação alta',
           31:'Solo exposto',41:'Floresta decídua',42:'Floresta perene',43:'Floresta mista',
           52:'Arbustos',71:'Herbáceas',81:'Pastagem / feno',82:'Cultivos',90:'Áreas úmidas arborizadas',95:'Áreas úmidas herbáceas'}
CRITERIOS = [
    {'id':'cobertura','nome':'Cobertura atual','descricao':'Representação de classes associadas ao cenário dentro da área. Não comprova aptidão futura.','unidade':'índice 0–100','sentido':'beneficio'},
    {'id':'entorno','nome':'Continuidade com o entorno','descricao':'Representação das mesmas classes num anel de 1 km. Indicador de contexto, sem equivaler a conectividade ecológica.','unidade':'índice 0–100','sentido':'beneficio'},
    {'id':'relevo','nome':'Condição relativa do relevo','descricao':'Transformação exploratória da declividade. Não avalia estabilidade geotécnica.','unidade':'índice 0–100','sentido':'beneficio'}]
ALTERNATIVAS = [
    {'id':'agricultura','nome':'Agricultura','descricao':'Explorar agricultura; solo, clima e segurança alimentar ainda exigem estudos.','classes':[81,82],'expoente_relevo':3},
    {'id':'uso_florestal','nome':'Uso florestal','descricao':'Explorar uso florestal; não equivale a restauração nativa aprovada.','classes':[41,42,43],'expoente_relevo':1},
    {'id':'recreacao','nome':'Recreação em áreas abertas','descricao':'Explorar lazer terrestre em áreas abertas; não avalia banho, esportes aquáticos ou acesso público.','classes':[21,71],'expoente_relevo':2}]
AVISO = 'Comparação territorial exploratória. Não avalia custos, segurança, qualidade do solo ou aceitação social e não autoriza uso.'


def sha256(arquivo: Path) -> str:
    """Assina bytes para conferir se os dados correspondem ao pacote preparado."""
    return hashlib.sha256(arquivo.read_bytes()).hexdigest()


def carregar_caso(codigo: str, dados: Path = DADOS) -> dict:
    """Confere a lista fixa de fontes antes de carregar o recorte, sem aceitar caminhos do usuário."""
    if codigo not in CODIGOS:
        raise ErroDecisao('Caso demonstrativo desconhecido.')
    pasta = dados/codigo
    try:
        manifesto = json.loads((pasta/'manifesto.json').read_text())
        for nome, esperado in manifesto['sha256'].items():
            if Path(nome).name != nome or sha256(pasta/nome) != esperado:
                raise ErroDecisao('Uma fonte preparada está ausente ou teve sua integridade alterada.')
    except (OSError,ValueError,KeyError,TypeError) as exc:
        raise ErroDecisao('Uma fonte preparada está ausente ou não pôde ser conferida.') from exc
    return manifesto


def geometria_documento(documento: dict):
    """Monta a superfície 2D de posições já validadas, preservando a altitude no documento original."""
    geometria = documento['features'][0]['geometry']
    partes = [geometria['coordinates']] if geometria['type'] == 'Polygon' else geometria['coordinates']
    planas = [[[posicao[:2] for posicao in anel] for anel in parte] for parte in partes]
    return shape({'type': geometria['type'], 'coordinates': planas[0] if geometria['type'] == 'Polygon' else planas})


def projetar(g, epsg):
    """Transforma explicitamente longitude/latitude para a referência métrica da fonte."""
    t = Transformer.from_crs(4326, epsg, always_xy=True)
    return transform(g, t.transform, interleaved=False)


def resumo_entrada(conteudo: bytes, nome: str, dados: Path = DADOS) -> dict:
    """Valida o upload, mede com UTM local e identifica os dois casos pela geometria, não pelo nome do arquivo."""
    area = validar_geojson(conteudo, nome)
    g = geometria_documento(area.documento)
    centro = g.centroid
    if not -80 <= centro.y <= 84 or g.bounds[2] - g.bounds[0] > 6 or g.bounds[3] - g.bounds[1] > 6:
        raise ErroDecisao('Use uma área local dentro de uma zona UTM, entre 80°S e 84°N.')
    zona = min(60, max(1, int((centro.x + 180)//6) + 1))
    epsg = (32600 if centro.y >= 0 else 32700) + zona
    geom_m = projetar(g, epsg)
    codigo = None
    caso = None
    canonica = normalize(g).wkb
    for cod in CODIGOS:
        m = carregar_caso(cod, dados)
        outro = json.loads((dados/cod/'area.geojson').read_text())
        if normalize(geometria_documento(outro)).wkb == canonica:
            codigo, caso = cod, m
            break
    return {'arquivo': nome, 'sha256_entrada': area.sha256, 'documento': area.documento,
            'geometria': mapping(g), 'area_ha': geom_m.area/10000, 'epsg_medida': epsg,
            'numero_partes': area.numero_partes, 'bbox': list(g.bounds),
            'caso': codigo, 'nome': caso['nome'] if caso else nome.removesuffix('.geojson'),
            'localizacao': caso['localizacao'] if caso else 'Área enviada',
            'imagem': {'bounds':caso['imagem_bounds'],'credito':caso['credito_imagem']} if caso else None,
            'estado':'pronta_para_analisar' if caso else 'sem_fontes_preparadas',
            'aviso':AVISO}


def declividade_horn(z: np.ndarray, passo_x: float, passo_y: float) -> np.ndarray:
    """Calcula Horn 3×3 em graus conservando bordas e vizinhos sem dados como ausentes."""
    if z.ndim != 2 or min(z.shape)<3 or passo_x<=0 or passo_y<=0:
        raise ErroDecisao('Grade de relevo incompatível.')
    a,b,c=z[:-2,:-2],z[:-2,1:-1],z[:-2,2:]
    d,f=z[1:-1,:-2],z[1:-1,2:]
    g,h,i=z[2:,:-2],z[2:,1:-1],z[2:,2:]
    dx=((c+2*f+i)-(a+2*d+g))/(8*passo_x)
    dy=((g+2*h+i)-(a+2*b+c))/(8*passo_y)
    validos=np.ones(dx.shape,dtype=bool)
    for linha in range(3):
        for coluna in range(3):validos &= np.isfinite(z[linha:linha+dx.shape[0],coluna:coluna+dx.shape[1]])
    saida=np.full(z.shape,np.nan)
    saida[1:-1,1:-1]=np.where(validos,np.degrees(np.arctan(np.hypot(dx,dy))),np.nan)
    return saida


def extrair_dem(g, caminho: Path) -> tuple[dict,np.ndarray]:
    """Extrai relevo só com cobertura integral, nove amostras e ao menos 90% de dados válidos."""
    with rasterio.open(caminho) as ds:
        geom = projetar(g,ds.crs)
        px,py=ds.res
        if ds.count!=1 or ds.crs.is_geographic or not box(ds.bounds.left+px,ds.bounds.bottom+py,ds.bounds.right-px,ds.bounds.top-py).covers(geom):
            raise ErroDecisao('O relevo não cobre integralmente esta área.')
        z=ds.read(1,masked=True).astype(float).filled(np.nan)
        mascara=geometry_mask([mapping(geom)],out_shape=ds.shape,transform=ds.transform,invert=True)
        slope=declividade_horn(z,px,py)
        bons=mascara & np.isfinite(slope)
        partes=list(geom.geoms) if geom.geom_type=='MultiPolygon' else [geom]
        for parte in partes:
            m=geometry_mask([mapping(parte)],out_shape=ds.shape,transform=ds.transform,invert=True)
            if not np.any(m & bons):raise ErroDecisao('Uma parte do mapa não está representada no relevo.')
        if bons.sum()<9 or not mascara.sum() or bons.sum()/mascara.sum()<.9:
            raise ErroDecisao('A qualidade do relevo é insuficiente para esta comparação.')
        amostras=slope[bons]
        resumo={'declividade_mediana_graus':float(np.median(amostras)),
                'declividade_p90_graus':float(np.percentile(amostras,90)),
                'elevacao_min_m':float(np.nanmin(z[mascara])), 'elevacao_max_m':float(np.nanmax(z[mascara])),
                'celulas_validas':int(bons.sum()),'fracao_valida':float(bons.sum()/mascara.sum()),'passo_m':list(ds.res),'epsg':ds.crs.to_epsg()}
    return resumo,amostras


def extrair_cobertura(g,caminho:Path,ano:int) -> dict:
    """Conta classes originais na área e no anel externo de 1 km, sem confundir ausência e dado faltante."""
    with rasterio.open(caminho) as ds:
        geom=projetar(g,ds.crs);anel=geom.buffer(1000).difference(geom)
        if not box(*ds.bounds).covers(geom.buffer(1000)):raise ErroDecisao('A cobertura do solo não cobre o entorno completo.')
        z=ds.read(1,masked=True);valido=~np.ma.getmaskarray(z) & np.isin(z.data,list(CLASSES))
        saida={}
        for nome,superficie in (('area',geom),('entorno',anel)):
            mascara=geometry_mask([mapping(superficie)],out_shape=ds.shape,transform=ds.transform,invert=True)
            bons=mascara & valido
            if not mascara.sum() or bons.sum()/mascara.sum()<.9:raise ErroDecisao('Cobertura do solo insuficiente; não foi atribuída nota.')
            classes,contagens=np.unique(z.data[bons],return_counts=True)
            saida[nome]={'celulas_validas':int(bons.sum()),'fracao_valida':float(bons.sum()/mascara.sum()),
                         'percentuais':{str(int(c)):float(q/bons.sum()*100) for c,q in zip(classes,contagens)}}
        saida.update(ano=ano,produto='Annual NLCD',raio_entorno_m=1000)
        return saida


def analisar_territorio(entrada: dict, dados:Path=DADOS) -> dict:
    """Recalcula indicadores reais; regras exploratórias não são critérios certificados de aptidão."""
    codigo=entrada.get('caso')
    if not codigo:raise ErroDecisao('Este mapa ainda não tem fontes territoriais preparadas. Prepare as fontes desta área antes de comparar.')
    manifesto=carregar_caso(codigo,dados)
    g=shape(entrada['geometria']);pasta=dados/codigo
    relevo,inclinacoes=extrair_dem(g,pasta/'relevo.tif')
    cobertura=extrair_cobertura(g,pasta/'cobertura.tif',manifesto['cobertura_ano'])
    notas=[];auditoria=[]
    for alternativa in ALTERNATIVAS:
        classes=alternativa['classes']
        local=sum(cobertura['area']['percentuais'].get(str(c),0) for c in classes)
        contexto=sum(cobertura['entorno']['percentuais'].get(str(c),0) for c in classes)
        topo=float(np.mean((1-inclinacoes/90)**alternativa['expoente_relevo'])*100)
        notas.append([local,contexto,topo])
        auditoria.append({'alternativa':alternativa['id'],'classes_associadas':classes,
                         'formula_relevo':f'média de 100 × (1 − declividade_graus/90)^{alternativa["expoente_relevo"]}',
                         'natureza_regra':'Hipótese exploratória do protótipo; associação de classes e expoentes não calibrados ou validados por especialistas.',
                         'valores_calculados':[local,contexto,topo]})
    dominante=max(cobertura['area']['percentuais'],key=cobertura['area']['percentuais'].get)
    return {'estado':'analisada','relevo':relevo,'cobertura':cobertura,'cobertura_predominante':CLASSES[int(dominante)],
            'criterios':CRITERIOS,'alternativas':ALTERNATIVAS,'matriz':notas,'regras':auditoria,
            'triagem':{'comparacao_territorial':'disponivel','decisao_de_uso':'pendente_de_estudos',
                       'nao_avaliados':['Estabilidade geotécnica e contaminação','Solo e clima para o uso proposto','Custos de implantação e manutenção','Demanda e aceitação social','Permissões e viabilidade do uso']},
            'fontes':manifesto,'aviso':AVISO,
            'limitacoes':['Classes do solo atual não equivalem a potencial de uso futuro.','Cobertura atual e entorno podem ser correlacionados; avaliar sensibilidade dos pesos.',
                          'Perfil exploratório de pesquisa: sem parecer da Vale, sem notas de especialistas e sem estimativa de custo.',
                          'Fontes de diferentes datas e resoluções; imagem de fundo serve apenas à visualização.']}
