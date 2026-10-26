# Dados geográficos — navegação

## Limite de Minas Gerais

- Infraestrutura: [IDE-Sisema](https://geoportal.meioambiente.mg.gov.br/home).
- Origem: limites municipais da Fundação João Pinheiro (FJP), agregados na camada estadual conforme seu metadado.
- Camada: `IDE:ide_1101_mg_unidade_federacao_pol`.
- [Metadado oficial](https://idesisema.meioambiente.mg.gov.br/geonetwork/srv/por/catalog.search#/metadata/ce121547-8e95-4cc0-a6b9-e12a59c74f28).
- Serviço: `https://geoserver.meioambiente.mg.gov.br/ows`, WFS 2.0.0, `GetFeature`, `count=1`, `outputFormat=application/json`, `srsName=EPSG:4326`.
- Identificação conferida: `geocodigo=31`, `nomuf=Minas Gerais`.
- Aplicação: contorno de navegação estadual, simplificado em 0,001 grau com topologia preservada. Essa representação não é uma medição cadastral.

A geometria é consultada pela API e guardada temporariamente em memória. O backend retorna fonte, URL, referência espacial, simplificação, indicador de ajuste visual e data efetiva da consulta. O dado recebido apresentou uma autointerseção de anel; a preparação visual usa `make_valid`, conserva as superfícies e simplifica o contorno. Não altera o cadastro oficial nem certifica sua precisão. Não há cópia do conjunto bruto integral versionada no projeto. A atribuição exibida no mapa é FJP / IDE-Sisema; a documentação do fornecedor informa as condições de uso aplicáveis ao conjunto.

## Mina Horizontes

O catálogo contém uma única mina: Horizontes, anteriormente Capitão do Mato, Vale, Nova Lima/MG, Complexo Vargem Grande. A identificação se apoia na [notícia oficial da Vale](https://www.vale.com/ar/w/vale-altera-nome-de-mina-e-barragem-em-nova-lima-e-reforca-posicionamento-antirracista).

O ponto de navegação é **aproximado**, em longitude −43,91708014 e latitude −20,12139929, EPSG:4326. Foi derivado do centroide do polígono do processo ANM 003.964/1950 obtido no WFS da IDE-Sisema em 24/10/2026. O vínculo desse processo com o empreendimento consta de [documento público da FEAM](https://sistemas.meioambiente.mg.gov.br/licenciamento/uploads/-r1U-OgCZO3dEqex9HShmdqbrC5mgstw.pdf).

O cadastro e os links de origem estão em `dados/minas.json`. O nome anterior é somente um termo de pesquisa da mesma entrada. O marcador **não é uma localização certificada do centro da mina**, nem um polígono físico/operacional. O processo minerário pode ser adicionado pelo botão Polígono ANM, com prévia e confirmação, preservando seu significado cadastral. Não se infere condição de operação a partir de sua fase cadastral.

## Mapas de fundo

- **Mapa:** tiles padrão do OpenStreetMap, com [atribuição](https://www.openstreetmap.org/copyright) e [política do serviço](https://operations.osmfoundation.org/policies/tiles/). Somente acesso interativo; sem pré-download ou remoção dos créditos.
- **Satélite:** [Esri World Imagery](https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer), com atribuição Esri e fornecedores. As imagens são contexto visual; sua data e resolução variam por lugar. Não representam observação ao vivo.

Leaflet é a biblioteca de visualização; não é o fornecedor desses dados. As imagens são solicitadas diretamente pelo navegador. O contorno estadual é solicitado pelo nosso backend. A camada estadual cobre MG; o fundo continua navegável globalmente.

## Cinco temas e dez bases oficiais

Sobreposições estaduais provenientes do WMS da IDE-Sisema: `https://geoserver.meioambiente.mg.gov.br/ows`. O catálogo fixo está em `backend/geovale/camadas.py`. As imagens são reprojetadas pelo fornecedor para EPSG:3857 no `GetMap` WMS 1.1.1; a localização e o WFS estadual usam EPSG:4326. O serviço publica as bases nativas em SIRGAS 2000/EPSG:4674. Não há cálculo de área/distância em Web Mercator nesta etapa.

As referências de catálogo foram consultadas em 24/10/2026 e os dez `GetMap` e dez `GetLegendGraphic` foram verificados em 25/10/2026 com retorno PNG válido. Data de revisão do metadado é distinta do ano de referência dos dados. Cada linha abaixo tem link para a ficha oficial.

| Tema | Identificador WMS (prefixo `IDE:`) | Origem / referência e limite |
|---|---|---|
| Relevo | [`ide_0201_mg_decliv_topodata`](https://idesisema.meioambiente.mg.gov.br/geonetwork/srv/por/catalog.search#/metadata/46b18109-06ab-4529-9401-5a662f1e39b2) | INPE/Topodata; declividade em seis classes, baseada em SRTM de fevereiro de 2000, pixel refinado de cerca de 30 m. Não descreve a cava atual. |
| Água | [`ide_0103_mg_massa_dagua_bho_pol`](https://idesisema.meioambiente.mg.gov.br/geonetwork/srv/por/catalog.search#/metadata/537a07b7-4a29-422d-bdde-43ae8af87b61) | ANA/Igam; massas d’água da base hidrográfica. Publicação registrada em 2021; não informa nível ou qualidade atual da água. |
| Água | [`ide_0104_mg_hidrografia_principal_lin`](https://idesisema.meioambiente.mg.gov.br/geonetwork/srv/por/catalog.search#/metadata/ebb215b7-10a5-481b-8cb2-823b4cf3d5e4) | Igam; principais ottotrechos. Publicação registrada em 2022; não representa toda drenagem local. |
| Solos | [`ide_1502_mg_mapa_solos_pol`](https://idesisema.meioambiente.mg.gov.br/geonetwork/srv/por/catalog.search#/metadata/365b8a86-6ecd-474b-ae20-30efac6107a8) | UFV/Cetec/UFLA/Sisema; produzido em 2010. Pedologia regional, sem ensaio químico, contaminação ou recuperação atual. |
| Vegetação | [`ide_1402_mg_uso_terra_mapbiomas_2025`](https://idesisema.meioambiente.mg.gov.br/geonetwork/srv/por/catalog.search#/metadata/bb27f72b-2a30-45c0-9b04-2d3a8a32f0ca) | MapBiomas coleção 11, referência 2025, 30 m; classes de uso/cobertura, incluindo vegetação. O recorte inclui buffer de 1 km na borda estadual. Não certifica vegetação ou intervenção legalmente autorizada. |
| Conservação | [`ide_2010_mg_unidades_conservacao_estaduais_pol`](https://idesisema.meioambiente.mg.gov.br/geonetwork/srv/por/catalog.search#/metadata/f4b56fd6-5d60-40bc-be8a-d25949525b85) | IEF; UCs estaduais; revisão do recurso registrada em 06/08/2026. |
| Conservação | [`ide_2010_mg_unidades_conservacao_federais_pol`](https://idesisema.meioambiente.mg.gov.br/geonetwork/srv/por/catalog.search#/metadata/48a7ad10-baee-4dff-aebd-fd275346a7ba) | ICMBio; UCs federais em MG; revisão registrada em 27/04/2026. |
| Conservação | [`ide_2010_mg_unidades_conservacao_municipais_pol`](https://idesisema.meioambiente.mg.gov.br/geonetwork/srv/por/catalog.search#/metadata/c509af74-2ff0-414a-8bb2-b1238392ffa4) | Municípios/IEF; UCs municipais; revisão do recurso registrada em 31/07/2026. Não reúne todas as restrições ambientais. |
| Entorno | [`ide_1401_mg_areas_urbanizadas_2022_pol`](https://idesisema.meioambiente.mg.gov.br/geonetwork/srv/por/catalog.search#/metadata/cbdfc068-5fff-4365-b4cd-9837f1373a70) | IBGE; ano de referência 2022, publicação cadastrada em 2026. Não mede demanda social nem população atual. |
| Infraestrutura | [`ide_0401_mg_rodovias_lin`](https://idesisema.meioambiente.mg.gov.br/geonetwork/srv/por/catalog.search#/metadata/ba9062d9-15d1-4373-9638-2ef8ce885f74) | DNIT/SNV; revisão registrada em 29/06/2022. Não cobre toda via local nem atesta acesso ou capacidade operacional. |

Os cinco checkboxes representam grupos, não cinco arquivos. O rótulo “Solos e condição ambiental” conserva o tema definido na discussão, mas seu conteúdo implementado é apenas o mapa pedológico; não há diagnóstico ambiental. Da mesma forma, o tema entorno inclui urbanização e rodovias, não toda infraestrutura e conhecimento social do território.

Fundamentação e justificativa do recorte em [Escolhas territoriais](ESCOLHAS_TERRITORIAIS.md). Não há perímetro físico certificado da mina ou base de treinamento. Há várias áreas de estudo independentes, desenhadas pelo usuário ou adicionadas do processo ANM, mantidas apenas na página. Ajustar um polígono cadastral e confirmar produz recorte manual; não altera a fonte oficial.

## Sexta opção: trilhas municipais

A camada **Trilhas de Nova Lima** utiliza o cadastro publicado pela Prefeitura, independente do WMS da IDE-Sisema. São agora seis opções e onze bases, preservando os cinco grupos estaduais. A camada municipal chama-se `Trilhas_Decreto_6773_2016_fev_2024`; fonte nativa EPSG:31983, consultada em EPSG:4326 e projetada pelo Leaflet para exibição. Campos consumidos: identificador e nome, associados às cores e rótulos do renderer oficial do item. A configuração consultada contém 59 categorias e 12 cores diferentes para os 67 registros; categorias distintas podem compartilhar uma cor. Limite publicado aproximado: oeste −44,005238; sul −20,211133; leste −43,749501; norte −19,923718.

Em 25/10/2026, a consulta pública contou 67 registros. O serviço informou última edição em **22/04/2024, 16:34:49 UTC**; isso não data cada levantamento. A identificação do decreto é o título fornecido pelo cadastro, sem verificação jurídica do ato nesta etapa. Metadados técnicos, links e limites em [Trilhas de Nova Lima](TRILHAS_NOVA_LIMA.md). A ausência de informação explícita de licença no item não foi interpretada como autorização irrestrita de redistribuição.

## Processo ANM e município IBGE

O cadastro e a geometria do processo 003.964/1950 são consultados diretamente no SIGMINE da ANM, com saída solicitada em EPSG:4326, origem/data e campos cadastrais controlados. Consulta de 26/10/2026: VALE S.A., CONCESSÃO DE LAVRA, FERRO e 471,39 ha. Não é perímetro físico nem declaração de operação ativa. [Contrato e proveniência](ANM.md).

O contorno municipal vem da API de malhas simplificadas do IBGE, código Nova Lima 3144805, qualidade máxima disponível nessa API. Não se assume ano de levantamento a partir da consulta. Só o município da mina selecionada é acrescentado; não é camada temática nem área de estudo. [Precisão, fonte e operação](LIMITE_MUNICIPAL.md).
