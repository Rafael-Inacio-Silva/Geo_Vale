# Estado atual

Versão **4.0.0**, atualizada em 26/10/2026. Mapa mundial aberto em Minas Gerais, contorno estadual oficial, uma Mina Horizontes e Nova Lima sob seleção. Fundos OpenStreetMap/Esri, cinco temas estaduais e trilhas municipais, com intensidade e legendas. ANM fornece atributos cadastrais; IBGE fornece o município.

A barra esquerda apresenta **Influência**, desabilitada antes da seleção. Selecionar pelo cartão ou pela bolinha já mostra o contorno da mina. Ativar Influência acrescenta o contorno externo e todas as onze bases visualmente recortadas. Os checkboxes da direita ampliam cada tema além da influência; desmarcar restaura o recorte enquanto Influência estiver ativa. Atributos, valores, fontes e datas ficam no relatório **Exportar JSON**, sem painel de dados na tela.

A preparação usa WFS para oito bases vetoriais estaduais, WCS para dois rasters e ArcGIS REST para trilhas. Todos os atributos dos registros que intersectam a influência são conservados. Os rasters mantêm valores e grade nativa em GeoTIFF mascarado. SQLite guarda os resultados por mina/base em `.local`, fora do Git. Atualização automática, controle de validade e novas tentativas independem da interface.

Consulta real da Horizontes no recorte comum: 68 trechos hidrográficos, 16 massas d’água, 3 registros de solos, 3 UCs estaduais, 1 federal, 1 municipal, 34 áreas urbanizadas, 4 registros rodoviários e 34 trilhas. Declividade: 171.428 células válidas e seis classes; cobertura da terra: 182.154 células válidas e dez classes. Valores calculados na fonte e no recorte, não inseridos como constantes no código.

O recorte comum é uma aproximação da AII de águas/solos do projeto conjunto de ampliação. Não representa área de intervenção ou limite de fechamento para todos os temas. Não há diagnóstico, recomendação, ranking, ML, upload ou implantação pública. [Evidência](INFLUENCIA.md), [método](DADOS_TERRITORIAIS.md), [verificações](VALIDACAO.md).
