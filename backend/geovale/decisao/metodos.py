"""AHP por autovetor principal e TOPSIS vetorial com trilha de cálculo explícita."""
from math import isfinite
import numpy as np

RI = {1: 0.0, 2: 0.0, 3: 0.58, 4: 0.90, 5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49}


class ErroDecisao(ValueError):
    """Recusa dados incompletos ou inconsistentes antes de gerar uma classificação."""


def numeros(valores, dimensao: int) -> np.ndarray:
    """Aceita somente números JSON finitos; booleanos não representam avaliações."""
    def verificar(v):
        """Confere recursivamente os valores antes da conversão NumPy."""
        if isinstance(v, (list, tuple)):
            return all(verificar(i) for i in v)
        try:
            return type(v) in (int, float) and isfinite(v)
        except OverflowError:
            return False
    if not verificar(valores):
        raise ErroDecisao('Informe apenas números finitos, sem campos vazios.')
    try:
        matriz = np.asarray(valores, dtype=float)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ErroDecisao('A matriz deve ter linhas de mesmo tamanho.') from exc
    if matriz.ndim != dimensao or not np.all(np.isfinite(matriz)):
        raise ErroDecisao('Formato numérico incompatível.')
    return matriz


def calcular_ahp(comparacoes: list[list[float]]) -> dict:
    """Obtém pesos relativos, lambda máximo, CI e CR; não atribui autoria técnica aos julgamentos."""
    a = numeros(comparacoes, 2)
    n = a.shape[0]
    if a.shape != (n, n) or n not in RI or n < 2 or np.any(a < 1/9 - 1e-12) or np.any(a > 9 + 1e-12):
        raise ErroDecisao('AHP exige matriz quadrada de 2 a 10 critérios, com valores de 1/9 a 9.')
    if not np.allclose(np.diag(a), 1, atol=1e-10, rtol=0) or not np.allclose(a * a.T, 1, atol=1e-9, rtol=0):
        raise ErroDecisao('As comparações devem ser recíprocas e a diagonal deve ser 1.')
    valores, vetores = np.linalg.eig(a)
    indice = int(np.argmax(valores.real))
    pesos = np.abs(vetores[:, indice].real)
    pesos = pesos / pesos.sum()
    lambda_max = float(np.mean((a @ pesos) / pesos))
    ci = max(0.0, (lambda_max - n)/(n - 1))
    cr = ci/RI[n] if RI[n] else 0.0
    return {'metodo': 'AHP-autovetor', 'matriz': a.tolist(), 'pesos': pesos.tolist(),
            'lambda_max': lambda_max, 'indice_consistencia': ci, 'razao_consistencia': cr,
            'consistente': cr <= 0.10 + 1e-12,
            'aviso': 'Consistência matemática não comprova validade técnica dos julgamentos.'}


def validar_pesos(valores: list[float], quantidade: int) -> np.ndarray:
    """Exige pesos não negativos que somem 100%; não corrige silenciosamente a entrada."""
    p = numeros(valores, 1)
    if len(p) != quantidade or np.any(p < 0) or not np.isclose(p.sum(), 100.0, atol=1e-8, rtol=0):
        raise ErroDecisao('Os pesos devem somar 100%, sem valores negativos.')
    return p / 100.0


def calcular_topsis(matriz: list[list[float]], pesos: list[float], sentidos: list[str]) -> dict:
    """Normaliza vetores, aplica pesos e mede distâncias aos ideais sem converter resultado em probabilidade."""
    x = numeros(matriz, 2)
    if x.shape[0] < 2 or not 1 <= x.shape[1] <= 10 or np.any(x < 0) or len(sentidos) != x.shape[1] or any(s not in ('beneficio', 'custo') for s in sentidos):
        raise ErroDecisao('TOPSIS exige ao menos duas alternativas e critérios não negativos com sentido definido.')
    w = validar_pesos(pesos, x.shape[1])
    normas = np.linalg.norm(x, axis=0)
    normalizada = np.divide(x, normas, out=np.zeros_like(x), where=normas > 0)
    ponderada = normalizada * w
    melhor = np.array([np.max(ponderada[:,j]) if s == 'beneficio' else np.min(ponderada[:,j]) for j,s in enumerate(sentidos)])
    pior = np.array([np.min(ponderada[:,j]) if s == 'beneficio' else np.max(ponderada[:,j]) for j,s in enumerate(sentidos)])
    dp = np.linalg.norm(ponderada - melhor, axis=1)
    dn = np.linalg.norm(ponderada - pior, axis=1)
    totais = dp + dn
    escores = np.divide(dn, totais, out=np.full(x.shape[0], 0.5), where=totais > 1e-15)
    ordem = sorted(range(len(escores)), key=lambda i: (-round(float(escores[i]), 10), i))
    posicoes = [0] * len(escores)
    for k, i in enumerate(ordem):
        posicoes[i] = posicoes[ordem[k-1]] if k and abs(escores[i] - escores[ordem[k-1]]) <= 1e-10 else k + 1
    return {'metodo': 'TOPSIS-vetorial-1.0', 'matriz': x.tolist(), 'pesos_percentuais': (w*100).tolist(),
            'sentidos': sentidos, 'normalizada': normalizada.tolist(), 'ponderada': ponderada.tolist(),
            'ideal_positivo': melhor.tolist(), 'ideal_negativo': pior.tolist(),
            'distancia_positiva': dp.tolist(), 'distancia_negativa': dn.tolist(),
            'escores': escores.tolist(), 'posicoes': posicoes, 'ordem': ordem,
            'sem_discriminacao': bool(np.allclose(escores, escores[0], atol=1e-10, rtol=0)),
            'colunas_nulas': np.where(normas == 0)[0].tolist()}


def analisar_sensibilidade(matriz: list[list[float]], pesos: list[float], sentidos: list[str]) -> dict:
    """Varia cada peso em dez pontos percentuais redistribuindo os demais, mantendo a soma em 100%."""
    base = calcular_topsis(matriz, pesos, sentidos)
    lideres_base = {i for i, p in enumerate(base['posicoes']) if p == 1}
    cenarios = []
    for j in range(len(pesos)):
        for delta in (-10.0, 10.0):
            novo = pesos[j] + delta
            if not 0 <= novo <= 100:
                continue
            outros = sum(pesos[k] for k in range(len(pesos)) if k != j)
            if outros == 0 and novo < 100:
                continue
            p = [v*(100-novo)/outros if k != j and outros else 0.0 for k,v in enumerate(pesos)]
            p[j] = novo
            r = calcular_topsis(matriz, p, sentidos)
            lideres = [i for i, pos in enumerate(r['posicoes']) if pos == 1]
            cenarios.append({'criterio': j, 'variacao_pp': delta, 'pesos': p, 'lideres': lideres,
                             'mudou_lideranca': set(lideres) != lideres_base})
    return {'variacao_pontos_percentuais': 10, 'cenarios': cenarios,
            'mudou_em': sum(c['mudou_lideranca'] for c in cenarios),
            'aviso': 'Teste local de pesos; não é intervalo de confiança nem validação de campo.'}
