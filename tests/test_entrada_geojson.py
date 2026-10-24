"""Aceitação CT-01: mapas reais, limites inclusivos e rejeição sem correção."""

import copy
import hashlib
import json
import math
from pathlib import Path

import pytest

from geovale.geografia.entrada import ErroEntrada, MAX_BYTES, validar_geojson

RAIZ = Path(__file__).resolve().parents[1]
MAPA_REAL = RAIZ / "tests/fixtures/il087.geojson"
ANEL = [[0, 0], [2, 0], [2, 2], [0, 2], [0, 0]]


def documento(coordenadas=None, tipo="Polygon"):
    """Monta entrada mínima; coordenadas de teste não são dados científicos."""
    return {"type": "FeatureCollection", "features": [{"type": "Feature", "properties": None, "geometry": {"type": tipo, "coordinates": copy.deepcopy(coordenadas if coordenadas is not None else [ANEL])}}]}


def codificar(objeto):
    """Converte um documento de controle em bytes UTF-8."""
    return json.dumps(objeto, separators=(",", ":")).encode()


def circulo(quantidade, centro=0, raio=1):
    """Gera contorno válido com quantidade exata de posições, incluindo fechamento."""
    pontos = [[round(centro + raio * math.cos(2 * math.pi * i / (quantidade - 1)), 12), round(raio * math.sin(2 * math.pi * i / (quantidade - 1)), 12)] for i in range(quantidade - 1)]
    return pontos + [pontos[0].copy()]


def test_mapa_real_preserva_todas_as_partes():
    """O caso IL_087 mantém três partes, 68 posições e hash dos bytes recebidos."""
    conteudo = MAPA_REAL.read_bytes()
    resultado = validar_geojson(conteudo, "area.geojson")
    assert (resultado.numero_partes, resultado.numero_posicoes, resultado.numero_aneis) == (3, 68, 3)
    assert resultado.tamanho_bytes == 2829
    assert resultado.sha256 == hashlib.sha256(conteudo).hexdigest()
    assert resultado.documento == json.loads(conteudo)


@pytest.mark.parametrize("coordenadas,tipo,partes,aneis", [
    ([ANEL], "Polygon", 1, 1),
    ([list(reversed(ANEL))], "Polygon", 1, 1),
    ([ANEL, [[.5,.5],[.5,1],[1,1],[1,.5],[.5,.5]]], "Polygon", 1, 2),
    ([[ANEL], [[[2,2],[3,2],[3,3],[2,3],[2,2]]]], "MultiPolygon", 2, 2),
    ([[[0,0,5],[2,0],[2,2,9],[0,2],[0,0,5]]], "Polygon", 1, 1),
    ([[[-180,-90],[180,-90],[180,90],[-180,90],[-180,-90]]], "Polygon", 1, 1),
])
def test_superficies_validas_preservadas(coordenadas, tipo, partes, aneis):
    """Aceita orientação inversa, vazios, contato pontual e posições 2D/3D."""
    original = documento(coordenadas, tipo)
    resultado = validar_geojson(codificar(original), "AREA.GEOJSON")
    assert resultado.documento == original
    assert (resultado.numero_partes, resultado.numero_aneis) == (partes, aneis)


def test_limite_bytes_inclusivo():
    """Aceita exatamente 1 MiB e rejeita um byte adicional sem truncamento."""
    conteudo = codificar(documento())
    exato = conteudo + b" " * (MAX_BYTES - len(conteudo))
    assert validar_geojson(exato, "a.geojson").tamanho_bytes == MAX_BYTES
    with pytest.raises(ErroEntrada, match="1 MiB") as erro:
        validar_geojson(exato + b" ", "a.geojson")
    assert erro.value.status == 413


