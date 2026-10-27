"""Área minerada × entorno, áreas em UTM, UCs por grupo, barragens e água simulada contra limites legais."""
import copy
import json

import numpy as np
import pytest
from rasterio.io import MemoryFile
from rasterio.transform import from_origin
from shapely.geometry import LineString, Point, Polygon, box, mapping, shape

from geovale.api.main import RAIZ
from geovale.fichas import avaliar_agua, dividir, fatos_ucs, Ficha, ler_grade, preparar, projetar
from geovale.fontes_territorio import obter_wfs
from geovale.mapa import FonteIndisponivel
from geovale.relatorio import ler_cenario
from test_territorio import preparar_raiz

PONTOS = b'<xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema"><xsd:sequence><xsd:element name="id" type="xsd:int"/><xsd:element name="geom" type="gml:MultiPointPropertyType"/><xsd:element name="nome" type="xsd:string"/></xsd:sequence></xsd:schema>'
CELULA = 1 / 3600


def grade_teste(valores, oeste=-43.93, norte=-20.11):
    """GeoTIFF SIRGAS 2000 de células de um segundo, como Topodata e MapBiomas."""
    with MemoryFile() as memoria:
        with memoria.open(driver='GTiff', width=valores.shape[1], height=valores.shape[0], count=1, dtype='uint8',
                          crs='EPSG:4674', transform=from_origin(oeste, norte, CELULA, CELULA), nodata=0) as d:
            d.write(valores, 1)
        return memoria.read()


def wfs_pontos(monkeypatch, propriedades, z=0):
    def consultar(url, par, limite=None):
        if par['request'] == 'DescribeFeatureType':
            return PONTOS
        return json.dumps({'type': 'FeatureCollection', 'numberMatched': 1, 'numberReturned': 1, 'crs': {'properties': {'name': 'EPSG:4326'}},
                           'features': [{'type': 'Feature', 'id': 'b.1', 'properties': propriedades,
                                         'geometry': {'type': 'MultiPoint', 'coordinates': [[.2, .2, z]]}}]}).encode()
    monkeypatch.setattr('geovale.fontes_territorio.consultar', consultar)


def test_wfs_aceita_so_campo_extra_declarado_e_cota_zero(monkeypatch):
    recorte = Polygon([(0, 0), (1, 0), (0, 1)])
    declarada = {'camada': 'IDE:barragens', 'campos_extras': ['name'], 'z_zero': True}
    wfs_pontos(monkeypatch, {'id': 1, 'nome': 'B1', 'name': '1 - B1'})
    resultado, _ = obter_wfs(declarada, recorte)
    assert [c['name'] for c in resultado['campos']] == ['id', 'nome', 'name']
    geom = shape(resultado['dados']['features'][0]['geometry'])
    assert geom.equals(Point(.2, .2)) and not geom.has_z
    assert 'Cota publicada igual a zero' in resultado['aviso']
    with pytest.raises(FonteIndisponivel):
        obter_wfs({'camada': 'IDE:barragens', 'z_zero': True}, recorte)
    wfs_pontos(monkeypatch, {'id': 1, 'nome': 'B1', 'name': '1 - B1'}, z=12)
    with pytest.raises(FonteIndisponivel):
        obter_wfs(declarada, recorte)


def test_area_das_celulas_e_medida_em_utm_e_soma_a_extensao_da_grade():
    valores = np.ones((30, 40), dtype='uint8')
    grade = ler_grade(grade_teste(valores))
    extensao = projetar(mapping(box(-43.93, -20.11 - 30 * CELULA, -43.93 + 40 * CELULA, -20.11)))
    assert grade['area'].sum() == pytest.approx(extensao.area, rel=1e-4)
    assert 880 < grade['area'].mean() < 910


