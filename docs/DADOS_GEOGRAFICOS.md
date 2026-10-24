# Dados preparados e reprodução

## Dois recortes reais

| Caso | Tamanho do GeoJSON | Pacote completo local |
|---|---:|---:|
| Rapatee / IL_006 | 39,373 bytes | 0.52 MiB |
| Burning Star 3 / IL_071 | 12,723 bytes | 0.51 MiB |

GeoJSON é o contorno vetorial: o tamanho do arquivo não determina quantidade de pontos de análise. São vértices da poligonal; relevo e cobertura são amostrados em células raster. Todas as contagens efetivas de células e percentuais válidos ficam no relatório técnico. Não são pontos de treinamento ML.

## Fontes e significado

Contornos: [GeoMine/OSMRE — operações de minas](https://geodata.osmre.gov/arcgis/rest/services/GeoMine/AllCoalmineOperations/MapServer/0), registros de Illinois. Consulta exata por `national_id` no manifesto. O pacote contém operações originais, atributos e união geométrica. Trata-se do limite publicado das operações encontradas, não uma certificação cadastral da mina inteira. Coleta do lote de contornos/DEM: 21/10/2026 UTC. Registro público não informa automaticamente estabilidade, fase de recuperação ou melhor uso futuro. Não extrapolar resultados para uma mina brasileira.

Relevo: [USGS 3DEP ImageServer](https://elevation.nationalmap.gov/arcgis/rest/services/3DEPElevation/ImageServer), exportações em UTM 15N (Rapatee) e 16N (Burning Star 3), grade de trabalho 30 m, interpolação bilinear. A grade amostrada não garante precisão de 30 m nem captura taludes/bancadas de uma mina. Horn 3×3 utiliza vizinhos; bordas/NoData permanecem ausentes.

Cobertura: [USGS Annual NLCD](https://www.usgs.gov/centers/eros/science/annual-nlcd-data-access), Collection 1.1, ano **2024**, códigos [MRLC](https://www.mrlc.gov/data/type/land-cover). Recorte obtido no [repositório público da Stanford Natural Capital Alliance](https://data.naturalcapitalalliance.stanford.edu/dataset/sts-28012eeef74b8535c027ce5a4d50b4ee3282ae6b3ce7a26d80145043e1e661c6), COG `MRLC_Annual_NLCD_LndCov_2024_c1v1.tif`. A distribuição usada já estava em EPSG4326. Foi lida somente a janela do entorno por HTTP Range, preservada em `cobertura-original.tif`; `cobertura.tif` é reprojeção por vizinho mais próximo para EPSG5070/30 m. Não afirmar que o arquivo reprojetado recupere a precisão/resolução original do produto. O WCS consultado apresentou falha; não houve geração ou preenchimento de classes simuladas.

Imagem: [USGS The National Map ImageryOnly](https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer), fotografia aérea USDA/USGS. Metadados do serviço referem NAIP 2017–2021; não foi confirmada a data exata por pixel. Exportação JPG de 1400×1000 com extensão EPSG3857 devolvida pelo serviço. A extensão real da resposta foi usada para sobrepor contorno; não se presume a extensão inicialmente pedida quando o servidor altera a proporção. A fotografia não é imagem atual em tempo real nem entrada do cálculo. Obtenção registrada em UTC no arquivo `imagem-origem.json`.

As imagens de fundo e os rasters têm datas, resoluções e finalidades diferentes. A coexistência de foto e poligonal não prova precisão cadastral. Limites ou valores aparentemente diferentes não devem ser ajustados visualmente sem analisar as fontes.

## Conteúdo e integridade

Cada `manifesto.json` registra identificação, natureza do limite, fonte/consulta, datas, DEM, ano da cobertura, extensão da fotografia, limitações, direitos e SHA256 de dez arquivos. Os outros arquivos de origem guardam as requisições/respostas e a janela de leitura. A aplicação verifica esses hashes antes de usar o caso. Os hashes detectam alteração local em relação ao manifesto; não constituem autenticação criptográfica do fornecedor nem prova de licença.

Os dados OSMRE/Illinois são públicos, mas não foi confirmada uma licença aberta específica no metadado consultado. Os recortes de referência conservam fontes, atribuições e metadados originais de aquisição; sua disponibilização com o código não os transforma em dados autorais do projeto nem concede direitos adicionais sobre materiais de terceiros. Os manifestos preservam o registro histórico do uso local durante a coleta. Não aplicar uma licença própria que pretenda conceder direitos sobre esses dados. A [política de créditos do USGS](https://www.usgs.gov/information-policies-and-instructions/copyrights-and-credits) distingue materiais produzidos pelo órgão de materiais de terceiros e orienta manter os créditos correspondentes.

## Reproduzir e inspecionar

1. `PYTHONPATH=backend python validacao/verificar_pacotes.py` confere todos os hashes, recalcula indicadores e índices neutros e lê as duas geometrias do GeoPackage, sem rede.
2. A entrada para repetir a extração é `area.geojson`; a origem geométrica está em `operacoes-origem.geojson`/atributos. Consultas completas estão no manifesto.
3. A requisição DEM pode ser repetida no endpoint `/exportImage` com os parâmetros de `relevo-origem.json`/manifesto. Exportação da imagem usa a URL de `imagem-origem.json` e a extensão retornada. Serviços vivos podem mudar dados, portanto novos bytes não devem substituir silenciosamente o pacote congelado.
4. Para cobertura, a URL do COG e os deslocamentos/tamanho da janela original estão em `cobertura-origem.json`. É necessário cliente raster com HTTP Range; evitar baixar o arquivo continental inteiro. O recorte ao redor da geometria usa margem de 1.200 metros em EPSG5070, jamais 1.200 graus. Reprojetar o recorte pelo vizinho mais próximo e resolução de trabalho 30 m; preservar NoData.
5. Novas aquisições precisam de novo diretório/versionamento, hashes, manifesto e repetição dos testes. Não atualizar um raster dentro do pacote antigo mantendo o manifesto anterior.

`dados/qgis/GeoVale.qgs` referencia `minas.gpkg` com duas feições. O GeoPackage foi lido em GeoPandas. **A interface QGIS não foi executada**, pois o aplicativo não estava instalado. QGIS é ferramenta de inspeção/preparação; não é dependência do usuário do dashboard.
