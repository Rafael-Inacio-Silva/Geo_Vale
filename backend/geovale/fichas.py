"""Fatos territoriais reproduzíveis, separados dos comentários e do cenário fictício."""
import re
import unicodedata

import numpy as np
from rasterio.features import geometry_mask, shapes
from rasterio.io import MemoryFile
from rasterio.warp import transform, transform_geom
from shapely import make_valid
from shapely.geometry import Point, mapping, shape
from shapely.ops import unary_union

from geovale.camadas import CAMADAS

TEMAS = [(t['id'], t['nome']) for t in CAMADAS]
UTM = 'EPSG:31983'
# Resolução CONAMA 357/2005, arts. 14 a 17; classe especial mantém condições naturais, sem padrão numérico.
LIMITES_AGUA = {
    '1': {'ph': (6, 9), 'turbidez': 40, 'fe_dissolvido': .3, 'mn_total': .1},
    '2': {'ph': (6, 9), 'turbidez': 100, 'fe_dissolvido': .3, 'mn_total': .1},
    '3': {'ph': (6, 9), 'turbidez': 100, 'fe_dissolvido': 5, 'mn_total': .5},
    '4': {'ph': (6, 9)},
}
PARAMETROS_AGUA = {'ph': ('pH', ''), 'turbidez': ('Turbidez', 'UNT'),
                   'fe_dissolvido': ('Ferro dissolvido', 'mg/L'), 'mn_total': ('Manganês total', 'mg/L')}
GRAUS_CAVIDADES = ['muito alto', 'alto', 'medio', 'baixo', 'ocorrencia improvavel']


def formato(valor, casas=0):
    """Formata o valor calculado sem alterar sua precisão armazenada."""
    return f'{valor:,.{casas}f}'.replace(',', 'X').replace('.', ',').replace('X', '.')


def ha(valor):
    return formato(valor, 1) + ' ha'


def km(valor):
    return formato(valor, 2) + ' km'


def normalizar(texto):
    """Compara rótulos publicados com ou sem acentos."""
    return unicodedata.normalize('NFKD', str(texto or '')).encode('ascii', 'ignore').decode().strip().lower()


def projetar(geometria):
    """Projeta uma cópia em SIRGAS 2000 / UTM 23S para medidas métricas locais."""
    return shape(transform_geom('EPSG:4326', UTM, geometria))


def medidas(feicoes):
    """Mede linhas por registro e união de polígonos, evitando somar sobreposições de área."""
    gs = [projetar(f['geometry']) for f in feicoes]
    linhas = [g for g in gs if g.geom_type in ('LineString', 'MultiLineString')]
    poligonos = [g for g in gs if g.geom_type in ('Polygon', 'MultiPolygon')]
    return {'km': sum(g.length for g in linhas) / 1000,
            'ha': unary_union(poligonos).area / 10000 if poligonos else 0}


def ler_grade(bruto):
    """Abre o GeoTIFF guardado e mede cada célula pelos quatro vértices projetados em UTM 23S."""
    with MemoryFile(bruto) as memoria, memoria.open() as origem:
        valores, validos, t, crs = origem.read(1), origem.read_masks(1) != 0, origem.transform, origem.crs
    h, w = valores.shape
    colunas, linhas = np.meshgrid(np.arange(w + 1), np.arange(h + 1))
    xs, ys = t @ (colunas, linhas)
    ex, ny = (np.asarray(v).reshape(h + 1, w + 1) for v in transform(crs, UTM, xs.ravel(), ys.ravel()))
    vertices = [(ex[:-1, :-1], ny[:-1, :-1]), (ex[:-1, 1:], ny[:-1, 1:]), (ex[1:, 1:], ny[1:, 1:]), (ex[1:, :-1], ny[1:, :-1])]
    area = .5 * np.abs(sum(p[0] * q[1] - q[0] * p[1] for p, q in zip(vertices, vertices[1:] + vertices[:1])))
    return {'valores': valores, 'validos': validos, 'area': area, 'transform': t, 'crs': crs}


def distribuicao(grade, classes, mascara):
    """Área de cada classe oficial dentro da máscara, somando as células medidas em UTM."""
    total = grade['area'][mascara].sum() / 1e4
    linhas = []
    for c in classes:
        area = grade['area'][mascara & (grade['valores'] == c['codigo'])].sum() / 1e4
        if area > 0:
            linhas.append({**c, 'ha': area, 'percentual': area * 100 / total})
    return total, linhas