@pytest.mark.parametrize("partes", [1, 5])
def test_limite_posicoes_inclusivo_e_global(partes):
    """Conta todos os fechamentos e todas as partes, aceitando 20.000 no total."""
    aneis = [[circulo(20_000 // partes, centro=4*i)] for i in range(partes)]
    original = documento(aneis, "MultiPolygon")
    conteudo = codificar(original)
    assert len(conteudo) <= MAX_BYTES
    assert validar_geojson(conteudo, "a.geojson").numero_posicoes == 20_000
    original["features"][0]["geometry"]["coordinates"][0] = [circulo(20_000 // partes + 1)]
    with pytest.raises(ErroEntrada) as erro:
        validar_geojson(codificar(original), "a.geojson")
    assert erro.value.codigo == "POSICOES_EXCEDIDAS"


@pytest.mark.parametrize("alteracao,codigo", [
    (lambda d: d.update(type="Feature"), "COLECAO_INVALIDA"),
    (lambda d: d.pop("features"), "QUANTIDADE_FEATURES"),
    (lambda d: d.update(features=[]), "QUANTIDADE_FEATURES"),
    (lambda d: d["features"].append(copy.deepcopy(d["features"][0])), "QUANTIDADE_FEATURES"),
    (lambda d: d.update(features={}), "QUANTIDADE_FEATURES"),
    (lambda d: d.update(features=[None]), "FEATURE_INVALIDA"),
    (lambda d: d["features"][0].update(type="Polygon"), "FEATURE_INVALIDA"),
    (lambda d: d["features"][0].pop("properties"), "ATRIBUTOS_INVALIDOS"),
    (lambda d: d["features"][0].update(properties=[]), "ATRIBUTOS_INVALIDOS"),
    (lambda d: d["features"][0].update(geometry=None), "GEOMETRIA_INCOMPATIVEL"),
    (lambda d: d["features"][0]["geometry"].pop("coordinates"), "COORDENADAS_INVALIDAS"),
    (lambda d: d["features"][0]["geometry"].update(coordinates=[]), "COORDENADAS_INVALIDAS"),
    (lambda d: d["features"][0]["geometry"].update(coordinates=[[]]), "COORDENADAS_INVALIDAS"),
    (lambda d: d["features"][0]["geometry"].update(coordinates=ANEL), "ANEL_CURTO"),
    (lambda d: d.update(crs={"type":"name", "properties":{"name":"EPSG:3857"}}), "CRS_LEGADO"),
])
def test_estrutura_invalida(alteracao, codigo):
    """Recusa estrutura incompleta ou ambígua e CRS legado sem reinterpretação."""
    original = documento()
    alteracao(original)
    with pytest.raises(ErroEntrada) as erro:
        validar_geojson(codificar(original), "a.geojson")
    assert erro.value.codigo == codigo


@pytest.mark.parametrize("tipo", ["Point", "MultiPoint", "LineString", "MultiLineString", "GeometryCollection", "polygon", None])
def test_tipos_incompativeis(tipo):
    """Só Polygon e MultiPolygon são aceitos, mesmo numa GeometryCollection poligonal."""
    with pytest.raises(ErroEntrada) as erro:
        validar_geojson(codificar(documento(tipo=tipo)), "a.geojson")
    assert erro.value.codigo == "GEOMETRIA_INCOMPATIVEL"


@pytest.mark.parametrize("posicao", [[0], [0,0,0,0], [True,0], [0,False], ["0",0], [None,0], [181,0], [0,-91], [0,0,"a"], [0,0,False], [0,0,10**400]])
def test_posicoes_invalidas(posicao):
    """Texto, booleanos, dimensão excessiva e coordenadas fora do intervalo falham."""
    original = documento()
    original["features"][0]["geometry"]["coordinates"][0][1] = posicao
    with pytest.raises(ErroEntrada):
        validar_geojson(codificar(original), "a.geojson")


@pytest.mark.parametrize("coordenadas,tipo,codigo", [
    ([[[0,0],[1,0],[0,1]]], "Polygon", "ANEL_CURTO"),
    ([[[0,0],[2,0],[2,2],[0,2]]], "Polygon", "ANEL_ABERTO"),
    ([[[0,0,1],[2,0],[2,2],[0,0,2]]], "Polygon", "ANEL_ABERTO"),
    ([[[0,0],[1,0],[0,0],[0,0]]], "Polygon", "VERTICES_INSUFICIENTES"),
    ([[[0,0],[1,1],[2,2],[0,0]]], "Polygon", "GEOMETRIA_INVALIDA"),
    ([[[0,0],[2,2],[0,2],[2,0],[0,0]]], "Polygon", "GEOMETRIA_INVALIDA"),
    ([ANEL, [[3,3],[4,3],[4,4],[3,4],[3,3]]], "Polygon", "GEOMETRIA_INVALIDA"),
    ([[ANEL], [[[1,1],[3,1],[3,3],[1,3],[1,1]]]], "MultiPolygon", "GEOMETRIA_INVALIDA"),
    ([[ANEL], [[[2,0],[3,0],[3,2],[2,2],[2,0]]]], "MultiPolygon", "GEOMETRIA_INVALIDA"),
])
def test_topologia_invalida_sem_reparacao(coordenadas, tipo, codigo):
    """Nenhum anel é fechado automaticamente, unido, reparado ou simplificado."""
    original = documento(coordenadas, tipo)
    antes = copy.deepcopy(original)
    with pytest.raises(ErroEntrada) as erro:
        validar_geojson(codificar(original), "a.geojson")
    assert erro.value.codigo == codigo
    assert original == antes


@pytest.mark.parametrize("conteudo", [b"", b" ", b"{", b"\xff", b"[]", b"null", b'{"type":"FeatureCollection","type":"FeatureCollection"}', b'{"n":NaN}', b'{"n":Infinity}', b'{"n":-Infinity}', b'{"n":1e999}', b'{"n":"\\ud800"}', b"["*2000+b"]"*2000])
def test_arquivos_corrompidos_ou_nao_representaveis(conteudo):
    """Falhas de decodificação e JSON excessivamente aninhado viram erro de entrada."""
    with pytest.raises(ErroEntrada):
        validar_geojson(conteudo, "a.geojson")


@pytest.mark.parametrize("nome", ["a.json", "a.geojson.exe", "", "a.zip"])
def test_extensao_nao_basta(nome):
    """Exige extensão e conteúdo do contrato, sem confiar apenas no nome."""
    with pytest.raises(ErroEntrada) as erro:
        validar_geojson(codificar(documento()), nome)
    assert erro.value.codigo == "EXTENSAO_INVALIDA"
