# Escolhas territoriais e justificativas para apresentação

Versão 4.0.0. O MVP permite conhecer o território e consultar automaticamente os dados de todas as bases em um recorte comum. Não avalia ou recomenda alternativas de uso futuro.

## Mapa e imagens de contexto

Mantemos Leaflet, fundo OpenStreetMap e Esri World Imagery para concentrar o esforço na integração/automação. Evitamos introduzir faturamento Google e 3D nesta etapa; não houve contratação. Fontes públicas têm regras de uso, atribuição e disponibilidade; não são ilimitadas. [Política dos tiles OSM](https://operations.osmfoundation.org/policies/tiles/) e [datas do World Imagery](https://support.esri.com/en-us/knowledge-base/faq-can-the-date-of-an-image-be-determined-from-the-wor-000012181).

Data/resolução das imagens variam por local e zoom; consulta recente/copyright não significa fotografia recente. A imagem é contexto visual, sem levantamento atual certificado da mina. O protótipo usa fontes públicas; uma aplicação interna exigiria conhecer os dados e sistemas já existentes na Vale.

## Cinco temas e uma fonte municipal

Os cinco temas/dez bases estaduais são um recorte pequeno para MVP, sem validação de especialista da Vale. A quantidade é escolha de escopo; os artigos sustentam a relevância dos assuntos, não prescrevem os cinco seletores nem validam resultados para Horizontes. Trilhas acrescenta fonte municipal para testar integração de infraestruturas distintas.

| Tema | Por que conhecer | Representação implementada | Apoio documental |
|---|---|---|---|
| Relevo e declividade | Entender a configuração regional do terreno e diferenças de inclinação. | Declividade Topodata em seis classes. | Revisão de Pagouni e estudo GIS de Ptolemais: topografia na avaliação territorial. |
| Água e drenagem | Observar rios e corpos d’água no território e entorno. | Principais trechos hidrográficos e massas d’água. | Ptolemais considera rios; Anglo inclui água no planejamento integrado. |
| Solos | Conhecer tipos regionais de solo, um dos componentes físicos do território. | Mapa pedológico de MG, produzido em 2010. Não há diagnóstico de contaminação. | Pagouni aborda propriedades físicas e químicas do solo e condições do local. |
| Vegetação e conservação | Observar cobertura da terra e unidades de conservação cadastradas. | MapBiomas 2025 e UCs estaduais, federais e municipais. | Vale considera vocações ambientais; Anglo contempla terra e natureza; revisão aborda ambiente. |
| Entorno humano e infraestrutura | Observar ocupação urbana e acessos existentes. | Áreas urbanizadas de referência 2022 e rodovias estaduais/federais. | Ptolemais usa proximidade de povoamentos e estradas; Vale aborda vocações socioeconômicas e participação social. |


## Referências e o que realmente sustentam

1. **Pagouni, Pavloudakis, Kapageridis e Yiannakou (2024).** *Transitional and Post-Mining Land Uses: A Global Review of Regulatory Frameworks, Decision-Making Criteria, and Methods*. Land 13(7), 1051. [DOI: 10.3390/land13071051](https://doi.org/10.3390/land13071051). Revisão de 90 artigos, com dimensões físicas, ambientais, sociais, econômicas e técnicas. Apoia olhar multidimensional; não propõe os cinco checkboxes deste MVP.
2. **Estudo aplicado em Ptolemais, Grécia (2023).** *A Geospatial Analysis Model for the Selection of Post-Mining Land Uses in Surface Lignite Mines: Application in the Ptolemais Mines, Greece*. Sustainability 15(19), 14388. [DOI: 10.3390/su151914388](https://doi.org/10.3390/su151914388). Considera declividade, elevação e distâncias a povoamentos, estradas, rios e transmissão elétrica. Apoia a integração GIS desses assuntos; critérios, pesos e resultados locais não foram transplantados para Minas Gerais.
3. **Vale — [Fechamento de mina e Uso Futuro](https://www.vale.com/pt/esg/fechamento-de-mina-e-uso-futuro).** Referência corporativa para conhecer aptidões ambientais e socioeconômicas, participação social e uso futuro. As quatro etapas Conhecer, Conceber, Viabilizar e Implantar não são quatro funcionalidades já implementadas no GeoVale.
4. **Anglo American — [Post-mine land use ecosystem model](https://www.angloamerican.com/our-stories/trusted-corporate-leader/developing-our-post-mine-land-use-ecosystem-model).** Modelo integrado de Amandelbult, África do Sul, envolvendo temas sociais, água, terra/natureza, resíduos e energia/carbono. Suas cinco frentes de valor não equivalem às cinco camadas GIS deste projeto.

## Um território comum, dados completos e visibilidade independente

O contorno externo AII águas/solos do parecer foi escolhido como **recorte comum de caracterização**. Simplifica a jornada: a mina já tem uma extensão definida e todas as fontes são organizadas nela. A mina sombreada oferece orientação cartográfica. Não se exige delimitação do engenheiro nesta etapa.

Essa opção é uma adaptação do MVP: a AII original é do meio físico do projeto conjunto Tamanduá/Horizontes, não delimitação oficial de todos os temas ou limite de fechamento. Mantemos fonte, figura/página, data e aviso de aproximação. Não foi obtido plano de fechamento específico de Horizontes. [Evidência e precisão](INFLUENCIA.md).

O [plano de fechamento Minas-Rio da Anglo](https://brasil.angloamerican.com/~/media/Files/A/Anglo-American-Group-v5/Brazil/sustentabilidade/plano-de-fechamento-de-mina-do-minas-rio.pdf), revisão de junho/2021, distingue em 11.7–11.8 (PDF p. 64/impressa 58) ações na ADA e consideração da AID se há interferência a reabilitar, além do público do meio físico. Isso sustenta investigar contexto sem supor intervenção em toda a influência. Não prescreve nosso recorte ou automação, nem transfere limites do Minas-Rio para a Vale.

Guardar dados por mina e atualizar todas as bases automaticamente demonstra as atividades da vaga de **integrar dados e automatizar etapas de avaliação**. Evita depender de quais camadas o usuário decidiu enxergar. O relatório JSON é gerado pelos dados reais e não por tabela manual de valores; fontes, datas e limitações ficam no arquivo e na documentação. A tela se concentra no mapa. Vetores mantêm todos os atributos; rasters conservam as células, além de resumos. Fontes sem resposta válida são explicitamente indisponíveis.

## Fala curta para apresentação

> “O engenheiro seleciona a mina e encontra um território e seus dados já organizados. Influência mostra todas as camadas dentro do território; os seletores ampliam cada tema para ver sua continuidade fora dele. O relatório JSON considera todas as bases integradas, independentemente da visualização. Os dados vêm das APIs oficiais, são recortados, guardados por mina e atualizados automaticamente, com origem e data. Usamos um recorte documental comum como simplificação do MVP. É uma caracterização preliminar para apoiar a discussão de fechamento e uso futuro, sem substituir avaliação especializada.”

## Limites

Rios/trechos, solos, vegetação, conservação, urbanização, vias e trilhas são representações heterogêneas, com idades/escalas próprias. Não comprovam ausência de risco, qualidade da água, contaminação, estabilidade, permissão de acesso ou aptidão. Topodata deriva de SRTM de 2000; não descreve a cava atual. Percentual matricial é de células válidas, não área medida. As fontes não substituem estudos, licenciamento, campo ou escuta das comunidades. O sistema não define beneficiários ou recomenda intervenções.

[Dados automáticos e método](DADOS_TERRITORIAIS.md), [ferramentas e motivos](FERRAMENTAS.md).