def texto_classes(linhas):
    return '\n'.join(f"{c['nome']}: {ha(c['ha'])} ({formato(c['percentual'], 1)}%)" for c in linhas) or 'Sem dado'


def preparar(dados):
    """Lê as grades guardadas e delimita a área minerada pela classe Mineração da cobertura MapBiomas."""
    dados['grades'] = {i: ler_grade(bruto) for i, bruto in dados.get('rasters', {}).items() if bruto}
    dados['area_minerada'] = None
    influencia = next(f['geometry'] for f in dados['influencia']['features'] if f['properties']['id'] == 'influencia')
    dados['recorte_ha'] = projetar(influencia).area / 1e4
    for b in dados['bases']:
        grade = dados['grades'].get(b['base']['id'])
        if b['base']['tema_id'] != 'vegetacao' or b['tipo'] != 'raster' or grade is None:
            continue
        classes = [c for c in b.get('classes', []) if 'minera' in normalizar(c['nome'])]
        mascara = grade['validos'] & np.isin(grade['valores'], [c['codigo'] for c in classes])
        if not mascara.any():
            return dados
        nativa = unary_union([shape(g) for g, _ in shapes(mascara.astype('uint8'), mask=mascara, transform=grade['transform'])])
        utm = shape(transform_geom(grade['crs'], UTM, mapping(nativa)))
        dados['area_minerada'] = {
            'nativa': nativa, 'crs': grade['crs'], 'utm': utm if utm.is_valid else make_valid(utm),
            'geojson': transform_geom(grade['crs'], 'EPSG:4326', mapping(nativa)),
            'ha': grade['area'][mascara].sum() / 1e4, 'cor': classes[0]['cor'],
            'classe': classes[0]['nome'], 'fonte': b['base']['nome']}
        return dados
    return dados


def mascara_minerada(grade, mineracao):
    """Seleciona, pelo centro, as células de outra grade que caem na área minerada."""
    if mineracao is None:
        return np.zeros(grade['valores'].shape, dtype=bool)
    geom = transform_geom(mineracao['crs'], grade['crs'], mapping(mineracao['nativa']))
    return geometry_mask([geom], grade['valores'].shape, grade['transform'], invert=True)


def dividir(feicoes, mineracao):
    """Total, parte na área minerada e entorno: linhas por registro, polígonos pela união, pontos por contagem."""
    gs = [projetar(f['geometry']) for f in feicoes]
    m = mineracao['utm'] if mineracao else None
    linhas = [g for g in gs if 'LineString' in g.geom_type]
    poligonos = [g for g in gs if 'Polygon' in g.geom_type]
    if linhas:
        total, dentro, unidade = sum(g.length for g in linhas) / 1000, (sum(g.intersection(m).length for g in linhas) / 1000 if m else None), 'km'
    elif poligonos:
        uniao = unary_union(poligonos)
        total, dentro, unidade = uniao.area / 1e4, (uniao.intersection(m).area / 1e4 if m else None), 'ha'
    else:
        total, dentro, unidade = len(gs), (sum(bool(g.intersects(m)) for g in gs) if m else None), 'registros'
    return {'unidade': unidade, 'total': total, 'dentro': dentro, 'entorno': None if dentro is None else total - dentro}


def medida(valor, unidade):
    return km(valor) if unidade == 'km' else ha(valor) if unidade == 'ha' else formato(valor) + ' ' + unidade


def texto_divisao(d, rotulo_dentro='Na área minerada'):
    if d['dentro'] is None:
        return 'Total: ' + medida(d['total'], d['unidade'])
    return '\n'.join([f"Total: {medida(d['total'], d['unidade'])}", f"{rotulo_dentro}: {medida(d['dentro'], d['unidade'])}",
                      f"No entorno: {medida(d['entorno'], d['unidade'])}"])


def distancia_km(feicoes, mineracao):
    """Menor distância em UTM 23S entre a área minerada e os registros; zero quando se tocam."""
    if not mineracao or not feicoes:
        return None
    return mineracao['utm'].distance(unary_union([projetar(f['geometry']) for f in feicoes])) / 1000


def chave_base(b):
    """Reconhece a base pelo nome da camada publicada, mantendo tratamento genérico para novas bases."""
    camada = b['base']['camada']
    for chave in ('cavidades', 'massa_dagua', 'hidrografia_principal', 'reg_vazao', 'enq_corpos', 'unidades_conservacao',
                  'apps_fbds', 'areas_urbanizadas', 'rodovias', 'barragens'):
        if chave in camada:
            return chave
    return b['base']['tema_id'] if b['tipo'] == 'vetor' else 'raster_' + b['base']['tema_id']


