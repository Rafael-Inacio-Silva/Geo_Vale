"""Validação estrita de entrada CT-01, sem reparação ou reprojeção."""

from dataclasses import dataclass
import hashlib
import json
import math
from typing import Any

from shapely.errors import GEOSException
from shapely.geometry import shape

MAX_BYTES = 1_048_576
MAX_POSICOES = 20_000


class ErroEntrada(Exception):
    """Representa uma rejeição compreensível, sem expor o conteúdo recebido."""

    def __init__(self, codigo: str, mensagem: str, campo: str = "arquivo", status: int = 422):
        """Registra causa, localização e código HTTP da falha de entrada."""
        super().__init__(mensagem)
        self.codigo = codigo
        self.mensagem = mensagem
        self.campo = campo
        self.status = status


@dataclass(frozen=True)
class AreaValidada:
    """Mantém documento original interpretado e contagens da única área."""

    documento: dict[str, Any]
    tamanho_bytes: int
    sha256: str
    numero_posicoes: int
    numero_partes: int
    numero_aneis: int
    dimensoes_presentes: tuple[int, ...]


def _objeto_unico(pares: list[tuple[str, Any]]) -> dict[str, Any]:
    """Rejeita chaves JSON duplicadas em vez de escolher um valor silenciosamente."""
    objeto = {}
    for chave, valor in pares:
        if chave in objeto:
            raise ErroEntrada("JSON_AMBIGUO", "O JSON contém uma chave repetida. Corrija o arquivo.", status=400)
        objeto[chave] = valor
    return objeto


def _constante_invalida(valor: str) -> None:
    """Impede as extensões NaN e Infinity que não fazem parte do JSON."""
    raise ErroEntrada("JSON_INVALIDO", "O JSON contém NaN ou infinito. Use valores finitos.", status=400)


def _real_finito(valor: str) -> float:
    """Rejeita também expoentes JSON que excedam a representação numérica."""
    numero = float(valor)
    if not math.isfinite(numero):
        raise ErroEntrada("NUMERO_INVALIDO", "O JSON contém número fora do intervalo finito suportado.", status=400)
    return numero


def _validar_textos(documento: Any) -> None:
    """Recusa escapes Unicode isolados que não podem voltar à resposta UTF-8."""
    pendentes = [documento]
    while pendentes:
        valor = pendentes.pop()
        if isinstance(valor, str):
            try:
                valor.encode("utf-8")
            except UnicodeEncodeError as exc:
                raise ErroEntrada("TEXTO_INVALIDO", "O JSON contém um escape Unicode isolado. Corrija o texto do arquivo.", status=400) from exc
        elif isinstance(valor, dict):
            pendentes.extend(valor.keys())
            pendentes.extend(valor.values())
        elif isinstance(valor, list):
            pendentes.extend(valor)


def _lista(valor: Any, campo: str) -> list:
    """Exige uma lista não vazia em cada nível das coordenadas."""
    if not isinstance(valor, list) or not valor:
        raise ErroEntrada("COORDENADAS_INVALIDAS", "As coordenadas precisam de listas não vazias na estrutura do tipo geométrico.", campo)
    return valor


def _posicao(valor: Any, campo: str) -> list:
    """Confere dimensão, números finitos e intervalos longitude/latitude."""
    if not isinstance(valor, list) or len(valor) not in (2, 3):
        raise ErroEntrada("POSICAO_INVALIDA", "Cada posição deve conter longitude, latitude e, opcionalmente, altitude.", campo)
    for numero in valor:
        try:
            finito = type(numero) in (int, float) and math.isfinite(numero)
        except OverflowError:
            finito = False
        if not finito:
            raise ErroEntrada("NUMERO_INVALIDO", "As coordenadas devem ser números finitos; texto e booleano não são aceitos.", campo)
    if not (-180 <= valor[0] <= 180 and -90 <= valor[1] <= 90):
        raise ErroEntrada("COORDENADA_FORA_INTERVALO", "Use WGS 84: longitude de −180 a 180 e latitude de −90 a 90 graus.", campo)
    return valor


