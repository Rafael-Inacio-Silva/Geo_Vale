"""Sugestão multicritério de uso pós-mineração por setor da área minerada.

Restrições legais excluem usos; fatores padronizados de 0 a 1 são combinados por soma ponderada
com pesos do engenheiro (padrão calculado por AHP). O resultado ordena usos para discussão; não decide.
"""
import hashlib
import json
import math
import threading

import numpy as np
import shapely
from rasterio.warp import transform, transform_geom
from shapely.geometry import mapping
from shapely.ops import unary_union

from geovale.fichas import NATIVA, UTM, chave_base, formato, ha, normalizar, preparar, projetar

CRITERIOS = [
    {'id': 'relevo', 'nome': 'Relevo (declividade)', 'curto': 'relevo'},
    {'id': 'vegetacao', 'nome': 'Vegetação nativa no entorno', 'curto': 'vegetação nativa'},
    {'id': 'drenagem', 'nome': 'Distância da drenagem', 'curto': 'drenagem'},
    {'id': 'acesso', 'nome': 'Acesso por rodovia', 'curto': 'acesso'},
    {'id': 'urbano', 'nome': 'Proximidade urbana', 'curto': 'proximidade urbana'},
    {'id': 'rede', 'nome': 'Rede elétrica', 'curto': 'rede elétrica'},
    {'id': 'trilhas', 'nome': 'Trilhas existentes', 'curto': 'trilhas'},
]
IDS = [c['id'] for c in CRITERIOS]
USOS = [
    {'id': 'conservacao', 'nome': 'Conservação e restauração', 'cor': '#2e7d32'},
    {'id': 'ecoturismo', 'nome': 'Ecoturismo e lazer', 'cor': '#e09b00'},
    {'id': 'silvicultura', 'nome': 'Silvicultura', 'cor': '#8d6e63'},
    {'id': 'solar', 'nome': 'Energia solar e infraestrutura', 'cor': '#1565c0'},
]
# Julgamentos par a par na escala de Saaty (1 a 9): quanto o primeiro critério importa mais que o segundo.
JULGAMENTOS = {
    ('relevo', 'vegetacao'): 2, ('relevo', 'drenagem'): 3, ('relevo', 'acesso'): 3, ('relevo', 'urbano'): 4, ('relevo', 'rede'): 5, ('relevo', 'trilhas'): 5,
    ('vegetacao', 'drenagem'): 2, ('vegetacao', 'acesso'): 2, ('vegetacao', 'urbano'): 3, ('vegetacao', 'rede'): 4, ('vegetacao', 'trilhas'): 4,
    ('drenagem', 'acesso'): 1, ('drenagem', 'urbano'): 2, ('drenagem', 'rede'): 3, ('drenagem', 'trilhas'): 3,
    ('acesso', 'urbano'): 2, ('acesso', 'rede'): 2, ('acesso', 'trilhas'): 3,
    ('urbano', 'rede'): 1, ('urbano', 'trilhas'): 2, ('rede', 'trilhas'): 1,
}
INDICE_ALEATORIO = {3: .58, 4: .90, 5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45}
MINIMO_HA = 20
VARIACAO = .2


def decresce(a, b, piso=0.):
    """1 até `a` metros, caindo linearmente até `piso` em `b`."""
    return lambda x: piso + (1 - piso) * np.clip((b - x) / (b - a), 0, 1)


def cresce(a, b, piso=0.):
    """`piso` até `a`, subindo linearmente até 1 em `b`."""
    return lambda x: piso + (1 - piso) * np.clip((x - a) / (b - a), 0, 1)


def por_classe(tabela):
    """Nota por classe de relevo da Embrapa (1 plano a 6 escarpado); sem dado vale 0,5."""
    tabela_completa = np.full(256, .5)
    for classe, nota in tabela.items():
        tabela_completa[classe] = nota
    return lambda x: tabela_completa[x.astype(int)]