class Ficha:
    """Acumula fatos de um tema com origem, comentário por regras e resumo opcional."""

    def __init__(self):
        self.dados = []

    def fato(self, chave, nome, valor, origem, comentario, resumo=None, **extra):
        self.dados.append({'id': chave, 'nome': nome, 'valor': valor, 'origem': origem, 'comentario': comentario,
                           **({'resumo': resumo} if resumo else {}), **extra})


def fatos_relevo(f, b, ctx):
    grade = ctx['grades'].get(b['base']['id'])
    if grade is None:
        return
    dentro = grade['validos'] & mascara_minerada(grade, ctx['mineracao'])
    fora = grade['validos'] & ~dentro
    _, entorno = distribuicao(grade, b.get('classes', []), fora)

    def inferior(nome):
        numeros = re.findall(r'(\d+)\s*%', nome)
        return 0 if '<' in nome or not numeros else int(numeros[0])
    ingreme = sum(c['percentual'] for c in entorno if inferior(c['nome']) >= 20)
    rotulo = 'Declividade no entorno' if ctx['mineracao'] else 'Declividade no recorte'
    f.fato(b['base']['id'] + '.entorno', rotulo, texto_classes(entorno), b['base']['nome'] + ' (SRTM, 2000) · área das células em UTM 23S',
           f'{formato(ingreme, 1)}% do entorno tem declividade acima de 20%: favorece conservação, revegetação e uso contemplativo e '
           'limita agricultura mecanizada, energia solar e edificações. Relevo regional de 2000.',
           resumo=f'Declividade acima de 20% em {formato(ingreme, 1)}% do entorno')
    if dentro.any():
        _, minerada = distribuicao(grade, b.get('classes', []), dentro)
        f.fato(b['base']['id'] + '.minerada', 'Declividade na área minerada - relevo de 2000', texto_classes(minerada),
               'Mesma grade, células na área minerada',
               'Relevo anterior à configuração atual de cavas e pilhas: não descreve a área minerada hoje. '
               'Avaliar essa área exige levantamento topográfico atual (LiDAR ou drone).')


def fatos_cavidades(f, b, ctx):
    m = ctx['mineracao']
    por_grau = {}
    for x in b['dados']['features']:
        por_grau.setdefault(normalizar(x['properties'].get('grau_de_po')) or 'nao informado', []).append(x)
    ordem = sorted(por_grau, key=lambda g: GRAUS_CAVIDADES.index(g) if g in GRAUS_CAVIDADES else 99)
    linhas, alto, alto_dentro = [], 0, 0
    for grau in ordem:
        d = dividir(por_grau[grau], m)
        nome = next(str(x['properties'].get('grau_de_po') or 'Não informado') for x in por_grau[grau])
        linhas.append(f"{nome}: {ha(d['total'])}" + (f" ({ha(d['dentro'])} na área minerada)" if d['dentro'] is not None else ''))
        if grau in ('muito alto', 'alto'):
            alto, alto_dentro = alto + d['total'], alto_dentro + (d['dentro'] or 0)
    f.fato(b['base']['id'] + '.graus', 'Potencial de ocorrência de cavidades', '\n'.join(linhas) or 'Sem registro no recorte',
           b['base']['nome'] + ' · união por grau em UTM 23S',
           f'{ha(alto)} com potencial alto ou muito alto ({ha(alto_dentro)} na área minerada): intervenções nessas áreas exigem '
           'prospecção espeleológica, pois cavidades são patrimônio protegido (Decreto 99.556/1990). Mapa nacional 1:2.500.000.',
           resumo=f'Cavidades com potencial alto ou muito alto: {ha(alto)}')


def fatos_massas(f, b, ctx):
    d = dividir(b['dados']['features'], ctx['mineracao'])
    n = len(b['dados']['features'])
    comentario = (f"{ha(d['dentro'])} de superfície d’água estão na área minerada, possivelmente reservatórios ou cavas: seu destino "
                  'depende do fechamento e da descaracterização. A base não informa qualidade nem volume.' if d['dentro']
                  else 'Corpos d’água podem ancorar usos paisagísticos, recreativos ou de reservação. A base não informa qualidade nem volume.')
    f.fato(b['base']['id'] + '.ha', b['base']['nome'], f'{formato(n)} registros\n' + texto_divisao(d), 'Cadastro publicado · união em UTM 23S',
           comentario, resumo=f"{formato(n)} massas d’água ({ha(d['total'])})")