def test_area_minerada_vem_da_classe_mineracao_e_divide_linhas_poligonos_e_pontos(tmp_path):
    valores = np.full((40, 40), 3, dtype='uint8')
    valores[10:20, 10:20] = 30
    raiz = preparar_raiz(tmp_path)
    influencia = json.loads((raiz / 'dados/influencias/horizontes.geojson').read_text())
    classes = [{'codigo': 3, 'nome': '3 - Formação Florestal', 'cor': '#1f8d49'}, {'codigo': 30, 'nome': '30 - Mineração', 'cor': '#9c0027'}]
    dados = {'influencia': influencia, 'rasters': {'mb': grade_teste(valores)},
             'bases': [{'base': {'id': 'mb', 'tema_id': 'vegetacao', 'nome': 'Cobertura'}, 'tipo': 'raster', 'classes': classes}]}
    m = preparar(dados)['area_minerada']
    assert m['ha'] == pytest.approx(dados['grades']['mb']['area'][10:20, 10:20].sum() / 1e4)
    assert m['cor'] == '#9c0027' and m['utm'].area / 1e4 == pytest.approx(m['ha'], rel=1e-3)
    oeste, norte = -43.93 + 10 * CELULA, -20.11 - 10 * CELULA
    linha = {'geometry': mapping(LineString([(oeste - 10 * CELULA, norte - 5 * CELULA), (oeste + 20 * CELULA, norte - 5 * CELULA)]))}
    d = dividir([linha], m)
    assert d['unidade'] == 'km' and d['dentro'] == pytest.approx(d['total'] / 3, rel=.02)
    assert d['entorno'] == pytest.approx(d['total'] - d['dentro'])
    dentro, fora = Point(oeste + 5 * CELULA, norte - 5 * CELULA), Point(oeste - 5 * CELULA, norte + 5 * CELULA)
    assert dividir([{'geometry': mapping(dentro)}, {'geometry': mapping(fora)}], m) == {'unidade': 'registros', 'total': 2, 'dentro': 1, 'entorno': 1}
    assert dividir([linha], None)['dentro'] is None


def test_ucs_sao_agrupadas_pelo_grupo_publicado_com_ou_sem_acento():
    quadrado = mapping(box(-43.93, -20.12, -43.92, -20.11))
    def uc(nome, grupo):
        return {'id': nome, 'properties': {'nome_uc': nome, 'grupo': grupo, 'esfera': 'Estadual'}, 'geometry': quadrado}
    bases = [{'base': {'nome': 'UCs estaduais'}, 'dados': {'features': [uc('Parque', 'Protecao Integral'), uc('APA', 'Uso Sustentavel')]}},
             {'base': {'nome': 'UCs federais'}, 'dados': {'features': [uc('RPPN', 'Uso Sustentável')]}}]
    f = Ficha()
    fatos_ucs(f, bases, {'mineracao': None, 'recorte_ha': 1000})
    integral, sustentavel = f.dados
    assert integral['nome'] == 'UCs de proteção integral' and 'Parque' in integral['valor'] and 'APA' not in integral['valor']
    assert 'uso indireto' in integral['comentario']
    assert sustentavel['nome'] == 'UCs de uso sustentável' and 'APA' in sustentavel['valor'] and 'RPPN' in sustentavel['valor']
    area = projetar(quadrado).area / 1e4
    assert sustentavel['resumo'].endswith(f"{area:.1f}".replace('.', ',') + ' ha')


def test_agua_simulada_usa_classe_real_do_trecho_e_limites_da_conama():
    trecho = {'properties': {'enq_dn': '1'}, 'geometry': mapping(LineString([(-43.9, -20.1), (-43.89, -20.1)]))}
    ponto = {'ponto': [-43.895, -20.1001], 'parametros': {'ph': 6.8, 'turbidez': 58.0, 'fe_dissolvido': .2, 'mn_total': .09}}
    classe, linhas, fora = avaliar_agua(ponto, [trecho])
    assert classe == '1' and fora == ['Turbidez'] and 'trecho enquadrado' in linhas[0]
    classe, _, fora = avaliar_agua({**ponto, 'ponto': [-43.895, -20.11]}, [trecho])
    assert classe == '2' and fora == []
    especial = {**trecho, 'properties': {'enq_dn': 'Especial'}}
    _, linhas, fora = avaliar_agua(ponto, [especial])
    assert fora == [] and all('sem padrão numérico' in l for l in linhas[1:])


def test_cenario_rejeita_ponto_parametro_ou_referencia_invalidos(tmp_path):
    original = json.loads((RAIZ / 'dados/cenarios/horizontes.json').read_text())
    pasta = tmp_path / 'dados/cenarios'
    pasta.mkdir(parents=True)
    assert ler_cenario(RAIZ, 'horizontes')['agua']
    for defeito in [lambda c: c['agua'][0]['parametros'].update(cobre=1.0), lambda c: c['agua'][0].update(ponto=[-43.9]),
                    lambda c: c['dados'][0].update(rotulo='LONGO'), lambda c: c['dados'][0]['referencia_tecnica'].update(maximo=2),
                    lambda c: c['agua'][1].update(id=c['dados'][0]['id'])]:
        c = copy.deepcopy(original)
        defeito(c)
        (pasta / 'horizontes.json').write_text(json.dumps(c))
        with pytest.raises(ValueError):
            ler_cenario(tmp_path, 'horizontes')