# Régua de cada uso em cada critério (nota de 0 a 1); critério ausente não participa do uso.
# Uma fonte só: o cálculo e a tabela de referência do relatório saem daqui.
CLASSES_RELEVO = ['plano', 'suave ondulado', 'ondulado', 'forte ondulado', 'montanhoso', 'escarpado']
REGUAS = {
    'conservacao': {'relevo': ('classe', {1: .5, 2: .5, 3: .7, 4: 1, 5: 1, 6: 1}), 'vegetacao': ('cresce', .1, .6, 0.),
                    'drenagem': ('decresce', 100, 600, .3), 'urbano': ('cresce', 500, 3000, .3)},
    'ecoturismo': {'relevo': ('classe', {1: .8, 2: 1, 3: 1, 4: .8, 5: .5, 6: .2}), 'vegetacao': ('cresce', .1, .6, .3),
                   'drenagem': ('decresce', 200, 1500, .3), 'acesso': ('decresce', 1000, 8000, 0.), 'urbano': ('decresce', 2000, 10000, .2),
                   'trilhas': ('decresce', 300, 3000, 0.)},
    'silvicultura': {'relevo': ('classe', {1: 1, 2: 1, 3: .7, 4: .3, 5: 0, 6: 0}), 'drenagem': ('cresce', 30, 200, 0.),
                     'acesso': ('decresce', 1000, 8000, .2)},
    'solar': {'relevo': ('classe', {1: 1, 2: .8, 3: .3, 4: 0, 5: 0, 6: 0}), 'drenagem': ('cresce', 50, 300, 0.),
              'acesso': ('decresce', 1000, 8000, 0.), 'urbano': ('decresce', 3000, 10000, .3), 'rede': ('decresce', 1000, 10000, 0.)},
}


def construir(regua):
    tipo, *parametros = regua
    if tipo == 'classe':
        return por_classe(parametros[0])
    a, b, piso = parametros
    return (cresce if tipo == 'cresce' else decresce)(a, b, piso)


RESPOSTAS = {u: {c: construir(r) for c, r in criterios.items()} for u, criterios in REGUAS.items()}


def metros(valor):
    return f"{formato(valor)} m" if valor < 1000 else f"{formato(valor / 1000, 0 if valor % 1000 == 0 else 1)} km"


def texto_regua(uso, criterio):
    """A régua em palavras e números, para a tabela de referência do relatório."""
    regua = REGUAS[uso].get(criterio)
    if regua is None:
        return 'não conta'
    tipo, *parametros = regua
    if tipo == 'classe':
        return ' · '.join(formato(parametros[0][i], 1 if parametros[0][i] % 1 else 0) for i in range(1, 7))
    a, b, piso = parametros
    nota = lambda v: formato(v, 1 if v % 1 else 0)
    if criterio == 'vegetacao':
        return f"{nota(piso)} até {formato(a * 100)}% de nativa; 1 a partir de {formato(b * 100)}%"
    if tipo == 'decresce':
        return f"1 até {metros(a)}; {nota(piso)} a partir de {metros(b)}"
    return f"{nota(piso)} até {metros(a)}; 1 a partir de {metros(b)}"


RESTRICOES = [
    {'id': 'pi_restrita', 'nome': 'UC de proteção integral sem visitação', 'curto': 'UC de proteção integral', 'permite': ['conservacao'], 'base': 'Lei 9.985/2000, arts. 7º e 9º'},
    {'id': 'pi_visitacao', 'nome': 'Parque ou monumento natural', 'curto': 'parque ou monumento natural', 'permite': ['conservacao', 'ecoturismo'], 'base': 'Lei 9.985/2000, arts. 7º, 11 e 12'},
    {'id': 'app', 'nome': 'APP hídrica', 'curto': 'APP', 'permite': ['conservacao', 'ecoturismo'], 'base': 'Lei 12.651/2012, arts. 3º (X, c), 4º e 8º'},
    {'id': 'zas', 'nome': 'Zona de autossalvamento', 'curto': 'ZAS', 'permite': ['conservacao', 'silvicultura'], 'base': 'Lei 12.334/2010, alterada pela Lei 14.066/2020'},
    {'id': 'agua', 'nome': 'Superfície d’água', 'curto': 'superfície d’água', 'permite': ['conservacao', 'ecoturismo'], 'base': 'Massas d’água ANA/Igam'},
]