def fatos_trechos(f, b, ctx):
    d = dividir(b['dados']['features'], ctx['mineracao'])
    n = len(b['dados']['features'])
    comentario = (f"{km(d['dentro'])} de drenagem principal cruzam a área minerada: a conformação final do terreno precisa restabelecer "
                  'o escoamento e as faixas de APP. Extensão não informa vazão nem qualidade.' if d['dentro']
                  else 'A drenagem principal não cruza a área minerada; ela conecta o entorno e orienta onde a água escoa.')
    f.fato(b['base']['id'] + '.km', b['base']['nome'], f'{formato(n)} registros\n' + texto_divisao(d), 'Cadastro publicado · comprimento em UTM 23S',
           comentario, resumo=f"{km(d['total'])} de drenagem principal" + (f", {km(d['dentro'])} na área minerada" if d['dentro'] else ''))


def classe_enquadramento(props):
    valor = normalizar(props.get('enq_dn'))
    return 'Especial' if valor == 'especial' else valor or 'não informada'


def fatos_enquadramento(f, b, ctx):
    por_classe = {}
    for x in b['dados']['features']:
        por_classe.setdefault(classe_enquadramento(x['properties']), []).append(x)
    ordem = sorted(por_classe, key=lambda c: (c != 'Especial', c))
    linhas, total = [], {}
    for c in ordem:
        d = dividir(por_classe[c], ctx['mineracao'])
        total[c] = d['total']
        rotulo = 'Classe Especial' if c == 'Especial' else 'Classe ' + c
        linhas.append(f"{rotulo}: {km(d['total'])}" + (f" ({km(d['dentro'])} na área minerada)" if d['dentro'] is not None else ''))
    partes = []
    if 'Especial' in total:
        partes.append(f"Trechos de classe Especial ({km(total['Especial'])}) não admitem lançamento de efluentes, mesmo tratados")
    if '1' in total:
        partes.append(f"a classe 1 ({km(total['1'])}) tem os padrões mais restritivos")
    comentario = ('; '.join(partes) + ' (CONAMA 357/2005). ' if partes else '') + 'Usos futuros que lancem efluentes ficam condicionados à classe do trecho.'
    f.fato(b['base']['id'] + '.classes', 'Classe dos trechos (enquadramento)', '\n'.join(linhas) or 'Sem trecho enquadrado',
           b['base']['nome'] + ' · comprimento em UTM 23S', comentario[0].upper() + comentario[1:],
           resumo='Trechos classe Especial: ' + km(total.get('Especial', 0)))


def fatos_vazao(f, b, ctx):
    fs = [x for x in b['dados']['features'] if isinstance(x['properties'].get('q710_anual'), (int, float))]
    if not fs:
        f.fato(b['base']['id'] + '.q710', 'Vazão mínima de referência (Q7,10)', 'Sem trecho com vazão publicada', b['base']['nome'], 'Sem dado para leitura.')
        return
    m = ctx['mineracao']

    def descrever(x):
        p = x['properties']
        nome = str(p.get('noriocomp') or '').strip() or 'trecho sem nome'
        return f"{formato(p['q710_anual'], 3)} m³/s - {nome} (drenagem de {formato(p.get('nuareamont') or 0, 1)} km²)"
    maior = max(fs, key=lambda x: x['properties']['q710_anual'])
    linhas = [f'{formato(len(fs))} trechos com vazão regionalizada', 'Maior no recorte: ' + descrever(maior)]
    if m:
        dentro = [x for x in fs if projetar(x['geometry']).intersects(m['utm'])]
        if dentro:
            linhas.append('Maior em trecho na área minerada: ' + descrever(max(dentro, key=lambda x: x['properties']['q710_anual'])))
    f.fato(b['base']['id'] + '.q710', 'Vazão mínima de referência (Q7,10)', '\n'.join(linhas), b['base']['nome'] + ' · atributo publicado',
           'Q7,10 é a vazão de referência para outorga em MG (Portaria Igam 48/2019): indica a água disponível na estiagem para usos futuros '
           'como irrigação, abastecimento ou manutenção de lagos. Estimativa regional por trecho, não medição.',
           resumo=f"Maior Q7,10: {formato(maior['properties']['q710_anual'], 3)} m³/s")


