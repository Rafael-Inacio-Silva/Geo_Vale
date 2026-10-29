# Dados geográficos — navegação e território preparado

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

O catálogo contém as Minas Abóboras e Trindade ([Catálogo de minas](MINAS.md)) e a Horizontes, anteriormente Capitão do Mato, Vale, Nova Lima/MG, Complexo Vargem Grande. A identificação se apoia na [notícia oficial da Vale](https://www.vale.com/ar/w/vale-altera-nome-de-mina-e-barragem-em-nova-lima-e-reforca-posicionamento-antirracista).

O ponto de navegação é aproximado, longitude -43.92145769 e latitude -20.11834631, derivado do centro visual do contorno de mineração OpenStreetMap, way 315221699. Não é um centro certificado. O catálogo e sua fonte estão em `dados/minas.json`; o nome anterior pesquisa a mesma entrada.

O [único recorte de influência e o sombreado OSM](INFLUENCIA.md) estão em GeoJSON local, com receita, fonte, hash do PDF, figura, página e aviso de aproximação. O contorno externo AII águas/solos é usado como recorte comum do MVP por simplificação declarada. A ANM fornece somente atributos cadastrais.

## Mapas de fundo

- **Mapa:** tiles padrão do OpenStreetMap, com [atribuição](https://www.openstreetmap.org/copyright) e [política do serviço](https://operations.osmfoundation.org/policies/tiles/). Somente acesso interativo; sem pré-download ou remoção dos créditos.
- **Satélite:** [Esri World Imagery](https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer), com atribuição Esri e fornecedores. As imagens são contexto visual; sua data e resolução variam por lugar. Não representam observação ao vivo.

Leaflet é a biblioteca de visualização; não é o fornecedor desses dados. As imagens são solicitadas diretamente pelo navegador. O contorno estadual é solicitado pelo nosso backend. A camada estadual cobre MG; o fundo continua navegável globalmente. A caracterização usa somente o recorte comum de cada mina, não toda a extensão visível.

## Seis temas e dezessete bases oficiais

Sobreposições estaduais provenientes do WMS da IDE-Sisema: `https://geoserver.meioambiente.mg.gov.br/ows`. O catálogo fixo está em `backend/geovale/camadas.py`. As imagens são reprojetadas pelo fornecedor para EPSG:3857 no `GetMap` WMS 1.1.1; a localização e o WFS estadual usam EPSG:4326. O serviço publica as bases nativas em SIRGAS 2000/EPSG:4674. Não há cálculo de área/distância em Web Mercator nesta etapa.

As referências de catálogo das dez primeiras bases foram consultadas em 24/10/2026 e seus `GetMap`/`GetLegendGraphic` verificados em 25/10/2026 com retorno PNG válido. As cinco bases acrescentadas na 4.3.0 e as duas da 4.4.0 tiveram metadado consultado e coleta WFS conferida em 27/10/2026. Data de revisão do metadado é distinta do ano de referência dos dados. Cada linha abaixo tem link para a ficha oficial.

| Tema | Identificador WMS (prefixo `IDE:`) | Origem / referência e limite |
|---|---|---|
| Relevo | [`ide_0201_mg_decliv_topodata`](https://idesisema.meioambiente.mg.gov.br/geonetwork/srv/por/catalog.search#/metadata/46b18109-06ab-4529-9401-5a662f1e39b2) | INPE/Topodata; declividade em seis classes, baseada em SRTM de fevereiro de 2000, pixel refinado de cerca de 30 m. Não descreve a cava atual. |
| Relevo | [`ide_2002_mg_potencialidade_cavidades_pol`](https://idesisema.meioambiente.mg.gov.br/geonetwork/srv/por/catalog.search#/metadata/15d09272-da9f-4ea1-8995-b496da17a3aa) | CECAV (Jansen, Cavalcanti e Lamblém, 2012); potencial de ocorrência de cavernas na escala 1:2.500.000. Não localiza cavidades. |
| Água | [`ide_0103_mg_massa_dagua_bho_pol`](https://idesisema.meioambiente.mg.gov.br/geonetwork/srv/por/catalog.search#/metadata/537a07b7-4a29-422d-bdde-43ae8af87b61) | ANA/Igam; massas d’água da base hidrográfica. Publicação registrada em 2021; não informa nível ou qualidade atual da água. Uma geometria inválida na faixa da Abóboras é corrigida com make_valid, declarado e contado. |
| Água | [`ide_0104_mg_hidrografia_principal_lin`](https://idesisema.meioambiente.mg.gov.br/geonetwork/srv/por/catalog.search#/metadata/ebb215b7-10a5-481b-8cb2-823b4cf3d5e4) | Igam; principais ottotrechos. Publicação registrada em 2022; não representa toda drenagem local. |
| Água | [`ide_240502_sf_igam_reg_vazao_lin`](https://idesisema.meioambiente.mg.gov.br/geonetwork/srv/por/catalog.search#/metadata/72318b9b-5d11-47f6-848b-8f66c124972d) | Igam; vazões regionalizadas por ottotrecho (BHO 2017), incluindo Q7,10, Q90, Q95 e média de longo termo em m³/s. Estimativa regional, não medição. |
| Água | [`ide_2019_sf_enq_corpos_dagua_sf5_lin`](https://idesisema.meioambiente.mg.gov.br/geonetwork/srv/por/catalog.search#/metadata/4a831429-170f-4856-b3e5-7fdb77709d02) | Igam; classe de enquadramento dos trechos do Rio das Velhas (SF5) e ato vigente. Classe não é medição de qualidade. |
| Solos | [`ide_1502_mg_mapa_solos_pol`](https://idesisema.meioambiente.mg.gov.br/geonetwork/srv/por/catalog.search#/metadata/365b8a86-6ecd-474b-ae20-30efac6107a8) | UFV/Cetec/UFLA/Sisema; produzido em 2010. Pedologia regional, sem ensaio químico, contaminação ou recuperação atual. |
| Vegetação | [`ide_1402_mg_uso_terra_mapbiomas_2025`](https://idesisema.meioambiente.mg.gov.br/geonetwork/srv/por/catalog.search#/metadata/bb27f72b-2a30-45c0-9b04-2d3a8a32f0ca) | MapBiomas coleção 11, referência 2025, 30 m; classes de uso/cobertura, incluindo vegetação. O recorte inclui buffer de 1 km na borda estadual. Não certifica vegetação ou intervenção legalmente autorizada. |
| Conservação | [`ide_2010_mg_unidades_conservacao_estaduais_pol`](https://idesisema.meioambiente.mg.gov.br/geonetwork/srv/por/catalog.search#/metadata/f4b56fd6-5d60-40bc-be8a-d25949525b85) | IEF; UCs estaduais; revisão do recurso registrada em 06/08/2026. |
| Conservação | [`ide_2010_mg_unidades_conservacao_federais_pol`](https://idesisema.meioambiente.mg.gov.br/geonetwork/srv/por/catalog.search#/metadata/48a7ad10-baee-4dff-aebd-fd275346a7ba) | ICMBio; UCs federais em MG; revisão registrada em 27/04/2026. |
| Conservação | [`ide_2010_mg_unidades_conservacao_municipais_pol`](https://idesisema.meioambiente.mg.gov.br/geonetwork/srv/por/catalog.search#/metadata/c509af74-2ff0-414a-8bb2-b1238392ffa4) | Municípios/IEF; UCs municipais; revisão do recurso registrada em 31/07/2026. Não reúne todas as restrições ambientais. |
| Conservação | [`ide_240905_sf5_apps_fbds_pol`](https://idesisema.meioambiente.mg.gov.br/geonetwork/srv/por/catalog.search#/metadata/a61b73f1-ca5b-4776-808a-a708209254f1) | FBDS; APPs hídricas do Rio das Velhas (nascentes, cursos e massas d’água) com faixa publicada. Mapeamento regional; o recorte não alcança outra circunscrição. |
| Entorno | [`ide_1401_mg_areas_urbanizadas_2022_pol`](https://idesisema.meioambiente.mg.gov.br/geonetwork/srv/por/catalog.search#/metadata/cbdfc068-5fff-4365-b4cd-9837f1373a70) | IBGE; ano de referência 2022, publicação cadastrada em 2026. Não mede demanda social nem população atual. |
| Infraestrutura | [`ide_0401_mg_rodovias_lin`](https://idesisema.meioambiente.mg.gov.br/geonetwork/srv/por/catalog.search#/metadata/ba9062d9-15d1-4373-9638-2ef8ce885f74) | DNIT/SNV; revisão registrada em 29/06/2022. Não cobre toda via local nem atesta acesso ou capacidade operacional. |
| Infraestrutura | [`ide_0501_mg_linhas_transmissao_ons_lin`](https://idesisema.meioambiente.mg.gov.br/geonetwork/srv/por/catalog.search#/metadata/aae1c08d-8afd-4321-b362-e3b6c9aacd29) | ONS; linhas de transmissão com tensão e concessionária. Duas linhas de 345 kV cruzam o recorte. Critério de rede elétrica da sugestão. Fica fora da imagem do mapa interativo porque o estilo WMS oficial falha no GeoServer (compara a tensão numérica com texto vazio); dados, sugestão e PDF usam o WFS normalmente. |
| Barragens | [`ide_1903_mg_zas_pae_pol`](https://idesisema.meioambiente.mg.gov.br/geonetwork/srv/por/catalog.search#/metadata/1d2e7b81-f729-454d-bf7f-035266599d52) | FEAM; zonas de autossalvamento dos PAEBM. A resposta conjunta excede 32 MiB: cada registro é lido separadamente. 13 das 19 geometrias publicadas são inválidas e são corrigidas com make_valid, declarado e contado. |
| Barragens | [`ide_1901_mg_barragens_rejeitos_residuos_pto`](https://idesisema.meioambiente.mg.gov.br/geonetwork/srv/por/catalog.search#/metadata/e0197766-b7af-4e1e-8766-7b1de8f2002c) | FEAM; barragens de rejeitos e resíduos, ano base 2024, com método construtivo, finalidade, PDA e classe. Não informa nível de emergência atual (SIGBM/ANM). |

Os seis checkboxes estaduais representam grupos, não arquivos únicos. O tema Solos contém apenas o mapa pedológico; não há diagnóstico ambiental. Da mesma forma, o tema entorno inclui urbanização e rodovias, não toda infraestrutura e conhecimento social do território.

Fundamentação e justificativa do recorte em [Escolhas territoriais](ESCOLHAS_TERRITORIAIS.md). Não há perímetro físico certificado da mina ou base de treinamento. A influência comum é uma aproximação documental; o sombreado da mina é colaborativo. Influência mostra todas as bases recortadas; cada checkbox amplia um tema além do contorno. Os dados completos são guardados por mina, independentemente da visibilidade; o PDF apresenta fichas legíveis com dados de todas as bases e comentários separados.

## Opção municipal: trilhas

A camada **Trilhas de Nova Lima** utiliza o cadastro publicado pela Prefeitura, independente do WMS da IDE-Sisema. São sete opções e dezoito bases, com seis grupos estaduais. A camada municipal chama-se `Trilhas_Decreto_6773_2016_fev_2024`; fonte nativa EPSG:31983, consultada em EPSG:4326 e projetada pelo Leaflet para exibição. Campos consumidos: identificador e nome, associados às cores e rótulos do renderer oficial do item. A configuração consultada contém 59 categorias e 12 cores diferentes para os 67 registros; categorias distintas podem compartilhar uma cor. Limite publicado aproximado: oeste −44,005238; sul −20,211133; leste −43,749501; norte −19,923718.

Em 25/10/2026, a consulta pública contou 67 registros. O serviço informou última edição em **22/04/2024, 16:34:49 UTC**; isso não data cada levantamento. A identificação do decreto é o título fornecido pelo cadastro, sem verificação jurídica do ato nesta etapa. Metadados técnicos, links e limites em [Trilhas de Nova Lima](TRILHAS_NOVA_LIMA.md). A ausência de informação explícita de licença no item não foi interpretada como autorização irrestrita de redistribuição.

## Processo ANM e município IBGE

Somente os atributos do processo 003.964/1950 são consultados no SIGMINE da ANM, com `returnGeometry=false`, fonte/data e campos controlados. Consulta de 26/10/2026: VALE S.A., CONCESSÃO DE LAVRA, FERRO e 471,39 ha. Não é perímetro físico nem declaração de operação ativa. [Contrato e proveniência](ANM.md).

O contorno municipal vem da API de malhas simplificadas do IBGE, código Nova Lima 3144805, qualidade máxima disponível nessa API. Não se assume ano de levantamento a partir da consulta. Só o município da mina selecionada é acrescentado; não é camada temática nem área de estudo. [Precisão, fonte e operação](LIMITE_MUNICIPAL.md).


## Caracterização persistida de todas as bases

As mesmas dezoito bases do catálogo são processadas automaticamente: quinze vetores WFS estaduais, dois rasters WCS e trilhas ArcGIS. Vetores preservam todos os atributos publicados e geometrias recortadas. Declividade e MapBiomas preservam valores/células no GeoTIFF nativo EPSG:4674, com seleção pelo centro e NoData separado. Rótulos/classes vêm do estilo padrão oficial. A fonte visual WMS não é usada para inferir valores numéricos.

O contorno externo AII águas/solos é o recorte comum do protótipo, uma simplificação que não certifica influência temática ou limites de recuperação. SQLite conserva os dados por mina e a aplicação atualiza automaticamente. Data de consulta não é data de levantamento. [Recorte](INFLUENCIA.md), [campos, células, atualização e limites](DADOS_TERRITORIAIS.md).