def pesos_ahp():
    """Autovetor principal da matriz recíproca e razão de consistência de Saaty."""
    n = len(IDS)
    matriz = np.ones((n, n))
    for (a, b), valor in JULGAMENTOS.items():
        i, j = IDS.index(a), IDS.index(b)
        matriz[i, j], matriz[j, i] = valor, 1 / valor
    valores, vetores = np.linalg.eig(matriz)
    k = int(np.argmax(valores.real))
    pesos = np.abs(vetores[:, k].real)
    return pesos / pesos.sum(), ((valores[k].real - n) / (n - 1)) / INDICE_ALEATORIO[n]


def ler_pesos(texto):
    """Pesos do engenheiro na ordem de CRITERIOS, separados por vírgula; normalizados para somar 1."""
    if texto is None:
        return None
    partes = texto.split(',')
    valores = [float(p) for p in partes]
    if len(valores) != len(IDS) or not all(math.isfinite(v) and 0 <= v <= 100 for v in valores) or sum(valores) <= 0:
        raise ValueError('Pesos inválidos')
    return np.array(valores) / sum(valores)


def soma_janela(matriz, raio):
    """Soma de cada janela quadrada (2·raio+1) por imagem integral, sem dependências extras."""
    p = np.pad(matriz, ((raio + 1, raio), (raio + 1, raio)))
    c = p.cumsum(0).cumsum(1)
    n = 2 * raio + 1
    return c[n:, n:] - c[:-n, n:] - c[n:, :-n] + c[:-n, :-n]