def fatos_solos(f, b, ctx):
    m = ctx['mineracao']
    fs = b['dados']['features']
    por_classe = {}
    for x in fs:
        por_classe.setdefault(str(x['properties'].get('legenda') or x['properties'].get('nome') or 'Sem classe publicada'), []).append(x)
    d = dividir(fs, m)
    linhas = [f"Total: {ha(d['total'])}"]
    if d['dentro'] is not None:
        linhas.append(f"Na área minerada (pedologia anterior): {ha(d['dentro'])}")
    linhas += [f"- {nome}: {ha(dividir(grupo, None)['total'])}" for nome, grupo in sorted(por_classe.items())]
    nomes = normalizar(' '.join(por_classe))
    rasos = 'litolico' in nomes or 'cambissolo' in nomes
    f.fato(b['base']['id'] + '.classes', 'Classes de solo', '\n'.join(linhas), b['base']['nome'] + ' · união em UTM 23S',
           ('Cambissolos e Neossolos litólicos são rasos e pouco férteis: favorecem revegetação com espécies nativas adaptadas; '
            'agricultura exigiria correção intensiva. ' if rasos else 'Classes regionais orientam a escolha de espécies e o preparo do solo. ')
           + 'Na área minerada, o substrato atual é material minerado, não este solo.',
           resumo='; '.join(sorted(por_classe)))


def fatos_cobertura(f, b, ctx):
    grade = ctx['grades'].get(b['base']['id'])
    if grade is None:
        return
    total, linhas = distribuicao(grade, b.get('classes', []), grade['validos'])
    nativa = sum(c['percentual'] for c in linhas if re.search(r'formacao|afloramento|campo alagado|restinga|mangue|apicum', normalizar(c['nome'])))
    m = ctx['mineracao']
    f.fato(b['base']['id'] + '.classes', 'Uso e cobertura da terra', texto_classes(linhas), b['base']['nome'] + ' · área das células em UTM 23S',
           f'Vegetação nativa ocupa {formato(nativa, 1)}% do recorte: a matriz natural favorece reconexão ecológica e revegetação com espécies locais.'
           + (f" A classe {m['classe']} ({ha(m['ha'])}) define a área minerada usada nas demais fichas." if m else ''),
           resumo=f'Vegetação nativa: {formato(nativa, 1)}% do recorte')


def fatos_ucs(f, bases, ctx):
    """Agrupa UCs de todas as esferas pelo grupo do SNUC publicado no próprio registro."""
    m, grupos = ctx['mineracao'], {}
    for b in bases:
        for x in b['dados']['features']:
            p = x['properties']
            grupo = {'protecao integral': 'Proteção integral', 'uso sustentavel': 'Uso sustentável'}.get(normalizar(p.get('grupo')), 'Grupo não informado')
            grupos.setdefault(grupo, []).append((x, str(p.get('nome_uc') or x.get('id')), str(p.get('esfera') or b['base']['nome'])))
    comentarios = {
        'Proteção integral': 'Proteção integral admite apenas uso indireto, como pesquisa e visitação conforme o plano de manejo (Lei 9.985/2000): '
                             'usos produtivos ficam excluídos nessas áreas.',
        'Uso sustentável': 'Uso sustentável admite ocupação e usos compatíveis com o plano de manejo ou zoneamento de cada unidade: '
                           'condiciona o licenciamento, mas não impede o uso futuro.'}
    for grupo in sorted(grupos, key=lambda g: (g != 'Proteção integral', g)):
        itens = grupos[grupo]
        d = dividir([x for x, _, _ in itens], m)
        linhas = [f"Total (união): {ha(d['total'])} · {formato(d['total'] * 100 / ctx['recorte_ha'], 1)}% do recorte"]
        if d['dentro'] is not None:
            linhas.append(f"Na área minerada: {ha(d['dentro'])}")
        linhas += [f"- {nome} ({esfera}): {ha(dividir([x], None)['total'])}" for x, nome, esfera in sorted(itens, key=lambda i: i[1])]
        f.fato('vegetacao.' + normalizar(grupo).replace(' ', '_'), 'UCs de ' + grupo.lower(), '\n'.join(linhas),
               'Grupo publicado em cada UC · união em UTM 23S',
               comentarios.get(grupo, 'Grupo não publicado: a restrição aplicável precisa ser conferida no ato de criação.'),
               resumo=f"{grupo}: {ha(d['total'])}")


