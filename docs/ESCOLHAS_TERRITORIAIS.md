# Justificativa do mapa e dos cinco temas

Registro atualizado em 26/10/2026 para o MVP GeoVale. A etapa implementada é conhecer visualmente o território: mapa, localização da Mina Horizontes, sobreposições e delimitação de várias áreas de estudo, com cadastro ANM e contexto municipal IBGE. Ainda não existe avaliação ou recomendação de uso futuro.

## Por que manter o mapa atual

Mantemos Leaflet, OpenStreetMap para o fundo cartográfico e Esri World Imagery para o fundo de imagens. Aproveitamos a navegação existente e evitamos introduzir uma conta de faturamento Google e uma integração 3D nesta etapa. Não houve contratação de Google Maps Platform. Não classificamos os serviços atuais como gratuitos e ilimitados: permanecem sujeitos às condições de uso, atribuição, disponibilidade e consumo do fornecedor. OSM estabelece [regras específicas para os tiles públicos](https://operations.osmfoundation.org/policies/tiles/); a Esri orienta a [conferir as condições de cada item e preservar os créditos](https://resources.esri.ca/education-and-research/how-to-cite-arcgis-maps-and-data).

A imagem serve de contexto visual, não de levantamento atual certificado. Datas e resolução variam por local e zoom; consulta recente ou ano de copyright não significa fotografia recente. A discussão visual mostrou divergência entre casas observadas em Google Earth e Esri. Consultas pontuais de metadados não foram suficientes para comprovar a correspondência com cada imagem exibida; portanto não atribuímos uma data única ao mapa. Referência: [Esri — datas de World Imagery](https://support.esri.com/en-us/knowledge-base/faq-can-the-date-of-an-image-be-determined-from-the-wor-000012181).

Há evidência pública de que a Vale já trabalha com bancos de dados integrados para fechamento e aptidões territoriais e com tecnologias de monitoramento geotécnico. Isso não comprova qual sistema ou imagem atual ela possui da Horizontes. Referências: [Uso futuro e dados integrados](https://saladeimprensa.vale.com/pt/esg/fechamento-de-mina-e-uso-futuro) e [Tecnologia](https://www.vale.com/pt/esg/tecnologia).

Formulação para a apresentação: **“O protótipo usa fontes públicas para demonstrar integração e exploração do território. Uma aplicação interna exigiria avaliar os dados, sistemas e necessidades já existentes na Vale.”** O valor pretendido está em organizar informação útil à avaliação, não em substituir sistemas corporativos ou apresentar um novo provedor de imagens.

## Por que cinco temas

É um recorte pequeno e verificável para um MVP sem validação de especialista da Vale. São **cinco grupos de informação**, implementados por dez bases geográficas. A quantidade é uma escolha de escopo do projeto, não uma conclusão dos artigos nem uma norma da Vale. As referências apoiam a relevância dos assuntos, sem validar automaticamente a seleção, as fontes locais ou qualquer decisão sobre a mina.

| Tema | Por que conhecer | Representação implementada | Apoio documental |
|---|---|---|---|
| Relevo e declividade | Entender a configuração regional do terreno e diferenças de inclinação. | Declividade Topodata em seis classes. | Revisão de Pagouni e estudo GIS de Ptolemais: topografia na avaliação territorial. |
| Água e drenagem | Observar rios e corpos d’água no território e entorno. | Principais trechos hidrográficos e massas d’água. | Ptolemais considera rios; Anglo inclui água no planejamento integrado. |
| Solos e condição ambiental | Conhecer tipos regionais de solo, um dos componentes físicos do território. | Mapa pedológico de MG, produzido em 2010. Não há diagnóstico de contaminação. | Pagouni aborda propriedades físicas e químicas do solo e condições do local. |
| Vegetação e conservação | Observar cobertura da terra e unidades de conservação cadastradas. | MapBiomas 2025 e UCs estaduais, federais e municipais. | Vale considera vocações ambientais; Anglo contempla terra e natureza; revisão aborda ambiente. |
| Entorno humano e infraestrutura | Observar ocupação urbana e acessos existentes. | Áreas urbanizadas de referência 2022 e rodovias estaduais/federais. | Ptolemais usa proximidade de povoamentos e estradas; Vale aborda vocações socioeconômicas e participação social. |

A interface abre com os cinco controles estaduais e a opção municipal de trilhas desmarcados. Marcar carrega o tema por WMS; desmarcar remove. É possível combinar temas e reduzir sua intensidade para preservar a leitura das sobreposições. A lista aparece como “Entorno e infraestrutura” para manter o rótulo curto.

## Referências e o que realmente sustentam

1. **Pagouni, Pavloudakis, Kapageridis e Yiannakou (2024).** *Transitional and Post-Mining Land Uses: A Global Review of Regulatory Frameworks, Decision-Making Criteria, and Methods*. Land 13(7), 1051. [DOI: 10.3390/land13071051](https://doi.org/10.3390/land13071051). Revisão de 90 artigos, com dimensões físicas, ambientais, sociais, econômicas e técnicas. Apoia olhar multidimensional; não propõe os cinco checkboxes deste MVP.
2. **Estudo aplicado em Ptolemais, Grécia (2023).** *A Geospatial Analysis Model for the Selection of Post-Mining Land Uses in Surface Lignite Mines: Application in the Ptolemais Mines, Greece*. Sustainability 15(19), 14388. [DOI: 10.3390/su151914388](https://doi.org/10.3390/su151914388). Considera declividade, elevação e distâncias a povoamentos, estradas, rios e transmissão elétrica. Apoia a integração GIS desses assuntos; critérios, pesos e resultados locais não foram transplantados para Minas Gerais.
3. **Vale — [Fechamento de mina e Uso Futuro](https://www.vale.com/pt/esg/fechamento-de-mina-e-uso-futuro).** Referência corporativa para conhecer aptidões ambientais e socioeconômicas, participação social e uso futuro. As quatro etapas Conhecer, Conceber, Viabilizar e Implantar não são quatro funcionalidades já implementadas no GeoVale.
4. **Anglo American — [Post-mine land use ecosystem model](https://www.angloamerican.com/our-stories/trusted-corporate-leader/developing-our-post-mine-land-use-ecosystem-model).** Modelo integrado de Amandelbult, África do Sul, envolvendo temas sociais, água, terra/natureza, resíduos e energia/carbono. Suas cinco frentes de valor não equivalem às cinco camadas GIS deste projeto.

## Limites para a apresentação

Os cinco temas têm cobertura de Minas Gerais; a sexta opção de trilhas tem cobertura municipal em Nova Lima. O fundo permite navegação mundial. Ausência de feição visível não comprova ausência de risco ou restrição. Não há cruzamento espacial, cálculo de distância, pesos, classificação de aptidão ou recomendação nesta etapa. As sobreposições não substituem estudos geotécnicos, hidrológicos, geoquímicos, licenciamento e escuta das comunidades.

O Topodata usa SRTM de fevereiro de 2000, refinado de cerca de 90 m para pixel de aproximadamente 30 m; não é topografia atual da cava. [Fonte INPE](https://data.inpe.br/dados/topodata/). O mapa pedológico não informa a qualidade atual de solo minerado. A disponibilidade estadual de dados não garante precisão adequada para projetar uma intervenção na mina. Proveniência das dez bases em [Dados geográficos](DADOS_GEOGRAFICOS.md).

## Por que acrescentar trilhas de outra fonte

A opção **Trilhas de Nova Lima** testa uma necessidade concreta: combinar a infraestrutura estadual com informação municipal mais específica. Caminhos cadastrados ajudam a observar conexões com o entorno e a levantar questões sobre acesso e possíveis usos recreativos. Não demonstram por si só viabilidade, segurança ou direito de passagem. A motivação é testar integração de outra fonte, não afirmar que as referências acima exigem uma sexta camada ou validam esses traçados.

A fonte escolhida foi a Prefeitura de Nova Lima porque o portal indicado pelo usuário publica uma camada vetorial consultável por ArcGIS REST. Não se copiou o aplicativo inteiro. No inventário WMS da IDE-Sisema consultado em 24/10/2026 não foram encontrados títulos contendo “trilh”; as dez bases integradas não contêm esse cadastro. Isso não prova inexistência em toda fonte estadual. [Proveniência e consulta](TRILHAS_NOVA_LIMA.md).

O desenho manual permite ao engenheiro escolher o recorte que pretende estudar, incluindo uma parte da mina e/ou seu entorno. Essa delimitação não substitui limite oficial, validação técnica ou consulta cadastral. A etapa implementada termina na confirmação da geometria; não há análise de aptidão resultante do desenho.

## Contexto municipal e recortes independentes

O IBGE foi acrescentado para identificar visualmente Nova Lima quando a mina é selecionada, sem exibir todas as cidades. A ANM foi acrescentada como fonte primária do cadastro minerário associado. São funções de localização e consulta cadastral, não novos critérios de aptidão. O engenheiro pode delimitar várias partes separadas (cava, morro, barragem), editar um recorte derivado da ANM ou desenhar do zero. Nenhuma escolha significa que toda a área do processo ou do município esteja disponível para uso futuro. [Município](LIMITE_MUNICIPAL.md), [ANM](ANM.md), [Áreas](AREA_ESTUDO.md).