def preparar_calculo(dados):
    """Mede, uma vez por coleta, fatores e restrições de cada célula da área minerada (30 m, MapBiomas)."""
    mineracao = dados.get('area_minerada')
    if mineracao is None:
        raise ValueError('Área minerada indisponível')
    cobertura = next(b for b in dados['bases'] if chave_base(b) == 'raster_vegetacao')
    grade = dados['grades'][cobertura['base']['id']]
    codigos = [c['codigo'] for c in cobertura['classes'] if 'minera' in normalizar(c['nome'])]
    lin, col = np.nonzero(grade['validos'] & np.isin(grade['valores'], codigos))
    xs, ys = (np.asarray(v) for v in grade['transform'] @ (col + .5, lin + .5))
    ex, ny = (np.asarray(v) for v in transform(grade['crs'], UTM, xs, ys))
    area = grade['area'][lin, col]
    pontos = shapely.points(ex, ny)

    def feicoes(chave):
        return [x for b in dados['bases'] if b['tipo'] == 'vetor' and chave_base(b) == chave for x in b['dados']['features']]

    def distancia(fs):
        saida = np.full(len(ex), np.inf)
        if fs:
            indices, d = shapely.STRtree([projetar(x['geometry']) for x in fs]).query_nearest(pontos, return_distance=True, all_matches=False)
            saida[indices[0]] = d
        return saida

    def dentro(fs):
        return shapely.contains_xy(unary_union([projetar(x['geometry']) for x in fs]), ex, ny) if fs else np.zeros(len(ex), bool)

    relevo = next((b for b in dados['bases'] if chave_base(b) == 'raster_relevo'), None)
    classe = np.zeros(len(ex), dtype=int)
    if relevo is not None and relevo['base']['id'] in dados['grades']:
        topo = dados['grades'][relevo['base']['id']]
        tx, ty = (np.asarray(v) for v in transform(grade['crs'], topo['crs'], xs, ys))
        c, r = (np.floor(np.asarray(v)).astype(int) for v in ~topo['transform'] @ (tx, ty))
        ok = (r >= 0) & (r < topo['valores'].shape[0]) & (c >= 0) & (c < topo['valores'].shape[1])
        classe[ok] = np.where(topo['validos'][r[ok], c[ok]], topo['valores'][r[ok], c[ok]], 0)
    nativos = [c['codigo'] for c in cobertura['classes'] if NATIVA.search(normalizar(c['nome']))]
    raio = 16  # janela de 33 células, cerca de 1 km
    fracao = (soma_janela((grade['validos'] & np.isin(grade['valores'], nativos)).astype(float), raio)
              / np.maximum(soma_janela(grade['validos'].astype(float), raio), 1))[lin, col]
    variaveis = {'relevo': classe, 'vegetacao': fracao, 'drenagem': distancia(feicoes('enq_corpos') or feicoes('hidrografia_principal')),
                 'acesso': distancia(feicoes('rodovias')), 'urbano': distancia(feicoes('areas_urbanizadas')),
                 'rede': distancia(feicoes('linhas_transmissao')), 'trilhas': distancia(feicoes('trilhas'))}
    ucs = [x for x in feicoes('unidades_conservacao') if normalizar(x['properties'].get('grupo')) == 'protecao integral']
    visitacao = [x for x in ucs if normalizar(x['properties'].get('categoria')).startswith(('par', 'mona', 'monumento'))]
    restricao = {'pi_restrita': dentro([x for x in ucs if x not in visitacao]), 'pi_visitacao': dentro(visitacao),
                 'app': dentro(feicoes('apps_fbds')), 'zas': dentro(feicoes('zas_pae')), 'agua': dentro(feicoes('massa_dagua'))}
    permitido = {}
    for uso in USOS:
        livre = np.ones(len(ex), bool)
        for r in RESTRICOES:
            if uso['id'] not in r['permite']:
                livre &= ~restricao[r['id']]
        permitido[uso['id']] = livre

    # Fechamento de 30 m une células vizinhas na diagonal; setores menores que o mínimo ficam fora da sugestão.
    fechado = mineracao['utm'].buffer(30).buffer(-30)
    candidatos = sorted(getattr(fechado, 'geoms', [fechado]), key=lambda p: -p.area)
    setor, partes = np.full(len(ex), -1), []
    for parte in candidatos:
        sel = (setor < 0) & shapely.contains_xy(parte, ex, ny)
        if area[sel].sum() / 1e4 >= MINIMO_HA:
            setor[sel] = len(partes)
            partes.append(parte)
    altos = [x for x in feicoes('cavidades') if normalizar(x['properties'].get('grau_de_po')) in ('alto', 'muito alto')]
    cavidade = dentro(altos)
    cava = projetar(next(f['geometry'] for f in dados['influencia']['features'] if f['properties']['id'] == 'mina'))
    barragens = [(projetar(x['geometry']), x['properties']) for x in feicoes('barragens')]

    fatores = {u: {c: RESPOSTAS[u][c](variaveis[c]) for c in RESPOSTAS[u]} for u in RESPOSTAS}
    setores = []
    for i, parte in enumerate(partes):
        sel = setor == i
        peso = area[sel] / area[sel].sum()
        media = {u: {c: float((peso * permitido[u][sel] * f[sel]).sum()) for c, f in fatores[u].items()} for u in fatores}
        bloqueio = {u: {r['id']: float((peso * restricao[r['id']][sel]).sum()) for r in RESTRICOES if u not in r['permite']} for u in fatores}
        proprias = [p for g, p in barragens if parte.buffer(30).intersects(g)]
        # Perfil físico do setor, em unidades do terreno, para explicar a sugestão sem falar em pontos.
        classes = classe[sel]
        perfil = {'ate8': float((peso * np.isin(classes, (1, 2))).sum()), 'de8a20': float((peso * (classes == 3)).sum()),
                  'acima20': float((peso * (classes >= 4)).sum()), 'acima45': float((peso * (classes >= 5)).sum()),
                  'vegetacao': float((peso * fracao[sel]).sum()),
                  'distancias': {c: (float(np.median(variaveis[c][sel])) if np.isfinite(variaveis[c][sel]).any() else None)
                                 for c in ('drenagem', 'acesso', 'urbano', 'rede', 'trilhas')}}
        setores.append({
            'id': f'S{i + 1}', 'ha': float(area[sel].sum() / 1e4), 'media': media, 'bloqueio': bloqueio, 'perfil': perfil,
            'permitido': {u: float((peso * permitido[u][sel]).sum()) for u in permitido},
            'restricoes': {r['id']: float((peso * restricao[r['id']][sel]).sum()) for r in RESTRICOES},
            'cavidades': float((peso * cavidade[sel]).sum()), 'cava_ha': parte.intersection(cava).area / 1e4,
            'barragens': [str(p.get('name') or p.get('nome_estru')) for p in proprias],
            'montante': [str(p.get('name') or p.get('nome_estru')) for p in proprias if normalizar(p.get('metodo_con')) == 'montante'],
            'geometria': transform_geom(UTM, 'EPSG:4326', mapping(parte.simplify(15))),
        })
    return {'setores': setores, 'area_minerada_ha': mineracao['ha'],
            'fora_ha': float(area[setor < 0].sum() / 1e4), 'celulas': int(len(ex))}