def fatos_apps(f, b, ctx):
    fs = b['dados']['features']
    d = dividir(fs, ctx['mineracao'])
    tipos = {}
    for x in fs:
        p = x['properties']
        tipos.setdefault((str(p.get('hidro') or 'não informado'), p.get('app_m')), []).append(x)
    linhas = texto_divisao(d).split('\n') + [f"- {tipo}: {formato(len(g))} registros" + (f' (faixa de {formato(faixa)} m)' if faixa else '')
                                             for (tipo, faixa), g in sorted(tipos.items(), key=lambda i: str(i[0]))]
    f.fato(b['base']['id'] + '.ha', 'APPs hídricas', '\n'.join(linhas), b['base']['nome'] + ' · união em UTM 23S',
           f"APPs devem manter ou recompor vegetação (Lei 12.651/2012); os {ha(d['dentro'] or 0)} de APP na área minerada indicam faixas "
           'a recompor no fechamento. Mapeamento regional da FBDS.',
           resumo=f"APPs: {ha(d['total'])}" + (f", {ha(d['dentro'])} na área minerada" if d['dentro'] else ''))


def fatos_proximidade(f, b, ctx, tipo):
    fs = b['dados']['features']
    d = dividir(fs, ctx['mineracao'])
    dist = distancia_km(fs, ctx['mineracao'])
    distancia = '' if dist is None else '\nDistância da área minerada: ' + ('encostam ou se sobrepõem' if dist < .005 else km(dist))
    valor = f'{formato(len(fs))} registros\n' + texto_divisao(d) + distancia
    if tipo == 'urbano':
        perto = '' if dist is None else 'encostam na área minerada' if dist < .005 else f'a {km(dist)} da área minerada'
        comentario = (f'Áreas urbanas {perto}: a proximidade de moradores amplia a demanda por lazer e serviços e também as exigências '
                      'de segurança e participação.' if perto else 'Ocupação urbana indica demanda potencial por lazer e serviços.')
        if d['dentro']:
            comentario += f" Os {ha(d['dentro'])} sobrepostos mostram classificação divergente entre IBGE e MapBiomas."
        resumo = f"Áreas urbanizadas: {ha(d['total'])}" + (f', {perto}' if perto else '')
    else:
        perto = '' if dist is None else 'cruzam ou encostam na área minerada' if dist < .005 else f'a {km(dist)} da área minerada'
        comentario = ((f'Rodovias {perto}: ' if perto else '') +
                      'o acesso existente reduz o custo de usos que recebem público ou carga. Cadastro não comprova condição da via.')
        resumo = f"Rodovias: {km(d['total'])}" + (f', {perto}' if perto else '')
    f.fato(b['base']['id'] + '.medidas', b['base']['nome'], valor, 'Cadastro publicado · medidas em UTM 23S', comentario, resumo=resumo)


def fatos_barragens(f, b, ctx):
    m = ctx['mineracao']
    fs = b['dados']['features']
    metodos = {'etapa unic': 'etapa única', 'linhadecen': 'linha de centro'}
    linhas, montante, dentro = [], [], 0
    for x in sorted(fs, key=lambda x: str(x['properties'].get('name') or x.get('id'))):
        p = x['properties']
        nome = str(p.get('name') or p.get('nome_estru') or x.get('id'))
        metodo = metodos.get(normalizar(p.get('metodo_con')), str(p.get('metodo_con') or 'método não informado'))
        finalidade = normalizar(p.get('finalidade'))
        finalidade = 'rejeitos' if 'rejeito' in finalidade else 'sedimentos' if 'sediment' in finalidade else str(p.get('finalidade') or 'finalidade não informada')
        na_area = bool(m and projetar(x['geometry']).intersects(m['utm']))
        dentro += na_area
        linhas.append(f"- {nome}: {finalidade}; {metodo}; PDA {p.get('pda') or 'n/i'}; classe {p.get('classe') or 'n/i'}" + (' · na área minerada' if na_area else ''))
        if normalizar(p.get('metodo_con')) == 'montante':
            montante.append(nome)
    cabecalho = f'{formato(len(fs))} barragens no recorte' + (f', {formato(dentro)} na área minerada' if m else '')
    f.fato(b['base']['id'] + '.lista', 'Barragens cadastradas', '\n'.join([cabecalho] + linhas), b['base']['nome'] + ' · atributos publicados',
           'Barragens e diques definem passivos do fechamento: descaracterização ou manutenção, monitoramento e restrição de uso a jusante. '
           'Nível de emergência atual deve ser conferido no SIGBM/ANM.',
           resumo=cabecalho + (f'; {formato(len(montante))} alteadas a montante' if montante else ''))
    f.fato(b['base']['id'] + '.montante', 'Alteadas a montante', '\n'.join(montante) or 'Nenhuma no recorte', 'Método construtivo publicado',
           'Barragens alteadas a montante devem ser descaracterizadas (Lei 14.066/2020); até a conclusão, o reservatório e a área a jusante '
           'ficam indisponíveis para usos com permanência de pessoas.' if montante else
           'Sem alteamento a montante no cadastro; ainda assim, estruturas ativas condicionam o uso a jusante.')
    f.fato('barragens.zas', 'Zona de autossalvamento (ZAS)', 'Não integrada', 'Limitação do MVP',
           'A camada pública de ZAS excede o limite de 32 MiB por consulta do adaptador. Em uso real, a ZAS é restrição obrigatória '
           'para usos com permanência de pessoas.')


