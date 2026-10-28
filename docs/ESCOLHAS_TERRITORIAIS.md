# Escolhas territoriais e justificativas para apresentação

Versão 4.6.3. O MVP permite conhecer o território e consultar automaticamente os dados de todas as bases em um recorte comum, separando área minerada e entorno, e ordena usos por setor da área minerada para discussão. As escolhas da sugestão e da IA estão em [Multicritério e IA](MULTICRITERIO.md).

## Mapa e imagens de contexto

Mantemos Leaflet, fundo OpenStreetMap e Esri World Imagery para concentrar o esforço na integração/automação. Evitamos introduzir faturamento Google e 3D nesta etapa; não houve contratação. Fontes públicas têm regras de uso, atribuição e disponibilidade; não são ilimitadas. [Política dos tiles OSM](https://operations.osmfoundation.org/policies/tiles/) e [datas do World Imagery](https://support.esri.com/en-us/knowledge-base/faq-can-the-date-of-an-image-be-determined-from-the-wor-000012181).

Data/resolução das imagens variam por local e zoom; consulta recente/copyright não significa fotografia recente. A imagem é contexto visual, sem levantamento atual certificado da mina. O protótipo usa fontes públicas; uma aplicação interna exigiria conhecer os dados e sistemas já existentes na Vale.

## Seis temas estaduais e uma fonte municipal

Os seis temas/quinze bases estaduais são um recorte pequeno para MVP, sem validação de especialista da Vale. A quantidade é escolha de escopo; os artigos sustentam a relevância dos assuntos, não prescrevem os cinco seletores nem validam resultados para Horizontes. Trilhas acrescenta fonte municipal para testar integração de infraestruturas distintas.

| Tema | Por que conhecer | Representação implementada | Apoio documental |
|---|---|---|---|
| Relevo e cavidades | Entender a configuração regional do terreno e onde cavernas podem restringir intervenções. | Declividade Topodata em seis classes e potencial de cavidades do CECAV. | Revisão de Pagouni e estudo GIS de Ptolemais: topografia na avaliação territorial; cavidades são patrimônio protegido (Decreto 99.556/1990). |
| Água e drenagem | Observar rios, corpos d’água, classe legal e disponibilidade hídrica. | Principais trechos, massas d’água, enquadramento e vazões regionalizadas do Igam. | Ptolemais considera rios; Anglo inclui água no planejamento integrado. |
| Solos | Conhecer tipos regionais de solo, um dos componentes físicos do território. | Mapa pedológico de MG, produzido em 2010. Não há diagnóstico de contaminação. | Pagouni aborda propriedades físicas e químicas do solo e condições do local. |
| Vegetação e conservação | Observar cobertura da terra, área minerada e restrições de conservação. | MapBiomas 2025, UCs por grupo do SNUC e APPs hídricas da FBDS. | Vale considera vocações ambientais; Anglo contempla terra e natureza; revisão aborda ambiente. |
| Entorno humano e infraestrutura | Observar ocupação urbana e acessos existentes. | Áreas urbanizadas de referência 2022 e rodovias estaduais/federais, com distância à área minerada. | Ptolemais usa proximidade de povoamentos e estradas; Vale aborda vocações socioeconômicas e participação social. |
| Barragens | Conhecer os passivos do fechamento e as restrições a jusante. | Barragens de rejeitos e resíduos da FEAM, ano base 2024, com método construtivo. | Lei 14.066/2020 exige descaracterizar barragens alteadas a montante. |


## Referências e o que realmente sustentam

1. **Pagouni, Pavloudakis, Kapageridis e Yiannakou (2024).** *Transitional and Post-Mining Land Uses: A Global Review of Regulatory Frameworks, Decision-Making Criteria, and Methods*. Land 13(7), 1051. [DOI: 10.3390/land13071051](https://doi.org/10.3390/land13071051). Revisão de 90 artigos, com dimensões físicas, ambientais, sociais, econômicas e técnicas. Apoia olhar multidimensional; não propõe os cinco checkboxes deste MVP.
2. **Servou, Paraskevis, Roumpos e Pavloudakis (2023), Ptolemais, Grécia.** *A Geospatial Analysis Model for the Selection of Post-Mining Land Uses in Surface Lignite Mines: Application in the Ptolemais Mines, Greece*. Sustainability 15(19), 14388. [DOI: 10.3390/su151914388](https://doi.org/10.3390/su151914388). Considera declividade, elevação e distâncias a povoamentos, estradas, rios e transmissão elétrica. Apoia a integração GIS desses assuntos; critérios, pesos e resultados locais não foram transplantados para Minas Gerais.
3. **Vale — [Fechamento de mina e Uso Futuro](https://www.vale.com/pt/esg/fechamento-de-mina-e-uso-futuro).** Referência corporativa para conhecer aptidões ambientais e socioeconômicas, participação social e uso futuro. As quatro etapas Conhecer, Conceber, Viabilizar e Implantar não são quatro funcionalidades já implementadas no GeoVale.
4. **Anglo American — [Post-mine land use ecosystem model](https://www.angloamerican.com/our-stories/trusted-corporate-leader/developing-our-post-mine-land-use-ecosystem-model).** Modelo integrado de Amandelbult, África do Sul, envolvendo temas sociais, água, terra/natureza, resíduos e energia/carbono. Suas cinco frentes de valor não equivalem às camadas GIS deste projeto.

## Por que a versão 4.3.0 separa área minerada e entorno

A 4.2.0 descrevia os 15.308 ha da AII como um bloco. A revisão crítica do MVP mostrou que o objeto do pós-mineração ficava escondido. Cada mudança tem o motivo e a evidência abaixo.

| Decisão | Por quê | Evidência |
|---|---|---|
| Área minerada como alvo; AII como contexto | O fechamento atua onde houve intervenção. A AII é a área de impacto indireto da ampliação. O polígono OSM (512,2 ha) cobre só a cava; a cobertura oficial mostra 3.173,3 ha minerados no recorte, incluindo pilhas e barragens. | Plano Minas-Rio, 11.7–11.8 (ações na ADA; AID quando há interferência a reabilitar); classe 30 Mineração do MapBiomas; medidas do próprio recorte. |
| Hectares a partir das células | O engenheiro lê área, não contagem de células. Medir cada célula em UTM 23S evita medida em graus. | A soma das células deu 15.309,2 ha (declividade) e 15.308,9 ha (cobertura) para um recorte de 15.308,5 ha. |
| UCs por grupo do SNUC | A APA Sul RMBH cobre 100% do recorte e escondia a restrição real: proteção integral admite apenas uso indireto; uso sustentável compatibiliza uso e conservação. | Lei 9.985/2000, art. 7º; campo `grupo` publicado em cada UC. |
| Tema Barragens | A Vale renomeou juntas a mina e a barragem Capitão do Mato para Horizontes. Barragens alteadas a montante devem ser descaracterizadas: é passivo central do fechamento. | [Comunicado da Vale](https://www.vale.com/ar/w/vale-altera-nome-de-mina-e-barragem-em-nova-lima-e-reforca-posicionamento-antirracista); Lei 14.066/2020; inventário FEAM, ano base 2024 (10 barragens no recorte, 2 a montante). |
| Potencial de cavidades | Formação ferrífera e canga concentram cavernas; cavidades são patrimônio protegido e exigem prospecção antes de intervir. | Decreto 99.556/1990; mapa do CECAV (Jansen, Cavalcanti e Lamblém, 2012), escala 1:2.500.000. |
| APPs hídricas | São faixas legais a manter ou recompor, que o fechamento precisa respeitar. | Lei 12.651/2012, arts. 4º e 7º; mapeamento FBDS. |
| Enquadramento | A classe do trecho define os limites de qualidade e se é possível lançar efluente. | Resolução CONAMA 357/2005; enquadramento publicado pelo Igam (DN COPAM 05/1993 no Rio das Velhas). |
| Vazão Q7,10 | É a vazão de referência para outorga em MG; mostra quanta água existe na estiagem para um uso futuro. Substitui a vazão de projeto inventada. | Portaria Igam 48/2019, art. 2º (Q7,10 como referência) e art. 3º (captações até 50% dela). |
| Turbidez, ferro e manganês nos pontos de água | Em bacias com minério de ferro, esses parâmetros são os que mais excedem os limites; o pH sozinho diz pouco. Drenagem ácida é típica de minério sulfetado, não de itabirito. | Nascimento et al. (2019), Rev. Ambiente & Água 14(5), [DOI 10.4136/ambi-agua.2383](https://doi.org/10.4136/ambi-agua.2383): ferro e manganês acima da CONAMA 357 em bacia com rejeito de minério de ferro. |
| Pontos simulados com coordenada | Sem localização, um valor não entra no mapa nem na análise. Com a classe real do trecho, a checagem contra o limite legal fica automática. | CONAMA 357/2005, arts. 14 a 17 (limites por classe) e 42 (classe 2 sem enquadramento). |
| Referências de estabilidade e compactação | Dão significado ao número simulado: atende ou não a um valor usual do setor. | ABNT NBR 13029:2017 (FS 1,5 no talude geral, freática normal); Taylor et al. (1966), limite usual de 2 MPa para raízes. |
| Comentários com implicação | O engenheiro precisa do "e daí?" do dado, não só do que ele não é. A regra continua sem classificar aptidão. | Revisão de Pagouni et al. (2024): critérios físicos, ambientais e sociais orientam a escolha de uso futuro. |

## Um território comum, dados completos e visibilidade independente

O contorno externo AII águas/solos do parecer foi escolhido como **recorte comum de caracterização**. Simplifica a jornada: a mina já tem uma extensão definida e todas as fontes são organizadas nela. A mina sombreada oferece orientação cartográfica. Não se exige delimitação do engenheiro nesta etapa.

Essa opção é uma adaptação do MVP: a AII original é do meio físico do projeto conjunto Tamanduá/Horizontes, não delimitação oficial de todos os temas ou limite de fechamento. Mantemos fonte, figura/página, data e aviso de aproximação. Não foi obtido plano de fechamento específico de Horizontes. [Evidência e precisão](INFLUENCIA.md).

O [plano de fechamento Minas-Rio da Anglo](https://brasil.angloamerican.com/~/media/Files/A/Anglo-American-Group-v5/Brazil/sustentabilidade/plano-de-fechamento-de-mina-do-minas-rio.pdf), revisão de junho/2021, distingue em 11.7–11.8 (PDF p. 64/impressa 58) ações na ADA e consideração da AID se há interferência a reabilitar, além do público do meio físico. Isso sustenta investigar contexto sem supor intervenção em toda a influência. Não prescreve nosso recorte ou automação, nem transfere limites do Minas-Rio para a Vale.

Guardar dados por mina e atualizar todas as bases automaticamente demonstra as atividades da vaga de **integrar dados e automatizar etapas de avaliação**. Evita depender de quais camadas o usuário decidiu enxergar. Os blocos geográficos do relatório PDF são gerados pelos dados reais; fontes, datas e limitações ficam no arquivo e na documentação. A tela se concentra no mapa. Vetores mantêm todos os atributos; rasters conservam as células, além de resumos. Fontes sem resposta válida são explicitamente indisponíveis.

## Fala curta para apresentação

> “O engenheiro seleciona a mina e encontra um território e seus dados já organizados. Influência mostra todas as camadas dentro do território; os seletores ampliam cada tema para ver sua continuidade fora dele. O PDF considera todas as bases integradas, separa a área minerada do entorno e inclui um cenário técnico fictício em seção separada. Os dados vêm das APIs oficiais, são recortados, guardados por mina e atualizados automaticamente, com origem e data. Usamos um recorte documental comum como simplificação do MVP. É uma caracterização preliminar para apoiar a discussão de fechamento e uso futuro, sem substituir avaliação especializada.”

## Limites

Rios/trechos, solos, vegetação, conservação, urbanização, vias e trilhas são representações heterogêneas, com idades/escalas próprias. Não comprovam ausência de risco, qualidade da água, contaminação, estabilidade, permissão de acesso ou aptidão. Topodata deriva de SRTM de 2000; não descreve a cava atual. Áreas matriciais somam células medidas em UTM 23S. A área minerada vem da classe Mineração do MapBiomas e inclui cavas, pilhas e barragens de mais de uma mina. As fontes não substituem estudos, licenciamento, campo ou escuta das comunidades. O sistema não define beneficiários ou recomenda intervenções.

[Dados automáticos e método](DADOS_TERRITORIAIS.md), [ferramentas e motivos](FERRAMENTAS.md).

## Cenário técnico e relatório

O cenário autorizado usa a estrutura de planejamento, vistoria e reabilitação do plano Minas-Rio, seções 8.2.1.3-8.2.1.5, 11.11.3 e 11.11.7.6. Considera, ficticiamente, três pontos de água, estabilidade de pilha, compactação, sobrevivência de mudas, uma edificação, acesso e participação. Os pontos ficam sobre dados reais; a água é conferida com a classe real do trecho e os limites da CONAMA 357/2005. Não copia parâmetros geotécnicos, custos ou resultados de outra mina como se fossem da Horizontes. Cada premissa traz sua referência metodológica.

A escolha demonstra uma entrada técnica complementar às APIs, em relatório legível com nossa marca, sem substituir dados reais ou inventar vistorias executadas. A síntese reúne condições e lacunas para a etapa multicritério. [Estrutura e rastreabilidade](RELATORIO.md), [sugestão e porquês](MULTICRITERIO.md).

## Dado, conhecimento e decisão

Para apresentar: “As fontes e cálculos geram fatos reproduzíveis. As fichas mostram o mapa e os dados de cada tema, mais uma leitura contextual separada por dado. Ensaios e informações que as camadas não trazem são demonstrados em uma ficha fictícia com asterisco, com pontos no mapa conferidos automaticamente com limites de referência. Depois, a sugestão multicritério divide a área minerada em setores, exclui o que a lei não admite, soma critérios com pesos AHP que o engenheiro pode mudar e mostra se a ordem resiste a ±20% nos pesos. A IA só explica essa sugestão, com números conferidos; sem chave, a explicação é por regras e o PDF diz isso. ML preditivo precisaria de histórico rotulado que não possuímos. A decisão de uso é do engenheiro e das partes interessadas.”