def notas(setor, pesos):
    """Soma ponderada normalizada pelos critérios que participam de cada uso; restrição vale zero."""
    saida = {}
    for uso in USOS:
        u = uso['id']
        total = sum(pesos[IDS.index(c)] for c in RESPOSTAS[u])
        saida[u] = 100 * (sum(pesos[IDS.index(c)] * v for c, v in setor['media'][u].items()) / total if total else setor['permitido'][u])
    return saida


def calcular(base, pesos=None):
    """Ordena os usos de cada setor e testa se o primeiro lugar resiste a ±20% em cada peso."""
    ahp, consistencia = pesos_ahp()
    w = ahp if pesos is None else pesos
    resultado = {'criterios': [{**c, 'peso': float(w[i]), 'peso_ahp': float(ahp[i])} for i, c in enumerate(CRITERIOS)],
                 'origem_pesos': 'AHP' if pesos is None else 'engenheiro', 'razao_consistencia': float(consistencia),
                 'usos': USOS, 'restricoes': RESTRICOES, 'minimo_ha': MINIMO_HA, 'variacao': VARIACAO,
                 'area_minerada_ha': base['area_minerada_ha'], 'fora_ha': base['fora_ha'], 'setores': []}
    for s in base['setores']:
        nota = notas(s, w)
        ordem = sorted(USOS, key=lambda u: -nota[u['id']])
        muda = []
        for i, criterio in enumerate(CRITERIOS):
            for fator in (1 - VARIACAO, 1 + VARIACAO):
                teste = w.copy()
                teste[i] *= fator
                outra = notas(s, teste / teste.sum())
                if max(outra, key=outra.get) != ordem[0]['id']:
                    muda.append(f"{criterio['curto']} {'-' if fator < 1 else '+'}{round(VARIACAO * 100)}%")
        total = {u: sum(w[IDS.index(c)] for c in RESPOSTAS[u]) for u in RESPOSTAS}
        contribuicoes = {u['id']: {c: 100 * w[IDS.index(c)] * v / total[u['id']] for c, v in s['media'][u['id']].items()} if total[u['id']] else {}
                         for u in USOS}
        estruturas = (['inclui a cava (OSM)'] if s['cava_ha'] >= 1 else []) + \
                     (['barragens ' + ', '.join(b.split(' - ')[0] for b in s['barragens'])] if s['barragens'] else [])
        resultado['setores'].append({
            'id': s['id'], 'ha': s['ha'], 'descricao': '; '.join(estruturas),
            'ranking': [{'uso': u['id'], 'nome': u['nome'], 'cor': u['cor'], 'nota': nota[u['id']], 'permitido': 100 * s['permitido'][u['id']]} for u in ordem],
            'margem': nota[ordem[0]['id']] - nota[ordem[1]['id']], 'contribuicoes': contribuicoes,
            'bloqueio': {u: {r: 100 * v for r, v in b.items()} for u, b in s['bloqueio'].items()},
            'restricoes': {r: 100 * v for r, v in s['restricoes'].items()}, 'cavidades': 100 * s['cavidades'],
            'barragens': s['barragens'], 'montante': s['montante'], 'robustez': {'estavel': not muda, 'muda_com': muda},
            'perfil': {'declividade': {k: 100 * s['perfil'][k] for k in ('ate8', 'de8a20', 'acima20', 'acima45')},
                       'vegetacao': 100 * s['perfil']['vegetacao'], 'distancias': s['perfil']['distancias']},
            'fatores': {u: {c: v / max(s['permitido'][u], 1e-9) for c, v in s['media'][u].items()} for u in RESPOSTAS},
            'geometria': s['geometria'],
        })
    return resultado