def fatos_trilhas(f, b, ctx):
    fs = b['dados']['features']
    d = dividir(fs, ctx['mineracao'])
    f.fato(b['base']['id'] + '.km', b['base']['nome'], f'{formato(len(fs))} registros\n' + texto_divisao(d), 'Cadastro municipal · comprimento em UTM 23S',
           f"{km(d['entorno'] if d['entorno'] is not None else d['total'])} de trilhas cadastradas no entorno formam uma rede existente para "
           'ecoturismo e uso contemplativo' + (f"; {km(d['dentro'])} cruzam a área minerada, onde o acesso depende de segurança e autorização."
                                                if d['dentro'] else '.'),
           resumo=f"{formato(len(fs))} trilhas, {km(d['total'])}" + (f", {km(d['dentro'])} na área minerada" if d['dentro'] else ''))


def fatos_genericos(f, b, ctx):
    if b['tipo'] == 'raster':
        grade = ctx['grades'].get(b['base']['id'])
        if grade is not None:
            _, linhas = distribuicao(grade, b.get('classes', []), grade['validos'])
            f.fato(b['base']['id'] + '.classes', b['base']['nome'], texto_classes(linhas), 'Área das células em UTM 23S', 'Distribuição das classes publicadas no recorte.')
        return
    d = dividir(b['dados']['features'], ctx['mineracao'])
    f.fato(b['base']['id'] + '.medidas', b['base']['nome'], f"{formato(len(b['dados']['features']))} registros\n" + texto_divisao(d),
           'Cadastro publicado · medidas em UTM 23S', 'Contagem cadastral no recorte.')


def avaliar_agua(ponto, trechos):
    """Confere valores simulados com a classe real do trecho mais próximo (até 300 m) e os limites da CONAMA 357/2005."""
    alvo = projetar(mapping(Point(ponto['ponto'])))
    proximo = min(((projetar(x['geometry']).distance(alvo), x) for x in trechos), key=lambda i: i[0], default=(None, None))
    if proximo[0] is not None and proximo[0] <= 300:
        classe, origem = classe_enquadramento(proximo[1]['properties']), f'trecho enquadrado a {formato(proximo[0])} m'
    else:
        classe, origem = '2', 'sem trecho enquadrado a até 300 m; classe 2 por padrão (CONAMA 357/2005, art. 42)'
    limites = LIMITES_AGUA.get(classe, {})
    linhas, acima = [f'Classe {classe} ({origem})'], []
    for chave, valor in ponto['parametros'].items():
        nome, unidade = PARAMETROS_AGUA[chave]
        limite = limites.get(chave)
        if limite is None:
            situacao, referencia = 'sem padrão numérico nesta classe', ''
        elif isinstance(limite, tuple):
            situacao, referencia = ('dentro' if limite[0] <= valor <= limite[1] else 'fora da faixa'), f'{formato(limite[0], 1)} a {formato(limite[1], 1)}'
        else:
            situacao, referencia = ('dentro' if valor <= limite else 'acima'), 'até ' + formato(limite, 1 if limite >= 1 else 2)
        if situacao in ('acima', 'fora da faixa'):
            acima.append(nome)
        linhas.append(f"{nome}: {formato(valor, 1 if chave in ('ph', 'turbidez') else 2)}{(' ' + unidade) if unidade else ''} *"
                      + (f' (limite {referencia}): {situacao}' if referencia else f': {situacao}'))
    return classe, linhas, acima


