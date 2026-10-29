"""Lê o único recorte de caracterização e a mina sombreada, com evidência local."""
import json
from shapely.geometry import shape


def ler_influencia(caminho, mina_id):
    """Confere identidade, procedência e contornos sem reparar ou redefinir limites."""
    dados = json.loads(caminho.read_text(encoding='utf-8'))
    if dados['type'] != 'FeatureCollection' or dados['mina_id'] != mina_id:
        raise ValueError('Influência incompatível')
    if len(dados['features']) != 2 or {f['properties']['id'] for f in dados['features']} != {'mina', 'influencia'}:
        raise ValueError('Pacote de influência incompleto')
    for feicao in dados['features']:
        p = feicao['properties']
        geom = shape(feicao['geometry'])
        # Influência: digitalizada de estudo ambiental ou, sem estudo público, faixa declarada em volta da cava.
        origens = {'referencia_osm'} if p['id'] == 'mina' else {'referencia_documental', 'faixa_declarada'}
        if feicao['type'] != 'Feature' or p['origem'] not in origens or p['aproximada'] is not True:
            raise ValueError('Procedência incompatível')
        if geom.geom_type not in ('Polygon', 'MultiPolygon') or geom.is_empty or not geom.is_valid:
            raise ValueError('Contorno inválido')
        x0, y0, x1, y1 = geom.bounds
        if not (-180 <= x0 < x1 <= 180 and -85 <= y0 < y1 <= 85):
            raise ValueError('Extensão incompatível')
    faixa = next(f for f in dados['features'] if f['properties']['id'] == 'influencia')['properties']['origem'] == 'faixa_declarada'
    evidencia = dados['fonte'].get('distancia_m', 0) > 0 and dados['fonte'].get('referencia') if faixa else dados['fonte'].get('sha256_pdf')
    if dados['fonte']['crs_saida'] != 'EPSG:4326' or not evidencia:
        raise ValueError('Evidência incompleta')
    return dados


# Recorte digitalizado de estudo ambiental (hoje só a Horizontes: AII da FEAM). Os textos ficam fora do pacote
# porque o pacote inteiro entra na assinatura das bases coletadas.
TEXTOS_DOCUMENTAL = {'recorte_curto': 'AII águas/solos (FEAM, Figura 2.3)', 'credito': 'FEAM / Amplo',
                     'origem_texto': 'AII de águas e solos — meio físico do projeto Tamanduá/Horizontes'}


def textos_recorte(dados):
    """Textos de exibição do recorte: os da faixa declarada vêm do pacote; os do estudo, de TEXTOS_DOCUMENTAL."""
    fonte = dados['fonte']
    return {k: fonte.get(k, TEXTOS_DOCUMENTAL[k]) for k in TEXTOS_DOCUMENTAL}
