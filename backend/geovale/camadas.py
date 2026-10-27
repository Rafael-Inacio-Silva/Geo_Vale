"""Catálogo único para visualização e caracterização automática de todas as bases."""

from urllib.parse import urlencode

SERVICO_WMS = 'https://geoserver.meioambiente.mg.gov.br/ows'
CATALOGO = 'https://idesisema.meioambiente.mg.gov.br/geonetwork/srv/por/catalog.search#/metadata/'


def base(nome, titulo, metadado):
    """Identifica uma base e sua legenda oficial, sem copiar o conjunto geográfico."""
    camada = f'IDE:{nome}'
    return {
        'camada': camada, 'nome': titulo, 'metadado': CATALOGO + metadado,
        'processamento': 'wcs' if nome in ('ide_0201_mg_decliv_topodata', 'ide_1402_mg_uso_terra_mapbiomas_2025') else 'wfs',
        'legenda': SERVICO_WMS + '?' + urlencode({
            'service': 'WMS', 'version': '1.1.1', 'request': 'GetLegendGraphic',
            'layer': camada, 'format': 'image/png', 'legend_options': 'fontSize:11;forceLabels:on',
        }),
    }


CAMADAS = [
    {
        'id': 'relevo', 'nome': 'Relevo e declividade', 'cor': '#b06f36',
        'opacidade': 0.5, 'ordem': 3, 'url': SERVICO_WMS,
        'credito': 'Relevo: INPE / Topodata / IDE-Sisema',
        'bases': [base('ide_0201_mg_decliv_topodata', 'Declividade — Topodata', '46b18109-06ab-4529-9401-5a662f1e39b2')],
    },
    {
        'id': 'agua', 'nome': 'Água e drenagem', 'cor': '#237bba',
        'opacidade': 0.85, 'ordem': 4, 'url': SERVICO_WMS,
        'credito': 'Água: ANA / Igam / IDE-Sisema',
        'bases': [
            base('ide_0103_mg_massa_dagua_bho_pol', "Massas d’água", '537a07b7-4a29-422d-bdde-43ae8af87b61'),
            base('ide_0104_mg_hidrografia_principal_lin', 'Principais trechos hidrográficos', 'ebb215b7-10a5-481b-8cb2-823b4cf3d5e4'),
        ],
    },
    {
        'id': 'solos', 'nome': 'Solos', 'cor': '#a87554',
        'opacidade': 0.4, 'ordem': 2, 'url': SERVICO_WMS,
        'credito': 'Solos: UFV / Cetec / UFLA / Sisema',
        'bases': [base('ide_1502_mg_mapa_solos_pol', 'Tipos de solos — mapeamento de 2010', '365b8a86-6ecd-474b-ae20-30efac6107a8')],
    },
    {
        'id': 'vegetacao', 'nome': 'Vegetação e conservação', 'cor': '#538343',
        'opacidade': 0.6, 'ordem': 1, 'url': SERVICO_WMS,
        'credito': 'Cobertura: MapBiomas; UCs: IEF / ICMBio / municípios / IDE-Sisema',
        'bases': [
            base('ide_1402_mg_uso_terra_mapbiomas_2025', 'Uso e cobertura da terra — 2025', 'bb27f72b-2a30-45c0-9b04-2d3a8a32f0ca'),
            base('ide_2010_mg_unidades_conservacao_estaduais_pol', 'Unidades de conservação estaduais', 'f4b56fd6-5d60-40bc-be8a-d25949525b85'),
            base('ide_2010_mg_unidades_conservacao_federais_pol', 'Unidades de conservação federais', '48a7ad10-baee-4dff-aebd-fd275346a7ba'),
            base('ide_2010_mg_unidades_conservacao_municipais_pol', 'Unidades de conservação municipais', 'c509af74-2ff0-414a-8bb2-b1238392ffa4'),
        ],
    },
    {
        'id': 'entorno', 'nome': 'Entorno e infraestrutura', 'cor': '#a44663',
        'opacidade': 0.8, 'ordem': 5, 'url': SERVICO_WMS,
        'credito': 'Entorno: IBGE / DNIT / IDE-Sisema',
        'bases': [
            base('ide_1401_mg_areas_urbanizadas_2022_pol', 'Áreas urbanizadas — referência 2022', 'cbdfc068-5fff-4365-b4cd-9837f1373a70'),
            base('ide_0401_mg_rodovias_lin', 'Rodovias estaduais e federais', 'ba9062d9-15d1-4373-9638-2ef8ce885f74'),
        ],
    },
]

# O envelope limita requisições; a cobertura efetiva continua sendo a de cada fonte.
for tema in CAMADAS:
    tema['tipo'] = 'wms'
    tema['cobertura'] = [[-23.5, -51.3], [-14.0, -38.7]]
    tema['alcance'] = 'Minas Gerais'

CAMADAS.append({
    'id': 'trilhas', 'nome': 'Trilhas de Nova Lima', 'tipo': 'geojson',
    'cor': '#ffff00', 'opacidade': 1.0, 'ordem': 6,
    'url': '/api/mapa/trilhas',
    'cobertura': [[-20.211133, -44.005239], [-19.923717, -43.749500]],
    'alcance': 'Nova Lima',
    'credito': 'Trilhas: <a href="https://pmnl.maps.arcgis.com/apps/webappviewer/index.html?id=ff761e397b904ad4b164eb8a71cb7d86">Prefeitura de Nova Lima</a>',
    'bases': [{
        'processamento': 'arcgis',
        'camada': 'Trilhas/FeatureServer/0', 'nome': 'Trilhas cadastradas — Decreto 6773/2016',
        'metadado': 'https://pmnl.maps.arcgis.com/home/item.html?id=2504a27b4e684bfdbe0210fa7af1971d',
        'legenda': '',
    }],
})