def fatos_tecnicos(f, cenario, ctx, recorte_utm):
    m = ctx['mineracao']

    def local(ponto):
        alvo = projetar(mapping(Point(ponto)))
        if not recorte_utm.covers(alvo):
            raise ValueError('Ponto simulado fora do recorte')
        return 'na área minerada' if m and m['utm'].covers(alvo) else 'no entorno'
    trechos = ctx['enquadramento']
    for ponto in cenario.get('agua', []):
        classe, linhas, acima = avaliar_agua(ponto, trechos)
        n = len(ponto['parametros'])
        comentario = (f"Simulação: {formato(len(acima))} de {formato(n)} parâmetros fora do limite da classe {classe}. Em caso real, indicaria controle "
                      'de sedimentos e investigação da fonte antes de usar essa água.' if acima else
                      f'Simulação: parâmetros dentro da classe {classe}. Uma campanha isolada não caracteriza o corpo d’água; exige série temporal.')
        f.fato('tecnico.' + ponto['id'], ponto['nome'], '\n'.join(linhas), f"Simulado: {ponto['metodo']} · ponto {local(ponto['ponto'])}",
               comentario, resumo=f"{ponto['rotulo']}: classe {classe}, {formato(len(acima))} fora do limite", simulado=True,
               rotulo=ponto['rotulo'], ponto=ponto['ponto'])
    for item in cenario['dados']:
        valor = formato(item['valor'], 2 if isinstance(item['valor'], float) else 0) + ' ' + item['unidade'] + ' *'
        ref = item.get('referencia_tecnica')
        if ref:
            if 'minimo' in ref:
                situacao = 'atende' if item['valor'] >= ref['minimo'] else 'abaixo do mínimo'
            else:
                situacao = 'abaixo do limiar' if item['valor'] < ref['maximo'] else 'no limiar ou acima'
            valor += f"\nReferência: {ref['texto']}: {situacao}"
        origem = 'Simulado: ' + item['metodo'] + (f" · ponto {local(item['ponto'])}" if item.get('ponto') else ' · sem localização')
        f.fato('tecnico.' + item['id'], item['nome'], valor, origem, item['comentario'], resumo=item['nome'] + ': ' + valor.split('\n')[0],
               simulado=True, **({'rotulo': item['rotulo'], 'ponto': item['ponto']} if item.get('ponto') else {}))


ESPECIFICOS = {'cavidades': fatos_cavidades, 'massa_dagua': fatos_massas, 'hidrografia_principal': fatos_trechos,
               'enq_corpos': fatos_enquadramento, 'reg_vazao': fatos_vazao, 'solos': fatos_solos, 'raster_relevo': fatos_relevo,
               'raster_vegetacao': fatos_cobertura, 'apps_fbds': fatos_apps, 'barragens': fatos_barragens, 'trilhas': fatos_trilhas,
               'areas_urbanizadas': lambda f, b, c: fatos_proximidade(f, b, c, 'urbano'),
               'rodovias': lambda f, b, c: fatos_proximidade(f, b, c, 'via')}


def montar_fichas(dados, cenario):
    """Deriva fichas de todas as bases, sem utilizar checkbox, LLM ou número demonstrativo real.

    Espera `preparar(dados)` já aplicado: grades medidas e área minerada delimitada.
    """
    ctx = {'grades': dados.get('grades', {}), 'mineracao': dados.get('area_minerada'), 'recorte_ha': dados.get('recorte_ha') or 1,
           'enquadramento': [x for b in dados['bases'] if chave_base(b) == 'enq_corpos' for x in b['dados']['features']]}
    fichas = []
    for tema, nome in TEMAS:
        bases = [b for b in dados['bases'] if b['base']['tema_id'] == tema]
        f = Ficha()
        ucs = [b for b in bases if chave_base(b) == 'unidades_conservacao']
        for b in bases:
            chave = chave_base(b)
            if chave == 'unidades_conservacao':
                if b is ucs[0]:
                    fatos_ucs(f, ucs, ctx)
                continue
            ESPECIFICOS.get(chave, fatos_genericos)(f, b, ctx)
        if tema == 'agua':
            f.fato('agua.qualidade', 'Qualidade da água', 'Sem rede pública integrada no recorte', 'Não medido',
                   'pH, turbidez e metais exigem campanhas. A ficha de dados técnicos simula três pontos e confere os valores com os limites '
                   'da classe real do trecho.')
        fichas.append({'id': tema, 'nome': nome, 'bases': bases, 'dados': f.dados})
    influencia = next(x['geometry'] for x in dados['influencia']['features'] if x['properties']['id'] == 'influencia')
    f = Ficha()
    fatos_tecnicos(f, cenario, ctx, projetar(influencia))
    fichas.append({'id': 'tecnicos', 'nome': 'Dados técnicos simulados', 'bases': [], 'dados': f.dados})
    return fichas