def distancia(metros):
    return f"{formato(round(metros, -1))} m" if metros < 1000 else f"{formato(metros / 1000, 1)} km"


# Usos para os quais estar longe é o desejável; nos demais pares, quanto mais perto, melhor.
LONGE = {('conservacao', 'urbano'), ('silvicultura', 'drenagem'), ('solar', 'drenagem')}
LUGARES = {'drenagem': 'o curso d’água principal', 'acesso': 'a rodovia', 'urbano': 'a área urbana',
           'rede': 'a linha de transmissão', 'trilhas': 'a trilha cadastrada'}


def parcela(pct, resto, pouco=False):
    """“62% do setor tem …”; com `pouco`, marca a falta (“só 3%”, “quase nada”)."""
    if pouco and pct < .5:
        return f"quase nada do setor tem {resto}"
    return f"{'só ' if pouco and pct < 50 else ''}{formato(pct)}% do setor tem {resto}"


def descrever(criterio, uso, perfil, contra=False):
    """O critério em unidades do terreno, na faixa que importa para o uso; `contra` descreve o que falta (ex.: solar quer declividade abaixo de 8%)."""
    d = perfil['declividade']
    ate20 = d['ate8'] + d['de8a20']
    if criterio == 'relevo':
        if uso == 'conservacao':
            return parcela(d['acima20'], 'declividade acima de 20%', contra)
        if uso == 'ecoturismo':
            return parcela(d['acima45'], 'declividade acima de 45%') if contra else parcela(ate20 + d['acima20'] - d['acima45'], 'declividade até 45%')
        if uso == 'silvicultura':
            return parcela(d['acima20'], 'declividade acima de 20%') if contra else parcela(ate20, 'declividade até 20%')
        return parcela(d['ate8'], 'declividade abaixo de 8%', contra)
    if criterio == 'vegetacao':
        return f"a vegetação nativa cobre {'só ' if contra else ''}{formato(perfil['vegetacao'])}% do entorno de 1 km"
    metros = perfil['distancias'][criterio]
    if metros is None:
        return f"não há {LUGARES[criterio].split(' ', 1)[1]} no recorte"
    longe = ((uso, criterio) in LONGE) != contra
    return f"{LUGARES[criterio]} fica {'longe' if longe else 'perto'}, a {distancia(metros)}"


