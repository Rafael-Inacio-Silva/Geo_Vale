"""Fatos territoriais reproduzíveis, separados dos comentários e do cenário fictício."""
from rasterio.warp import transform_geom
from shapely.geometry import shape
from shapely.ops import unary_union

TEMAS = [('relevo', 'Relevo e declividade'), ('agua', 'Água e drenagem'), ('solos', 'Solos'),
         ('vegetacao', 'Vegetação e conservação'), ('entorno', 'Entorno e infraestrutura'), ('trilhas', 'Trilhas de Nova Lima')]


def formato(valor, casas=0):
    """Formata o valor calculado sem alterar sua precisão armazenada."""
    return f'{valor:,.{casas}f}'.replace(',', 'X').replace('.', ',').replace('X', '.')


def projetar(geometria):
    """Projeta uma cópia em SIRGAS 2000 / UTM 23S para medidas métricas locais."""
    return shape(transform_geom('EPSG:4326', 'EPSG:31983', geometria))


def medidas(feicoes):
    """Mede linhas por registro e união de polígonos, evitando somar sobreposições de área."""
    gs = [projetar(f['geometry']) for f in feicoes]
    linhas = [g for g in gs if g.geom_type in ('LineString', 'MultiLineString')]
    poligonos = [g for g in gs if g.geom_type in ('Polygon', 'MultiPolygon')]
    return {'km': sum(g.length for g in linhas) / 1000,
            'ha': unary_union(poligonos).area / 10000 if poligonos else 0}


def montar_fichas(dados, cenario):
    """Deriva fichas de todas as bases, sem utilizar checkbox, LLM ou número demonstrativo real."""
    fichas = []
    def fato(lista, chave, nome, valor, origem, comentario):
        lista.append({'id': chave, 'nome': nome, 'valor': valor, 'origem': origem, 'comentario': comentario})
    for tema, nome in TEMAS:
        bases = [b for b in dados['bases'] if b['base']['tema_id'] == tema]
        itens = []
        for b in bases:
            chave = b['base']['id']
            if b['tipo'] == 'raster':
                fato(itens, chave+'.celulas', 'Células válidas', formato(b['quantidade']), 'Contagem da grade',
                     'Contagem das células com valor dentro do recorte. Não representa medição de área ou condição atual da mina.')
                classes = '\n'.join(f'{c["nome"]}: {formato(c["celulas"])} ({formato(c["percentual_celulas_validas"],2)}%)' for c in b.get('classes', []))
                fato(itens, chave+'.classes', 'Classes e contagens', classes or 'Sem classes publicadas', 'Valores categóricos da fonte',
                     'Distribuição das classes publicadas na grade. Percentuais se referem às células válidas; não são percentuais de área.')
                fato(itens, chave+'.nodata', 'Células sem dados no recorte', (formato(b['celulas_sem_dados']) if 'celulas_sem_dados' in b else 'Não informado'), 'Máscara da grade',
                     'Ausência de valor limita a caracterização. Não deve ser interpretada como inexistência de vegetação, água ou declividade.')
                continue
            fs = b['dados']['features']; m = medidas(fs)
            fato(itens, chave+'.registros', b['base']['nome'], formato(len(fs))+' registros', 'Cadastro publicado / recorte',
                 {'agua': ('São corpos de água cadastrados no recorte. A superfície mapeada não fornece profundidade, volume ou qualidade da água.' if any('Polygon' in f['geometry']['type'] for f in fs) else 'São trechos cadastrados, não rios distintos. A drenagem conecta partes do território; sua extensão não informa vazão ou qualidade.'),
                  'vegetacao': 'São cadastros de conservação por esfera. Presença no recorte não determina automaticamente a restrição legal aplicável.',
                  'solos': 'Unidades pedológicas regionais descrevem classes de solo. Não são ensaios de compactação, fertilidade ou contaminação.',
                  'entorno': 'Registros de ocupação ou vias descrevem o contexto. Não comprovam capacidade, condição operacional ou demanda.',
                  'trilhas': 'Traçados cadastrados dão contexto à circulação. Não comprovam acesso público, segurança ou conservação.'}.get(tema, 'Contagem cadastral no recorte.'))
            if any('LineString' in f['geometry']['type'] for f in fs):
                fato(itens, chave+'.km', 'Extensão dos trechos recortados', formato(m['km'],2)+' km', 'Calculado em UTM 23S',
                     'Soma dos comprimentos dos registros recortados. Sobreposições entre registros não foram dissolvidas; não mede acessibilidade ou vazão.')
            elif any('Polygon' in f['geometry']['type'] for f in fs):
                fato(itens, chave+'.ha', 'Superfície no recorte', formato(m['ha'],2)+' ha', 'União geométrica em UTM 23S',
                     'Área da união dos polígonos desta base dentro da influência. Não é área a recuperar, volume, profundidade ou diagnóstico de qualidade.')
            if tema == 'solos':
                nomes = sorted({str(f['properties'].get('legenda') or f['properties'].get('nome') or 'Sem classe publicada') for f in fs})
                fato(itens, chave+'.classes', 'Classes de solo', '; '.join(nomes), 'Atributo publicado',
                     'Classes regionais orientam a leitura do substrato. Condições locais de plantio exigem amostragem e ensaios específicos.')
        if tema == 'vegetacao':
            vetores=[b for b in bases if b['tipo']=='vetor']
            itens=[i for i in itens if not any(i['id'].startswith(b['base']['id']+'.') for b in vetores)]
            fato(itens,'vegetacao.ucs','Unidades de conservação', '\n'.join(b['base']['nome']+': '+str(len(b['dados']['features'])) for b in vetores),'Cadastro por esfera',
                 'Cadastros de esferas distintas podem se sobrepor. Contagem não determina restrição, estado de conservação ou área de recuperação.')
            fato(itens,'vegetacao.superficies','Superfície das UCs no recorte','\n'.join(b['base']['nome']+': '+formato(medidas(b['dados']['features'])['ha'],2)+' ha' for b in vetores),'União por base em UTM 23S',
                 'Áreas calculadas separadamente por base, sem somar esferas. A aplicação de regras de proteção exige enquadramento específico.')
        if tema == 'agua':
            fato(itens, 'agua.ensaios', 'pH, vazão atual, profundidade, volume e biota', 'Não disponíveis nas bases integradas', 'Não medido',
                 'Geometria de rio ou corpo de água não fornece esses parâmetros. Eles requerem campanhas, levantamentos ou documentos técnicos específicos.')
        fichas.append({'id': tema, 'nome': nome, 'bases': bases, 'dados': itens})
    tecnicos=[]
    for item in cenario['dados']:
        fato(tecnicos, 'tecnico.'+item['id'], item['nome'], formato(item['valor'],2 if isinstance(item['valor'],float) else 0)+' '+item['unidade']+' *', 'Simulado: '+item['metodo'], item['comentario'])
        tecnicos[-1]['simulado'] = True
    fichas.append({'id':'tecnicos','nome':'Dados técnicos sem camada','bases':[],'dados':tecnicos})
    return fichas
