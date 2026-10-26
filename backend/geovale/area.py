"""Validação geométrica do recorte manual, sem certificação de limites ou persistência."""

import math
from shapely.geometry import Polygon


class AreaInvalida(ValueError):
    """Indica um contorno que precisa ser corrigido pela pessoa que o desenhou."""


def validar_area(documento):
    """Aceita um Polygon simples GeoJSON com um anel fechado e até 500 vértices."""
    erro = 'Desenhe um contorno fechado com pelo menos três pontos distintos.'
    if not isinstance(documento, dict) or documento.get('type') != 'Feature':
        raise AreaInvalida(erro)
    geometria = documento.get('geometry')
    if not isinstance(geometria, dict) or geometria.get('type') != 'Polygon':
        raise AreaInvalida('A área deve ser um único polígono.')
    aneis = geometria.get('coordinates')
    if not isinstance(aneis, list) or len(aneis) != 1 or not isinstance(aneis[0], list):
        raise AreaInvalida('Use um contorno simples, sem recortes internos.')
    anel = aneis[0]
    if not 4 <= len(anel) <= 501:
        raise AreaInvalida('Use entre 3 e 500 pontos no contorno.')
    for ponto in anel:
        if not isinstance(ponto, list) or len(ponto) != 2:
            raise AreaInvalida(erro)
        if any(type(v) not in (int, float) or (type(v) is float and not math.isfinite(v)) for v in ponto):
            raise AreaInvalida('As coordenadas do contorno são inválidas.')
        if not -180 <= ponto[0] <= 180 or not -85 <= ponto[1] <= 85:
            raise AreaInvalida('O contorno está fora da extensão suportada pelo mapa.')
    if anel[0] != anel[-1] or len({tuple(p) for p in anel[:-1]}) < 3:
        raise AreaInvalida(erro)
    if any(abs(a[0] - b[0]) > 180 for a, b in zip(anel, anel[1:])):
        raise AreaInvalida('Desenhe uma área sem atravessar a borda mundial do mapa.')
    poligono = Polygon(anel)
    if poligono.is_empty or not poligono.is_valid or poligono.area <= 0:
        raise AreaInvalida('O contorno se cruza ou não forma uma superfície. Ajuste os pontos.')
    return {
        'type': 'Feature', 'geometry': {'type': 'Polygon', 'coordinates': [anel]},
        'properties': {'origem': 'desenho_manual', 'finalidade': 'area_de_estudo', 'vertices': len(anel) - 1},
    }