# O que cada fato significa para cada uso, a favor e contra; é o que transforma número em explicação.
SENTIDO = {
    ('relevo', 'conservacao'): ('dificulta máquinas e favorece deixar a vegetação voltar', 'pouca encosta para deixar regenerar sozinha'),
    ('relevo', 'ecoturismo'): ('relevo que ainda permite trilhas e visitação', 'encostas fortes demais para trilhas'),
    ('relevo', 'silvicultura'): ('permite plantio e colheita mecanizados', 'encostas dificultam plantio e colheita mecanizados'),
    ('relevo', 'solar'): ('terreno plano para painéis', 'painéis precisam de terreno quase plano'),
    ('vegetacao', 'conservacao'): ('fonte de sementes e fauna para a restauração', 'pouca fonte de sementes e fauna para a restauração'),
    ('vegetacao', 'ecoturismo'): ('paisagem natural para visitação', 'pouca paisagem natural para visitação'),
    ('drenagem', 'conservacao'): ('favorece recompor a mata ciliar', 'longe da água para recompor mata ciliar'),
    ('drenagem', 'ecoturismo'): ('água como atrativo', 'sem água próxima como atrativo'),
    ('drenagem', 'silvicultura'): ('sem conflito com a faixa do rio', 'plantio perto demais da faixa do rio'),
    ('drenagem', 'solar'): ('sem conflito com a faixa do rio', 'painéis perto demais da faixa do rio'),
    ('acesso', 'ecoturismo'): ('facilita receber visitantes', 'dificulta receber visitantes'),
    ('acesso', 'silvicultura'): ('facilita escoar a madeira', 'encarece escoar a madeira'),
    ('acesso', 'solar'): ('facilita obra e manutenção', 'encarece obra e manutenção'),
    ('urbano', 'conservacao'): ('menos pressão sobre a área restaurada', 'mais pressão urbana sobre a área'),
    ('urbano', 'ecoturismo'): ('público por perto', 'público distante'),
    ('urbano', 'solar'): ('consumo de energia por perto', 'consumo de energia distante'),
    ('rede', 'solar'): ('facilita conectar a energia', 'conexão à rede distante'),
    ('trilhas', 'ecoturismo'): ('já há caminho para visitantes', 'sem rede de trilhas por perto'),
}


def explicado(criterio, uso, perfil, contra=False):
    """Fato do terreno seguido do que ele significa para o uso."""
    sentido = SENTIDO.get((criterio, uso))
    fato = descrever(criterio, uso, perfil, contra)
    return f"{fato} ({sentido[1 if contra else 0]})" if sentido else fato


def motivos(setor, resultado):
    """Fatos do terreno que explicam o ranking: o que distingue o 1º uso do 2º e o que segura cada um dos outros."""
    pesos = {c['id']: c['peso'] for c in resultado['criterios']}
    restricoes = {r['id']: r for r in resultado['restricoes']}
    nomes = {u['id']: u['nome'].split(' e ')[0].lower() for u in resultado['usos']}
    perfil, fatores = setor['perfil'], setor['fatores']
    primeiro, segundo = setor['ranking'][0]['uso'], setor['ranking'][1]['uso']
    f1, f2 = fatores[primeiro], fatores[segundo]
    escolhidos = sorted((c for c in f1 if f1[c] >= .5), key=lambda c: -pesos[c] * (f1[c] - f2.get(c, 0)))[:2] \
        or sorted(f1, key=lambda c: -pesos[c] * f1[c])[:1]
    favor = [explicado(c, primeiro, perfil) for c in escolhidos]
    # Restrição que cobre boa parte do setor e admite o 1º uso também explica a escolha.
    legal = max(((r, v) for r, v in setor['restricoes'].items() if v >= 20 and primeiro in restricoes[r]['permite']), key=lambda i: i[1], default=None)
    if legal:
        r = restricoes[legal[0]]
        favor.append(f"{formato(legal[1])}% do setor é {r['curto']}, onde só {' e '.join(nomes[u] for u in r['permite'])} são permitidos")
    outros = []
    for uso in setor['ranking'][1:]:
        if setor['ranking'][0]['nota'] - uso['nota'] < 2:
            outros.append((uso['nome'], None))
            continue
        contra = []
        if uso['permitido'] < 90:
            barreira = max(setor['bloqueio'][uso['uso']].items(), key=lambda i: i[1])[0]
            contra.append(f"a lei não permite em {formato(100 - uso['permitido'])}% do setor ({restricoes[barreira]['curto']})")
        pior = max(fatores[uso['uso']], key=lambda c: pesos[c] * (1 - fatores[uso['uso']][c]))
        if fatores[uso['uso']][pior] < .7:
            contra.append(descrever(pior, uso['uso'], perfil, contra=True))
        if contra:
            outros.append((uso['nome'], contra))
    return {'favor': favor, 'outros': outros}