def validar_geojson(conteudo: bytes, nome: str) -> AreaValidada:
    """Valida bytes, estrutura e topologia; preserva partes, vazios e altitude."""
    if not isinstance(nome, str) or not nome.lower().endswith(".geojson"):
        raise ErroEntrada("EXTENSAO_INVALIDA", "Envie um arquivo com extensão .geojson.")
    if len(conteudo) > MAX_BYTES:
        raise ErroEntrada("ARQUIVO_GRANDE", "O arquivo excede o máximo de 1 MiB (1.048.576 bytes).", status=413)
    if not conteudo:
        raise ErroEntrada("ARQUIVO_VAZIO", "O arquivo está vazio.", status=400)
    try:
        documento = json.loads(conteudo.decode("utf-8"), object_pairs_hook=_objeto_unico, parse_constant=_constante_invalida, parse_float=_real_finito)
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError, RecursionError) as exc:
        raise ErroEntrada("JSON_INVALIDO", "O arquivo precisa conter JSON UTF-8 válido, com estrutura legível.", status=400) from exc
    _validar_textos(documento)
    if not isinstance(documento, dict) or documento.get("type") != "FeatureCollection":
        raise ErroEntrada("COLECAO_INVALIDA", "A raiz do arquivo deve ser um objeto FeatureCollection.")
    features = documento.get("features")
    if not isinstance(features, list) or len(features) != 1:
        raise ErroEntrada("QUANTIDADE_FEATURES", "Envie exatamente uma Feature. Prepare partes da mesma área em um único MultiPolygon; estudos independentes usam arquivos separados.", "features")
    feature = features[0]
    if not isinstance(feature, dict) or feature.get("type") != "Feature":
        raise ErroEntrada("FEATURE_INVALIDA", "O único registro precisa ser um objeto Feature.", "features[0]")
    if "properties" not in feature or (feature["properties"] is not None and not isinstance(feature["properties"], dict)):
        raise ErroEntrada("ATRIBUTOS_INVALIDOS", "A Feature deve conter properties como objeto ou null.", "features[0].properties")
    geometria = feature.get("geometry")
    if not isinstance(geometria, dict) or geometria.get("type") not in ("Polygon", "MultiPolygon"):
        raise ErroEntrada("GEOMETRIA_INCOMPATIVEL", "A geometria não pode ser nula e deve ser Polygon ou MultiPolygon.", "features[0].geometry")
    if any("crs" in objeto for objeto in (documento, feature, geometria)):
        raise ErroEntrada("CRS_LEGADO", "O campo crs legado não é aceito. Prepare o GeoJSON em WGS 84, longitude/latitude, conforme RFC 7946.", "crs")

    coordenadas = _lista(geometria.get("coordinates"), "coordinates")
    partes = [coordenadas] if geometria["type"] == "Polygon" else coordenadas
    partes_2d = []
    posicoes = aneis = 0
    dimensoes = set()
    for i, parte in enumerate(partes):
        aneis_2d = []
        for j, anel in enumerate(_lista(parte, f"coordinates.parte[{i}]")):
            campo = f"coordinates.parte[{i}].anel[{j}]"
            _lista(anel, campo)
            posicoes += len(anel)
            if posicoes > MAX_POSICOES:
                raise ErroEntrada("POSICOES_EXCEDIDAS", "O arquivo excede 20.000 posições, contando partes, anéis e fechamentos.", campo)
            if len(anel) < 4:
                raise ErroEntrada("ANEL_CURTO", "Cada anel deve ter pelo menos quatro posições, incluindo o fechamento.", campo)
            for k, valor in enumerate(anel):
                _posicao(valor, f"{campo}[{k}]")
                dimensoes.add(len(valor))
            if anel[0] != anel[-1]:
                raise ErroEntrada("ANEL_ABERTO", "O anel deve estar fechado no arquivo: a última posição precisa repetir todos os valores da primeira.", campo)
            anel_2d = [p[:2] for p in anel]
            if len({tuple(p) for p in anel_2d[:-1]}) < 3:
                raise ErroEntrada("VERTICES_INSUFICIENTES", "Cada anel precisa de pelo menos três vértices distintos em duas dimensões.", campo)
            aneis_2d.append(anel_2d)
            aneis += 1
        partes_2d.append(aneis_2d)
    # A cópia 2D é só para topologia; o documento de entrada conserva a altitude.
    entrada_2d = {"type": geometria["type"], "coordinates": partes_2d[0] if geometria["type"] == "Polygon" else partes_2d}
    try:
        superficie = shape(entrada_2d)
        valida = not superficie.is_empty and superficie.is_valid and superficie.area > 0
    except (GEOSException, ValueError, OverflowError) as exc:
        raise ErroEntrada("GEOMETRIA_INVALIDA", "Não foi possível interpretar a superfície. Confira contornos e recortes.", "geometry") from exc
    if not valida:
        raise ErroEntrada("GEOMETRIA_INVALIDA", "A superfície é inválida. Confira cruzamentos do contorno, recortes fora da área e partes sobrepostas ou com trecho de borda compartilhado. Nenhuma correção foi aplicada.", "geometry")
    return AreaValidada(documento, len(conteudo), hashlib.sha256(conteudo).hexdigest(), posicoes, len(partes), aneis, tuple(sorted(dimensoes)))
