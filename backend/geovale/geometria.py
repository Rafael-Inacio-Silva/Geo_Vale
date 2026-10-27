"""Operações de recorte que conservam a dimensão das feições."""
from shapely import get_parts


def partes_da_dimensao(geom, tipos):
    """Mantém componentes da dimensão original; contato pontual não vira trecho ou superfície."""
    if geom.is_empty:
        return []
    if geom.geom_type in tipos:
        return [geom]
    if geom.geom_type == 'GeometryCollection':
        return [p for grupo in get_parts(geom) for p in partes_da_dimensao(grupo, tipos)]
    return []