def frase_demais(m):
    """O que segura cada um dos outros usos, sempre por regras: é onde o modelo mais trocava números."""
    partes = [f"{nome[0].lower() + nome[1:]} quase empata, e a escolha entre os dois depende da prioridade dada aos critérios" if contra is None
              else f"{nome[0].lower() + nome[1:]}, porque {' e '.join(contra)}" for nome, contra in m['outros']]
    return f"Os demais ficam atrás: {'; '.join(partes)}." if partes else ''


def explicar_por_regras(setor, resultado):
    """Explicação determinística pelo território, montada com os mesmos motivos enviados à IA."""
    m = motivos(setor, resultado)
    return f"{setor['ranking'][0]['nome']}: {' e '.join(m['favor'])}. {frase_demais(m)}".strip()


class SugestoesUso:
    """Guarda o cálculo por coleta; mudar pesos só refaz a soma ponderada."""

    def __init__(self, fonte):
        self.fonte = fonte
        self.cache = {}
        self.trava = threading.Lock()

    def base(self, mina_id, dados=None):
        """Reaproveita dados já preparados pelo relatório; sem eles, lê o banco e mede as grades."""
        dados = dados if dados is not None else self.fonte.relatorio(mina_id)
        chave = hashlib.sha256(json.dumps([(b['base']['camada'], b['consultado_em'], b['recorte']['assinatura']) for b in dados['bases']],
                                          sort_keys=True).encode()).hexdigest()
        with self.trava:
            if self.cache.get(mina_id, (None,))[0] == chave:
                return self.cache[mina_id][1]
        if 'grades' not in dados:
            dados['rasters'] = {b['base']['id']: self.fonte.arquivo(mina_id, b['base']['id']) for b in dados['bases'] if b['tipo'] == 'raster'}
            preparar(dados)
        calculo = preparar_calculo(dados)
        with self.trava:
            self.cache[mina_id] = (chave, calculo)
        return calculo

    def obter(self, mina_id, pesos=None, dados=None):
        resultado = calcular(self.base(mina_id, dados), pesos)
        for setor in resultado['setores']:
            setor['explicacao'] = explicar_por_regras(setor, resultado)
        return resultado


def entrada_ia(resultado):
    """Para o modelo, o uso sugerido e os fatos a favor já escolhidos pela regra; a frase sobre os demais usos vem das regras."""
    return {'setores': [{'id': s['id'], 'uso sugerido': s['ranking'][0]['nome'], 'a favor': motivos(s, resultado)['favor']}
                        for s in resultado['setores']]}


def demais_por_setor(resultado):
    return {s['id']: frase_demais(motivos(s, resultado)) for s in resultado['setores']}


def resumo_pesos(resultado):
    return '; '.join(f"{c['nome']}: {formato(100 * c['peso'])}%" for c in resultado['criterios'])


def texto_setor(setor):
    linhas = [f"{i}º {u['nome']}: {formato(u['nota'])}" + ('' if u['permitido'] >= 99.5 else f" (lei permite em {formato(u['permitido'])}% da área)")
              for i, u in enumerate(setor['ranking'], 1)]
    return '\n'.join(linhas)


def nome_setor(setor):
    return f"{setor['id']} · {ha(setor['ha'])}" + (f" · {setor['descricao']}" if setor['descricao'] else '')
