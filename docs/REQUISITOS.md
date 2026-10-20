# Requisitos do GeoVale

Os requisitos de negócio da Etapa 1 foram validados, revisados e tiveram seu
encerramento aprovado em 20/10/2026. A Etapa 2 — Engenharia de requisitos do
sistema foi iniciada com a identificação dos atores. Este documento permanece
em elaboração incremental; os demais requisitos serão discutidos e registrados
em entregas posteriores.

## Requisitos de negócio

### RNG-01 — Problema de negócio

**Estado:** aprovado pelo responsável pelo projeto em 19/10/2026.

**Descrição aprovada:**

A equipe responsável pela avaliação de áreas pós-mineração precisa comparar possíveis usos futuros considerando características do terreno, restrições e critérios de custo e benefício.

O problema que o GeoVale pretende tratar é a dificuldade de reunir essas informações e justificar a comparação entre alternativas de forma organizada e rastreável, deixando explícitos as fontes utilizadas, os critérios considerados e as limitações da análise.

### RNG-02 — Objetivo do sistema

**Estado:** aprovado pelo responsável pelo projeto em 19/10/2026.

**Descrição aprovada:**

Disponibilizar uma ferramenta demonstrativa de apoio à avaliação e comparação de possíveis usos futuros de áreas pós-mineração, reunindo informações geográficas e critérios de decisão para apresentar resultados organizados, compreensíveis e rastreáveis.

A comparação deverá permitir ao especialista consultar as informações utilizadas, os critérios considerados e as limitações da análise, com identificação clara de dados reais e simulados, para subsidiar sua tomada de decisão.

**Resultado esperado:**

O resultado esperado é que o usuário consiga compreender quais alternativas foram avaliadas, como foram comparadas e por que receberam determinada classificação.

### RNG-03 — Público-alvo

**Estado:** aprovado pelo responsável pelo projeto em 19/10/2026.

**Descrição aprovada:**

- **Público principal:** engenheiros e profissionais técnicos envolvidos na avaliação e no planejamento de usos futuros de áreas pós-mineração. Utilizarão o sistema para organizar informações da área, configurar critérios e comparar alternativas.
- **Público interessado nos resultados:** gestores e responsáveis pelo planejamento dessas áreas, que consultarão mapas, comparações e relatórios para compreender as alternativas avaliadas e subsidiar decisões.

**Cenário de demonstração:**

No cenário de demonstração, esses grupos serão representados pelo **engenheiro que realiza a análise** e pelo **gestor da Vale que avalia os resultados apresentados**.

### RNG-04 — Benefícios esperados

**Estado:** aprovado pelo responsável pelo projeto em 19/10/2026.

**Descrição aprovada:**

1. **Organização das informações:** reunir dados da área, fontes e critérios utilizados, facilitando sua consulta.
2. **Comparação estruturada:** avaliar alternativas com critérios e pesos explícitos, mantendo as restrições eliminatórias separadas das pontuações.
3. **Rastreabilidade da análise:** permitir compreender como os resultados foram obtidos, quais informações foram utilizadas e quais limitações existem.
4. **Comunicação técnica:** apresentar mapas, comparações e relatórios compreensíveis, facilitando a discussão entre profissionais técnicos e gestores.

Esses são **benefícios pretendidos**, que deverão ser verificados na demonstração do MVP. Ainda não representam resultados comprovados nem ganhos medidos de tempo ou custo.

### RNG-05 — Escopo do MVP

**Estado:** aprovado pelo responsável pelo projeto em 20/10/2026.

**Descrição aprovada:**

O GeoVale contemplará um fluxo demonstrativo de avaliação de uma área de estudo em Minas Gerais, incluindo:

1. **Envio e validação:** receber um arquivo geográfico e identificar a área informada.
2. **Análise geográfica:** calcular características da área e cruzar camadas públicas para identificar distâncias, sobreposições e alertas.
3. **Comparação de alternativas:** cadastrar possíveis usos futuros e compará-los com critérios, notas e pesos definidos, aplicando restrições eliminatórias separadamente das pontuações.
4. **Dashboard:** apresentar mapa, características, alertas e classificação das alternativas, com fontes, parâmetros e limitações identificados.
5. **Persistência:** salvar e recuperar análises, incluindo os parâmetros utilizados e seus resultados.
6. **Relatório:** exportar os resultados para consulta e apresentação técnica.
7. **Machine Learning demonstrativo:** estimar aptidão física e utilizar a previsão como uma das entradas da comparação, identificando a origem dos dados de treinamento e as limitações do modelo.

**Sequência de implementação e entrega do ML:**

O fluxo principal será desenvolvido primeiro. O Machine Learning será desenvolvido na Etapa 8, após o funcionamento do fluxo principal, e integrará a versão final do MVP apresentada na demonstração, com o ML integrado, testado e documentado.

**Dados do cenário demonstrativo:**

Dados geográficos públicos serão utilizados quando disponíveis. Áreas, regras, notas e dados simulados serão claramente identificados.

### RNG-06 — Limitações do MVP

**Estado:** aprovado pelo responsável pelo projeto em 20/10/2026.

**Descrição aprovada:**

1. **Cenário delimitado:** a demonstração será validada em uma área de estudo em Minas Gerais. A aplicação em outras áreas exigirá conferir os dados e a adequação das regras utilizadas.
2. **Qualidade dos dados:** os resultados dependerão da cobertura, resolução, atualização e qualidade das bases disponíveis. Fontes, datas e limitações conhecidas deverão ser registradas.
3. **Informações demonstrativas:** regras, notas, custos e benefícios poderão ser simulados quando faltarem informações reais, com identificação explícita. A classificação refletirá os dados e parâmetros utilizados.
4. **Limitação do ML:** o modelo integrará o MVP final. Quando treinado com dados sintéticos, demonstrará o funcionamento técnico do algoritmo, sem comprovar capacidade preditiva em áreas reais.
5. **Responsabilidade pela decisão:** os resultados apoiarão a análise de especialistas e não substituirão estudos ou avaliações ambientais, legais e de segurança, nem constituirão autorização para utilizar uma área.

### RNG-07 — Critérios de sucesso do MVP

**Estado:** aprovado pelo responsável pelo projeto em 20/10/2026.

**Descrição aprovada:**

| Critério | Evidência esperada |
| --- | --- |
| **Fluxo completo** | Executar o cenário demonstrativo desde o envio do arquivo geográfico até a apresentação dos resultados e a exportação do relatório. |
| **Comparação explicável** | Comparar pelo menos duas alternativas, apresentando critérios, notas, pesos e classificação. Demonstrar que uma restrição eliminatória não é compensada por uma pontuação alta. |
| **Rastreabilidade** | Consultar fontes, datas, parâmetros e limitações da análise, identificando claramente informações reais e simuladas. |
| **ML integrado** | O modelo receber atributos da análise geográfica, retornar uma previsão e utilizá-la na comparação. Origem do treinamento, avaliação e limitações deverão estar documentadas, com testes reproduzíveis. |
| **Persistência** | Salvar uma análise e recuperá-la com seus parâmetros e resultados preservados. |
| **Comunicação compreensível** | O responsável pelo projeto conseguir identificar, no dashboard e no relatório, as alternativas avaliadas, os fatores da classificação e as limitações dos resultados. |
| **Execução reproduzível** | Instalar e executar o sistema em um ambiente limpo seguindo a documentação, com os testes previstos executados e seus resultados registrados. |

**Momento de verificação:**

A comprovação de atendimento desses critérios ocorrerá durante a validação e a demonstração do MVP, após sua implementação. Os critérios definem as evidências esperadas; os resultados das verificações serão registrados quando executadas.

## Requisitos do sistema

### Atores e responsabilidades

**Estado:** aprovado pelo responsável pelo projeto em 20/10/2026.

**Origem:** público-alvo e cenário de demonstração definidos no RNG-03.

Os atores representam os papéis das pessoas que utilizarão o GeoVale:

| Identificador | Ator | Responsabilidades previstas |
| --- | --- | --- |
| **AT-01** | **Engenheiro/analista** | Fornecer o arquivo geográfico da área, configurar a análise e comparar alternativas de uso futuro. |
| **AT-02** | **Gestor** | Consultar mapas, resultados e relatórios para compreender as alternativas avaliadas e apoiar decisões. |

### RF-01 — Envio e validação do arquivo geográfico

**Estado:** definição, formato inicial, estrutura e tipos de geometria
aprovados pelo responsável pelo projeto em 20/10/2026; limites de entrada,
regras adicionais de validade das geometrias e tratamento de múltiplas áreas
ainda pendentes de detalhamento.

**Ator:** AT-01 — Engenheiro/analista.

**Origem:** capacidade de envio e validação definida no RNG-05.

**Prioridade:** essencial para o fluxo principal do MVP.

**Descrição aprovada:**

O sistema deverá permitir que o engenheiro/analista envie o arquivo geográfico
da área de estudo e verificar sua adequação antes de iniciar a análise.
Um arquivo válido permitirá prosseguir; arquivos vazios, corrompidos ou
incompatíveis deverão ser rejeitados com mensagem compreensível. Falhas de
validação deverão impedir o processamento da análise.

O formato inicial aceito será GeoJSON, conforme a
[RFC 7946](https://www.rfc-editor.org/rfc/rfc7946), com extensão `.geojson`.
A validação deverá conferir a extensão e o conteúdo; a extensão isolada não
será suficiente para considerar o arquivo válido. Um arquivo que atenda ao
formato inicial poderá prosseguir às demais validações de entrada.

A estrutura inicial aceita pelo MVP será um objeto `FeatureCollection`, cujo
campo `features` deverá ser uma lista não vazia composta somente por objetos
`Feature`. Cada `Feature` deverá conter `geometry` como objeto de geometria
não nulo e `properties` como objeto de atributos ou `null`. Essas condições
são restrições de entrada do GeoVale; a RFC admite coleções vazias e geometrias
nulas, que serão rejeitadas nessa entrada do MVP. A aprovação estrutural
permitirá prosseguir às demais validações, incluindo a conferência dos tipos
de geometria definidos abaixo, sem resolver as regras adicionais de validade,
limites ou tratamento de múltiplas áreas.

Os tipos de geometria aceitos para representar a área de estudo serão
`Polygon` e `MultiPolygon`. Um `Polygon` representa uma área contínua; um
`MultiPolygon` reúne partes poligonais em uma única geometria, permitindo
representar partes separadas. Esses tipos representam superfícies adequadas
ao cálculo da extensão do terreno previsto no RF-03.

Geometrias dos tipos `Point`, `MultiPoint`, `LineString`, `MultiLineString`
e `GeometryCollection` serão rejeitadas nessa entrada do MVP. A rejeição de
`GeometryCollection` também se aplica quando seus componentes forem somente
polígonos. A aceitação do tipo não comprova a validade completa da geometria
nem define como tratar arquivos com mais de uma `Feature`; essas regras
permanecem pendentes nos RF-01 e RF-02.

**Critérios de aceitação:**

| Cenário | Resultado esperado |
| --- | --- |
| Arquivo válido conforme as regras de entrada especificadas | Permitir prosseguir para a análise. |
| Arquivo vazio | Rejeitar o arquivo e informar o problema com mensagem compreensível. |
| Arquivo corrompido | Rejeitar o arquivo e informar o problema com mensagem compreensível. |
| Arquivo incompatível com as regras de entrada especificadas | Rejeitar o arquivo e informar o problema com mensagem compreensível. |
| Falha em uma validação | Impedir o processamento da análise a partir do arquivo rejeitado. |
| Arquivo `.geojson` com conteúdo GeoJSON válido | Prosseguir às demais validações de entrada. |
| Arquivo `.geojson` vazio ou com JSON malformado | Rejeitar o arquivo com mensagem compreensível. |
| Arquivo `.geojson` contendo JSON válido que não represente GeoJSON | Rejeitar o arquivo como conteúdo incompatível, com mensagem compreensível. |
| Arquivo com extensão não aceita | Rejeitar o arquivo e informar que o formato inicial aceito é `.geojson`. |
| Objeto `FeatureCollection` com os campos estruturais exigidos | Prosseguir às demais validações de entrada. |
| Objeto principal de outro tipo | Rejeitar o arquivo e informar que a estrutura inicial aceita pelo MVP é `FeatureCollection`. |
| Campo `features` ausente, diferente de lista ou vazio | Rejeitar o arquivo com mensagem compreensível. |
| Item de `features` que não seja `Feature`, ou com `geometry` ausente, nula ou diferente de objeto de geometria | Rejeitar o arquivo com mensagem compreensível. |
| Campo `properties` ausente ou cujo valor não seja um objeto nem `null` | Rejeitar o arquivo com mensagem compreensível. |
| Geometria do tipo `Polygon` | Prosseguir às demais validações de entrada. |
| Geometria do tipo `MultiPolygon` | Prosseguir às demais validações de entrada. |
| Geometria do tipo `Point`, `MultiPoint`, `LineString` ou `MultiLineString` | Rejeitar o arquivo e informar que os tipos aceitos são `Polygon` e `MultiPolygon`. |
| Geometria do tipo `GeometryCollection`, mesmo contendo somente polígonos | Rejeitar o arquivo e informar que os tipos aceitos são `Polygon` e `MultiPolygon`. |

**Dependências e detalhamento pendente:**

O formato inicial, a estrutura e os tipos de geometria estão definidos como
GeoJSON com extensão `.geojson`, objeto principal `FeatureCollection` e
geometrias `Polygon` ou `MultiPolygon`, conforme as condições acima. Os
limites de entrada, as regras adicionais de validade das geometrias, incluindo
coordenadas e topologia, e o tratamento de arquivos com múltiplas áreas ou
mais de uma `Feature` ainda deverão ser especificados e aprovados antes da
implementação e da preparação dos arquivos de teste válidos e inválidos.
A definição dos tipos de geometria não resolve essas pendências.

**Momento de verificação:**

Os critérios serão testados durante a implementação da funcionalidade. Este
registro especifica o comportamento esperado; a funcionalidade ainda não foi
implementada e os testes funcionais ainda não foram executados.

### RF-02 — Leitura do arquivo e identificação da área

**Estado:** definição aprovada pelo responsável pelo projeto em 20/10/2026;
regras para arquivos com múltiplas áreas ainda pendentes.

**Ator:** AT-01 — Engenheiro/analista.

**Origem:** identificação da área informada prevista no RNG-05.

**Prioridade:** essencial para o fluxo principal do MVP.

**Descrição aprovada:**

O sistema deverá ler o arquivo geográfico aprovado pela validação do RF-01,
identificar a geometria da área de estudo e disponibilizá-la às análises
seguintes. Falhas de leitura ou a impossibilidade de identificar a área
deverão ser informadas com mensagem compreensível e impedir o prosseguimento
para as análises seguintes.

**Critérios de aceitação:**

| Cenário | Resultado esperado |
| --- | --- |
| Leitura bem-sucedida e área identificada conforme as regras de entrada | Disponibilizar a geometria da área às análises seguintes. |
| Falha de leitura do arquivo | Apresentar mensagem compreensível e impedir o prosseguimento para as análises seguintes. |
| Impossibilidade de identificar a área no arquivo | Apresentar mensagem compreensível e impedir o prosseguimento para as análises seguintes. |

**Dependências e detalhamento pendente:**

O requisito depende do RF-01 e da definição das regras para arquivos com
múltiplas áreas. Essas regras deverão ser especificadas e aprovadas antes da
implementação e da preparação dos cenários de teste correspondentes.
As pendências técnicas do RF-01 permanecem em aberto.

**Momento de verificação:**

Os critérios serão testados durante a implementação da funcionalidade. Este
registro especifica o comportamento esperado; a funcionalidade ainda não foi
implementada e os testes funcionais ainda não foram executados.

### RF-03 — Cálculo da extensão do terreno

**Estado:** definição aprovada pelo responsável pelo projeto em 20/10/2026;
sistema de coordenadas adequado, precisão e tolerância de comparação ainda
pendentes de definição.

**Ator:** AT-01 — Engenheiro/analista.

**Origem:** análise das características da área prevista no RNG-05.

**Prioridade:** essencial para o fluxo principal do MVP.

**Descrição aprovada:**

O sistema deverá calcular a área da geometria identificada pelo RF-02 e
apresentar o resultado em metros quadrados (m²) e hectares (ha), utilizando
um sistema de coordenadas adequado ao cálculo. Quando não for possível
calcular a área, deverá apresentar uma mensagem compreensível sobre o problema.

**Critérios de aceitação:**

| Cenário | Resultado esperado |
| --- | --- |
| Cálculo realizado com sucesso | Apresentar o valor da área em m² e hectares, com as unidades identificadas. |
| Conferência com uma área de referência | O resultado deverá corresponder ao valor de referência dentro da precisão e da tolerância de comparação especificadas. |
| Impossibilidade de calcular a área | Apresentar mensagem compreensível sobre o problema. |

**Dependências e detalhamento pendente:**

O requisito depende da geometria disponibilizada pelo RF-02. O sistema de
coordenadas adequado, a precisão e a tolerância de comparação deverão ser
especificados e aprovados antes da implementação e da preparação dos testes
com área de referência. As pendências dos RF-01 e RF-02 permanecem em aberto.

**Momento de verificação:**

Os critérios serão testados durante a implementação da funcionalidade. Este
registro especifica o comportamento esperado; a funcionalidade ainda não foi
implementada e os testes de cálculo ainda não foram executados.

### RF-04 — Cruzamento com as bases geográficas

**Estado:** definição aprovada pelo responsável pelo projeto em 20/10/2026;
bases e operações específicas ainda pendentes de detalhamento.

**Ator:** AT-01 — Engenheiro/analista.

**Origem:** análise geográfica com camadas públicas prevista no RNG-05.

**Prioridade:** essencial para o fluxo principal do MVP.

**Descrição aprovada:**

O sistema deverá cruzar a geometria da área identificada pelo RF-02 com as
camadas geográficas públicas preparadas, identificando as fontes utilizadas.
Falhas no cruzamento ou indisponibilidade de dados deverão ser informadas
com mensagem compreensível.

**Critérios de aceitação:**

| Cenário | Resultado esperado |
| --- | --- |
| Cruzamento em um cenário de referência | O resultado deverá corresponder ao esperado para as bases e operações especificadas no cenário. |
| Consulta das informações utilizadas no cruzamento | Identificar as camadas e suas fontes. |
| Falha na execução do cruzamento | Informar o problema com mensagem compreensível. |
| Dados necessários indisponíveis | Informar a indisponibilidade com mensagem compreensível. |

**Dependências e detalhamento pendente:**

O requisito depende da geometria disponibilizada pelo RF-02, das camadas
geográficas preparadas e de sistemas de coordenadas compatíveis. As bases e
as operações específicas deverão ser detalhadas e aprovadas antes da
implementação e da preparação do cenário de referência. As pendências dos
requisitos anteriores permanecem em aberto.

**Momento de verificação:**

Os critérios serão testados durante a implementação da funcionalidade. Este
registro especifica o comportamento esperado; a funcionalidade ainda não foi
implementada e os testes de cruzamento ainda não foram executados.

### RF-05 — Identificação de distâncias, sobreposições e alertas

**Estado:** definição aprovada pelo responsável pelo projeto em 20/10/2026;
medições, tolerâncias e condições dos alertas ainda pendentes de definição.

**Ator:** AT-01 — Engenheiro/analista.

**Origem:** identificação de distâncias, sobreposições e alertas prevista no RNG-05.

**Prioridade:** essencial para o fluxo principal do MVP.

**Descrição aprovada:**

O sistema deverá identificar distâncias e sobreposições relevantes a partir
do cruzamento previsto no RF-04 e apresentar os alertas associados, com as
fontes e os parâmetros utilizados. Os resultados deverão apresentar suas
unidades e distinguir a ausência de uma ocorrência da indisponibilidade dos
dados necessários. Falhas deverão ser informadas com mensagem compreensível.

**Critérios de aceitação:**

| Cenário | Resultado esperado |
| --- | --- |
| Conferência de distâncias, sobreposições e alertas em cenários de referência | Os resultados deverão corresponder ao esperado conforme as medições, tolerâncias e condições de alerta especificadas. |
| Consulta das medições e dos alertas obtidos | Apresentar as unidades das medições e identificar as fontes e os parâmetros utilizados. |
| Ausência de uma ocorrência nos dados analisados | Identificar essa ausência como resultado da análise realizada. |
| Dados necessários indisponíveis | Informar a indisponibilidade de forma distinta da ausência de ocorrência. |
| Falha na identificação das distâncias, sobreposições ou alertas | Informar o problema com mensagem compreensível. |

**Dependências e detalhamento pendente:**

O requisito depende do RF-04. As medições, as tolerâncias e as condições de
emissão dos alertas deverão ser especificadas e aprovadas antes da
implementação e da preparação dos cenários de referência. As pendências dos
requisitos anteriores permanecem em aberto.

**Momento de verificação:**

Os critérios serão testados durante a implementação da funcionalidade. Este
registro especifica o comportamento esperado; a funcionalidade ainda não foi
implementada e os testes de medições e alertas ainda não foram executados.

### RF-06 — Aplicação de regras de negócio demonstrativas

**Estado:** definição aprovada pelo responsável pelo projeto em 20/10/2026;
regras de negócio, parâmetros e tratamento de dados ausentes ainda pendentes
de especificação.

**Ator:** AT-01 — Engenheiro/analista.

**Origem:** comparação com restrições eliminatórias prevista no RNG-05 e
identificação de informações demonstrativas prevista no RNG-06.

**Prioridade:** essencial para o fluxo principal do MVP.

**Descrição aprovada:**

O sistema deverá aplicar regras de negócio demonstrativas aos dados da
análise, identificando a regra utilizada e a justificativa de cada resultado.
As restrições eliminatórias deverão permanecer separadas das pontuações;
uma pontuação alta não poderá compensar uma restrição eliminatória.
As regras simuladas deverão ser explicitamente identificadas.

**Critérios de aceitação:**

| Cenário | Resultado esperado |
| --- | --- |
| Cenário de referência com restrição eliminatória | Identificar a restrição conforme a regra especificada e apresentar a justificativa do resultado. |
| Cenário de referência sem restrição eliminatória | Apresentar o resultado esperado conforme a regra especificada e sua justificativa. |
| Restrição eliminatória acompanhada de pontuação alta | Manter a restrição separada da pontuação, sem permitir sua compensação pela nota. |
| Consulta do resultado de uma regra | Identificar a regra utilizada e a justificativa do resultado. |
| Aplicação de regra simulada | Identificar explicitamente seu caráter simulado. |

**Dependências e detalhamento pendente:**

O requisito depende do RF-05 e da especificação das regras de negócio, de
seus parâmetros e do tratamento de dados ausentes. Essas definições deverão
ser aprovadas antes da implementação e da preparação dos cenários de teste.
As pendências dos requisitos anteriores permanecem em aberto.

**Momento de verificação:**

Os critérios serão testados durante a implementação da funcionalidade. Este
registro especifica o comportamento esperado; a funcionalidade ainda não foi
implementada e os testes de aplicação das regras ainda não foram executados.

### RF-07 — Cadastro e seleção de alternativas de uso futuro

**Estado:** definição aprovada pelo responsável pelo projeto em 20/10/2026;
campos e regras de validação do cadastro ainda pendentes de definição.

**Ator:** AT-01 — Engenheiro/analista.

**Origem:** cadastro e comparação de alternativas previstos no RNG-05 e
comparação de pelo menos duas alternativas prevista no RNG-07.

**Prioridade:** essencial para o fluxo principal do MVP.

**Descrição aprovada:**

O sistema deverá permitir cadastrar alternativas de uso futuro e selecionar
quais serão comparadas para a área em análise. As alternativas cadastradas e
as selecionadas deverão ser identificáveis. Para iniciar a comparação,
deverão estar selecionadas pelo menos duas alternativas distintas. Dados de
cadastro inválidos deverão ser informados com mensagem compreensível.

**Critérios de aceitação:**

| Cenário | Resultado esperado |
| --- | --- |
| Cadastro com dados válidos conforme as regras especificadas | Permitir cadastrar e identificar a alternativa. |
| Seleção de alternativas cadastradas | Permitir conferir quais alternativas foram selecionadas para a comparação da área em análise. |
| Seleção de pelo menos duas alternativas distintas | Atender ao mínimo de alternativas necessário para iniciar a comparação. |
| Seleção de menos de duas alternativas distintas | Impedir o início da comparação e informar a necessidade de selecionar pelo menos duas alternativas distintas. |
| Dados de cadastro inválidos | Informar o problema com mensagem compreensível. |

**Dependências e detalhamento pendente:**

O requisito depende da área identificada pelo RF-02 e da definição dos campos
e das regras de validação do cadastro. Essas definições deverão ser
especificadas e aprovadas antes da implementação e da preparação dos cenários
de teste. As pendências dos requisitos anteriores permanecem em aberto.

**Momento de verificação:**

Os critérios serão testados durante a implementação da funcionalidade. Este
registro especifica o comportamento esperado; a funcionalidade ainda não foi
implementada e os testes de cadastro e seleção ainda não foram executados.

### RF-08 — Definição de critérios, notas e pesos

**Estado:** definição aprovada pelo responsável pelo projeto em 20/10/2026;
escalas, limites, validação dos pesos e tratamento de valores ausentes ainda
pendentes de definição.

**Ator:** AT-01 — Engenheiro/analista.

**Origem:** comparação por critérios, notas e pesos prevista no RNG-05 e
comparação explicável prevista no RNG-07.

**Prioridade:** essencial para o fluxo principal do MVP.

**Descrição aprovada:**

O sistema deverá permitir definir os critérios da comparação, atribuir notas
às alternativas e configurar os pesos dos critérios. Os critérios, as notas
e os pesos configurados deverão poder ser consultados. Cada nota deverá estar
associada à alternativa e ao critério correspondentes. Valores inválidos
deverão ser rejeitados com mensagem compreensível.

**Critérios de aceitação:**

| Cenário | Resultado esperado |
| --- | --- |
| Configuração com valores válidos conforme as regras especificadas | Permitir definir critérios, atribuir notas às alternativas e configurar os pesos dos critérios. |
| Consulta da configuração da comparação | Apresentar os critérios, as notas e os pesos configurados. |
| Consulta de uma nota atribuída | Identificar a alternativa e o critério correspondentes. |
| Informação de valores inválidos | Rejeitar os valores e informar o problema com mensagem compreensível. |

**Dependências e detalhamento pendente:**

O requisito depende das alternativas do RF-07 e da definição das escalas, dos
limites, da validação dos pesos e do tratamento de valores ausentes. Essas
definições deverão ser especificadas e aprovadas antes da implementação e da
preparação dos cenários de teste. As pendências dos requisitos anteriores
permanecem em aberto.

**Momento de verificação:**

Os critérios serão testados durante a implementação da funcionalidade. Este
registro especifica o comportamento esperado; a funcionalidade ainda não foi
implementada e os testes de configuração de critérios, notas e pesos ainda
não foram executados.

### RF-09 — Cálculo multicritério por soma ponderada

**Estado:** definição aprovada pelo responsável pelo projeto em 20/10/2026;
regras de normalização, precisão, empates e valores ausentes ainda pendentes
de definição.

**Ator:** AT-01 — Engenheiro/analista.

**Origem:** comparação por critérios, notas e pesos prevista no RNG-05 e
comparação explicável com restrições separadas prevista no RNG-07.

**Prioridade:** essencial para o fluxo principal do MVP.

**Descrição aprovada:**

O sistema deverá calcular a pontuação das alternativas somando as notas
multiplicadas pelos respectivos pesos e apresentar sua classificação.
As notas e os pesos utilizados deverão ser identificáveis. As restrições
eliminatórias deverão permanecer separadas da pontuação, sem permitir sua
compensação por uma nota alta. Entradas inconsistentes deverão ser informadas
com mensagem compreensível.

**Critérios de aceitação:**

| Cenário | Resultado esperado |
| --- | --- |
| Cálculo com entradas válidas | Calcular as pontuações por soma ponderada e apresentar a classificação das alternativas. |
| Conferência com um cálculo de referência | As pontuações e a classificação deverão corresponder ao esperado conforme as regras e a precisão especificadas. |
| Consulta das entradas utilizadas no cálculo | Identificar as notas e os respectivos pesos utilizados. |
| Alternativa com restrição eliminatória e pontuação alta | Manter a restrição separada da pontuação, sem permitir sua compensação pela nota. |
| Entradas inconsistentes | Informar o problema com mensagem compreensível. |

**Dependências e detalhamento pendente:**

O requisito depende das regras do RF-06, das alternativas do RF-07 e dos
critérios, notas e pesos do RF-08. As regras de normalização, precisão,
empates e valores ausentes deverão ser definidas e aprovadas antes da
implementação e da preparação dos cenários de teste com cálculo de referência.
As pendências dos requisitos anteriores permanecem em aberto.

**Momento de verificação:**

Os critérios serão testados durante a implementação da funcionalidade. Este
registro especifica o comportamento esperado; a funcionalidade ainda não foi
implementada e os testes de cálculo multicritério ainda não foram executados.

### RF-10 — Apresentação dos resultados no dashboard

**Estado:** definição aprovada pelo responsável pelo projeto em 20/10/2026;
detalhamento da apresentação ainda pendente.

**Atores:** AT-01 — Engenheiro/analista e AT-02 — Gestor.

**Origem:** dashboard previsto no RNG-05 e comunicação compreensível dos
resultados prevista no RNG-07.

**Prioridade:** essencial para o fluxo principal do MVP.

**Descrição aprovada:**

O sistema deverá apresentar no dashboard o mapa, as características da área,
os alertas, as restrições e a classificação das alternativas, com fontes,
parâmetros e limitações. A apresentação deverá distinguir informações reais,
simuladas e indisponíveis e permitir compreender os fatores da classificação.
As previsões de Machine Learning serão incorporadas na Etapa 8 e estarão
presentes no dashboard do MVP final.

**Critérios de aceitação:**

| Cenário | Resultado esperado |
| --- | --- |
| Consulta dos resultados de uma análise | Apresentar mapa, características da área, alertas, restrições e classificação consistentes com os resultados da análise. |
| Consulta das informações que fundamentam os resultados | Permitir consultar fontes, parâmetros e limitações. |
| Exibição de informações reais, simuladas ou indisponíveis | Distinguir claramente essas situações na apresentação. |
| Compreensão da classificação pelo responsável pelo projeto | Permitir identificar as alternativas avaliadas e os fatores da classificação. |
| Dashboard do MVP final após a integração da Etapa 8 | Apresentar as previsões de ML consistentes com os resultados do modelo integrado. |

**Dependências e detalhamento pendente:**

O requisito depende dos resultados dos requisitos anteriores e do detalhamento
da apresentação, que deverá ser aprovado antes da implementação e da
preparação dos cenários de teste correspondentes. A apresentação das previsões
depende da integração de ML prevista na Etapa 8, incluída na entrega final do
MVP. As pendências dos requisitos anteriores permanecem em aberto.

**Momento de verificação:**

Os critérios serão testados durante a implementação da funcionalidade e,
para as previsões, após a integração do ML. Este registro especifica o
comportamento esperado; o dashboard ainda não foi implementado e seus testes
ainda não foram executados.

### RF-11 — Persistência e consulta das análises

**Estado:** definição aprovada pelo responsável pelo projeto em 20/10/2026;
modelo e regras de armazenamento ainda pendentes de definição na Etapa 5.

**Atores:** AT-01 — Engenheiro/analista salva e consulta; AT-02 — Gestor consulta.

**Origem:** persistência prevista no RNG-05 e recuperação de parâmetros e
resultados prevista no RNG-07.

**Prioridade:** essencial para o fluxo principal do MVP.

**Descrição aprovada:**

O sistema deverá permitir salvar análises com seus parâmetros e resultados,
identificar as análises salvas e recuperá-las posteriormente. A recuperação
em uma nova sessão deverá preservar os parâmetros e os resultados salvos.
Falhas de gravação ou leitura e análises não encontradas deverão ser
informadas com mensagem compreensível.

**Critérios de aceitação:**

| Cenário | Resultado esperado |
| --- | --- |
| Salvamento bem-sucedido de uma análise | Permitir identificar a análise salva com seus parâmetros e resultados. |
| Recuperação da análise em uma nova sessão | Recuperar os parâmetros e resultados preservados conforme o conteúdo salvo. |
| Falha de gravação | Informar o problema com mensagem compreensível. |
| Falha de leitura | Informar o problema com mensagem compreensível. |
| Análise solicitada não encontrada | Informar que a análise não foi encontrada com mensagem compreensível. |

**Dependências e detalhamento pendente:**

O requisito depende dos dados e resultados da análise e da definição do modelo
e das regras de armazenamento, a detalhar na Etapa 5. Essas definições deverão
ser aprovadas antes da implementação e da preparação dos cenários de teste.
As pendências dos requisitos anteriores permanecem em aberto.

**Momento de verificação:**

Os critérios serão testados durante a implementação da funcionalidade. Este
registro especifica o comportamento esperado; a persistência e a consulta
ainda não foram implementadas e seus testes ainda não foram executados.

### RF-12 — Exportação de relatório

**Estado:** definição aprovada pelo responsável pelo projeto em 20/10/2026;
formato e estrutura do relatório ainda pendentes de definição.

**Atores:** AT-01 — Engenheiro/analista exporta; AT-02 — Gestor consulta o relatório.

**Origem:** exportação de relatório prevista no RNG-05 e fluxo completo e
rastreabilidade previstos no RNG-07.

**Prioridade:** essencial para o fluxo principal do MVP.

**Descrição aprovada:**

O sistema deverá permitir exportar os resultados da análise em um relatório
com identificação da área, alternativas, classificação, restrições, fontes,
parâmetros e limitações. Informações simuladas deverão ser identificadas.
Falhas de geração deverão ser informadas com mensagem compreensível.
As previsões de Machine Learning integrarão o relatório do MVP final.

**Critérios de aceitação:**

| Cenário | Resultado esperado |
| --- | --- |
| Exportação bem-sucedida | Gerar um arquivo que possa ser aberto para consulta. |
| Conferência do relatório com a análise | Apresentar identificação da área, alternativas, classificação, restrições, fontes, parâmetros e limitações correspondentes à análise. |
| Relatório com informações simuladas | Identificar explicitamente essas informações. |
| Falha na geração do relatório | Informar o problema com mensagem compreensível. |
| Relatório do MVP final após a integração da Etapa 8 | Incluir as previsões de ML correspondentes à análise. |

**Dependências e detalhamento pendente:**

O requisito depende dos dados e resultados da análise e da definição do formato
e da estrutura do relatório. Essas definições deverão ser aprovadas antes da
implementação e da preparação dos cenários de teste correspondentes. A inclusão
das previsões depende da integração de ML prevista na Etapa 8, incluída na
entrega final do MVP. As pendências dos requisitos anteriores permanecem em
aberto.

**Momento de verificação:**

Os critérios serão testados durante a implementação da funcionalidade e,
para as previsões, após a integração do ML. Este registro especifica o
comportamento esperado; a exportação ainda não foi implementada e seus testes
ainda não foram executados.

### RF-13 — Previsão demonstrativa de aptidão física por ML

**Estado:** definição aprovada pelo responsável pelo projeto em 20/10/2026;
alvo, atributos, treinamento, avaliação e conversão da previsão em entrada
multicritério ainda pendentes de definição.

**Atores:** AT-01 — Engenheiro/analista utiliza a previsão; AT-02 — Gestor consulta os resultados.

**Origem:** ML demonstrativo previsto no RNG-05, limitações do modelo no RNG-06
e integração com testes reproduzíveis no RNG-07.

**Prioridade:** essencial para o MVP final.

**Descrição aprovada:**

O sistema deverá receber atributos da análise geográfica, produzir uma previsão
demonstrativa de aptidão física e utilizá-la como uma das entradas da comparação
multicritério do RF-09. A previsão deverá integrar o dashboard do RF-10 e o
relatório do RF-12, com entradas, origem do treinamento e limitações identificadas.
Entradas inválidas deverão ser informadas com mensagem compreensível. As
restrições eliminatórias deverão permanecer preservadas, sem serem substituídas
ou compensadas pela previsão.

Quando houver treinamento com dados sintéticos, o resultado demonstrará o
funcionamento do algoritmo, sem comprovar capacidade preditiva em áreas reais.

**Critérios de aceitação:**

| Cenário | Resultado esperado |
| --- | --- |
| Previsão com atributos válidos conforme as regras especificadas | Produzir a previsão e permitir identificar os atributos utilizados e o resultado obtido. |
| Integração da previsão ao MVP final | Utilizar a previsão como entrada da comparação e apresentá-la no dashboard e no relatório. |
| Consulta da origem e das limitações do modelo | Disponibilizar a origem dos dados de treinamento e as limitações, identificando treinamento sintético quando utilizado. |
| Reprodução dos testes do modelo | Permitir reproduzir os testes conforme os dados, procedimentos e critérios de avaliação documentados. |
| Entradas inválidas | Informar o problema com mensagem compreensível. |
| Previsão favorável acompanhada de restrição eliminatória | Preservar a restrição, sem permitir sua substituição ou compensação pela previsão. |

**Dependências e detalhamento pendente:**

O requisito depende dos atributos provenientes da análise geográfica e da
definição do alvo, dos atributos, do treinamento, da avaliação e da conversão
da previsão em entrada multicritério. Essas definições deverão ser aprovadas
antes da implementação e da preparação dos testes correspondentes. As
pendências dos requisitos anteriores permanecem em aberto.

**Momento de implementação e verificação:**

O requisito é especificado na Etapa 2. Sua implementação, integração e testes
permanecem previstos na Etapa 8, após o fluxo principal, e fazem parte da
entrega final do MVP. O modelo ainda não foi implementado; treinamento,
avaliação e testes ainda não foram executados.

### RNF-01 — Clareza da interface e das mensagens

**Estado:** definição aprovada pelo responsável pelo projeto em 20/10/2026.

**Origem:** compreensão e rastreabilidade previstas no RNG-02 e comunicação
compreensível prevista no RNG-07.

**Prioridade:** essencial.

**Descrição aprovada:**

A interface e suas mensagens deverão apresentar textos em português, campos
identificáveis e orientações compreensíveis. A apresentação deverá permitir
identificar a ação esperada e compreender os resultados. Em situações de erro,
a mensagem deverá permitir entender o problema e a orientação de correção,
quando aplicável.

**Critérios de aceitação:**

| Cenário | Resultado esperado |
| --- | --- |
| Uso da interface em um cenário válido | Os textos e campos deverão permitir ao responsável pelo projeto identificar a ação esperada, com apresentação em português. |
| Consulta dos resultados | O responsável pelo projeto deverá conseguir compreender os resultados apresentados. |
| Situação de erro prevista no fluxo | A mensagem deverá permitir ao responsável pelo projeto entender o problema e a orientação de correção, quando aplicável. |

**Forma de verificação e detalhamento:**

A verificação utilizará um checklist em cenários válidos e de erro, registrando
os pontos observados pelo responsável pelo projeto. Os fluxos e a interface
serão detalhados nas etapas correspondentes; os cenários do checklist deverão
ser definidos e aprovados antes da verificação.

**Momento de verificação:**

O checklist será aplicado quando a interface e os fluxos correspondentes
estiverem implementados. Este registro especifica a qualidade esperada; a
interface ainda não foi implementada e a verificação de usabilidade ainda
não foi executada.

### RNF-02 — Rastreabilidade da análise

**Estado:** definição aprovada pelo responsável pelo projeto em 20/10/2026;
metadados e seu armazenamento ainda pendentes de definição.

**Origem:** rastreabilidade prevista no RNG-02, limitações dos dados no RNG-06
e evidências de rastreabilidade previstas no RNG-07.

**Prioridade:** essencial.

**Descrição aprovada:**

Cada análise deverá permitir identificar as fontes, as datas, as versões
disponíveis, os parâmetros e as limitações associados aos seus resultados,
incluindo a identificação de informações simuladas. Essas informações deverão
manter correspondência entre a análise, sua consulta e o relatório exportado.

**Critérios de aceitação:**

| Cenário | Resultado esperado |
| --- | --- |
| Conferência de uma análise de referência | Permitir identificar as fontes, datas, versões disponíveis, parâmetros e limitações correspondentes aos resultados da análise. |
| Análise de referência com informações simuladas | Permitir identificar quais informações são simuladas. |
| Consulta da análise e conferência do relatório exportado | Manter a correspondência das informações de rastreabilidade com a análise de referência. |

**Forma de verificação e detalhamento:**

A verificação utilizará uma análise de referência para conferir as informações
de rastreabilidade e sua correspondência na consulta e no relatório. Os
metadados e seu armazenamento serão definidos e aprovados nas etapas
correspondentes, antes da implementação e da preparação do cenário de teste.
As pendências dos requisitos anteriores permanecem em aberto.

**Momento de verificação:**

A verificação ocorrerá após a implementação das funcionalidades correspondentes.
Este registro especifica a qualidade esperada; a rastreabilidade ainda não foi
implementada e sua verificação funcional ainda não foi executada.

### RNF-03 — Execução e testes reproduzíveis

**Estado:** definição aprovada pelo responsável pelo projeto em 20/10/2026;
stack, versões, conjuntos de referência e condições de reprodução ainda
pendentes de definição.

**Origem:** execução reproduzível e testes previstos no RNG-07, incluindo os
testes do ML integrado.

**Prioridade:** essencial.

**Descrição aprovada:**

O GeoVale deverá permitir instalação, execução e verificação seguindo a
documentação do projeto. As versões, os dados e os parâmetros necessários
deverão ser identificados. A repetição de um cenário de referência deverá
produzir resultados compatíveis com as tolerâncias definidas, incluindo as
condições de reprodução do ML. Os resultados reais dos testes deverão ser
registrados.

**Critérios de aceitação:**

| Cenário | Resultado esperado |
| --- | --- |
| Instalação e execução em ambiente limpo | Conseguir instalar e executar o GeoVale seguindo a documentação. |
| Consulta das condições necessárias à execução e aos testes | Identificar as versões, os dados e os parâmetros necessários. |
| Repetição de um cenário de referência nas condições documentadas | Obter resultados compatíveis com as tolerâncias definidas, incluindo o ML quando integrado. |
| Execução dos testes previstos | Registrar os resultados reais observados. |

**Forma de verificação e detalhamento:**

A verificação utilizará um ambiente limpo e cenários de referência, seguindo
os procedimentos documentados. A stack, as versões, os conjuntos de referência,
as tolerâncias e as condições de reprodução, incluindo o ML, deverão ser
definidos e aprovados nas etapas correspondentes antes da execução dessas
verificações. As pendências dos requisitos anteriores permanecem em aberto.

**Momento de verificação:**

As verificações ocorrerão nas etapas de implementação e validação, com a
execução em ambiente limpo também conferida na preparação da entrega. Este
registro especifica a qualidade esperada; ainda não existe aplicação executável
e essas verificações da aplicação ainda não foram realizadas.

### RNF-04 — Tratamento de falhas

**Estado:** definição aprovada pelo responsável pelo projeto em 20/10/2026;
detalhes de recuperação e registro ainda pendentes de definição.

**Origem:** falhas de entrada, persistência e exportação previstas nos RF-01,
RF-11 e RF-12 e clareza das mensagens prevista no RNF-01.

**Prioridade:** essencial.

**Descrição aprovada:**

O GeoVale deverá tratar erros de arquivos, entradas e processamento de forma
controlada, informando o problema. Operações com falha não deverão ser
apresentadas como concluídas. As análises já salvas deverão ser preservadas,
e uma nova tentativa deverá ser possível após a correção da causa da falha.
As mensagens e os registros deverão evitar a exposição de informações sensíveis.

**Critérios de aceitação:**

| Cenário | Resultado esperado |
| --- | --- |
| Erro de arquivo, entrada ou processamento previsto para uma funcionalidade | Informar o problema de forma controlada. |
| Falha durante uma operação | Não apresentar a operação com falha como concluída. |
| Falha com análises previamente salvas | Preservar as análises já salvas. |
| Nova tentativa após a correção da causa da falha | Permitir executar novamente a operação. |
| Consulta das mensagens e dos registros produzidos por uma falha | Evitar a exposição de informações sensíveis. |

**Forma de verificação e detalhamento:**

A verificação utilizará cenários de erro definidos para cada funcionalidade,
conferindo as mensagens, o estado da operação, as análises previamente salvas
e a nova tentativa após a correção da causa. Os detalhes de recuperação e
registro deverão ser definidos e aprovados antes da implementação e da
preparação dos cenários correspondentes. As pendências dos requisitos
anteriores permanecem em aberto.

**Momento de verificação:**

Os cenários de falha serão testados após a implementação das funcionalidades
correspondentes. Este registro especifica a qualidade esperada; o tratamento
de falhas da aplicação ainda não foi implementado e suas verificações ainda
não foram executadas.

### RNF-05 — Desempenho no cenário demonstrativo

**Estado:** definição aprovada pelo responsável pelo projeto em 20/10/2026;
ambiente, dados demonstrativos, operações avaliadas e limites de tempo ainda
pendentes de definição.

**Origem:** cenário de demonstração e fluxo completo previstos no RNG-07 e
verificação de desempenho básico prevista na Etapa 9 do roadmap.

**Prioridade:** importante para a demonstração.

**Descrição aprovada:**

O GeoVale deverá executar o cenário de demonstração dentro de limites de tempo
previamente aprovados. Os tempos das operações e do fluxo completo deverão
ser medidos, com registro do ambiente de execução, do volume dos dados e dos
resultados observados, permitindo comparar as medições com os limites definidos.

**Critérios de aceitação:**

| Cenário | Resultado esperado |
| --- | --- |
| Execução das operações avaliadas no cenário demonstrativo | Medir e registrar os tempos observados das operações. |
| Execução do fluxo completo da demonstração | Medir e registrar o tempo observado do fluxo completo. |
| Consulta das condições das medições | Identificar o ambiente de execução e o volume dos dados utilizados. |
| Comparação das medições com os limites aprovados | Verificar o atendimento aos limites de tempo e registrar os resultados reais observados. |

**Forma de verificação e detalhamento:**

As medições utilizarão o ambiente de execução e os dados demonstrativos
especificados. O ambiente, os dados, as operações avaliadas e os limites de
tempo aceitáveis deverão ser definidos e aprovados antes das medições.
As pendências dos requisitos anteriores permanecem em aberto.

**Momento de verificação:**

As medições ocorrerão após a implementação das funcionalidades correspondentes.
Este registro especifica a qualidade esperada; ainda não existe aplicação
executável e os tempos de processamento da aplicação ainda não foram medidos.

### RNF-06 — Organização e manutenção do código

**Estado:** definição aprovada pelo responsável pelo projeto em 20/10/2026;
arquitetura e convenções específicas ainda pendentes de definição na Etapa 4.

**Origem:** necessidade de compreensão e manutenção do projeto e separação de
responsabilidades prevista na Etapa 4 do planejamento.

**Prioridade:** essencial.

**Descrição aprovada:**

O código do GeoVale deverá organizar as responsabilidades de interface, regras
de negócio, processamento geográfico, Machine Learning e persistência em
componentes identificáveis. Deverá utilizar nomes descritivos, docstrings em
português em todas as funções e classes e comentários relevantes em português
para explicar regras e decisões técnicas, favorecendo a compreensão e a
manutenção pelo responsável pelo projeto.

**Critérios de aceitação:**

| Cenário | Resultado esperado |
| --- | --- |
| Revisão da organização de uma funcionalidade implementada | Identificar os componentes responsáveis pela interface, regras de negócio, processamento geográfico, ML e persistência envolvidos, conforme a arquitetura aprovada. |
| Revisão dos nomes no código desenvolvido | Identificar a finalidade dos componentes, funções, classes e variáveis por nomes descritivos. |
| Revisão da documentação do código desenvolvido | Encontrar docstrings em português em todas as funções e classes e comentários relevantes em português que expliquem as regras e decisões técnicas. |
| Revisão durante a implementação | Registrar os pontos observados na organização e na documentação e corrigir as divergências em relação às definições aprovadas. |

**Forma de verificação e detalhamento:**

A verificação ocorrerá por revisão da estrutura e do código desenvolvido,
conferindo a separação de responsabilidades, os nomes, as docstrings e os
comentários. A arquitetura e as convenções específicas serão definidas e
aprovadas na Etapa 4, antes da implementação correspondente. As pendências
dos requisitos anteriores permanecem em aberto.

**Momento de verificação:**

As revisões ocorrerão durante a implementação dos componentes correspondentes.
Este registro especifica a qualidade esperada; ainda não existe código da
aplicação para verificar o atendimento a este requisito.

### RT-01 — Registro da origem e das condições de uso das bases geográficas

**Estado:** definição aprovada pelo responsável pelo projeto em 20/10/2026;
estrutura de armazenamento e metadados das bases concretas ainda pendentes
de detalhamento nas etapas correspondentes.

**Origem:** rastreabilidade prevista no RNF-02 e registro de fontes, datas,
licenças e limitações previsto na Etapa 6 do planejamento.

**Prioridade:** essencial.

**Descrição aprovada:**

Cada base geográfica utilizada pelo GeoVale deverá possuir um registro que
identifique sua fonte, a data de obtenção, a versão disponível, a licença e
as limitações conhecidas. A fonte e as condições de uso deverão permitir
identificar a referência consultada. Os metadados deverão corresponder à
base efetivamente utilizada. Informações indisponíveis deverão ser indicadas
explicitamente, sem preenchimento com valores presumidos.

**Critérios de aceitação:**

| Cenário | Resultado esperado |
| --- | --- |
| Consulta dos metadados de uma base geográfica de referência | Identificar fonte, data de obtenção, versão disponível, licença e limitações conhecidas da base. |
| Conferência da licença e das condições de uso disponíveis | Identificar a referência consultada e registrar as condições de uso informadas pela fonte. |
| Metadado indisponível na fonte consultada | Indicar explicitamente a informação indisponível, sem apresentar um valor presumido como conhecido. |
| Conferência dos metadados com a base utilizada | Manter a correspondência entre o registro e a base efetivamente utilizada. |

**Dependências e detalhamento pendente:**

O requisito complementa o RNF-02 e depende da seleção e da preparação das
bases geográficas na Etapa 6. A estrutura de armazenamento será definida e
aprovada nas etapas correspondentes, antes da implementação. Os metadados
das bases concretas serão conferidos com suas fontes durante a preparação
dos dados. As pendências dos requisitos anteriores permanecem em aberto.

**Momento de verificação:**

Os registros serão conferidos durante a preparação das bases na Etapa 6 e
sua correspondência com os dados utilizados será verificada na implementação
das funcionalidades correspondentes. Este registro especifica o requisito;
ainda não existem bases preparadas nem armazenamento implementado para
verificar seu atendimento.

### RT-02 — Sistemas de coordenadas e unidades dos cálculos geográficos

**Estado:** definição aprovada pelo responsável pelo projeto em 20/10/2026;
sistemas de coordenadas concretos, procedimentos de compatibilização,
unidades de distância, precisão e tolerâncias ainda pendentes de definição.

**Origem:** adequação do cálculo de área prevista no RF-03, compatibilidade
das camadas prevista no RF-04 e medições com unidades previstas no RF-05.

**Prioridade:** essencial.

**Descrição aprovada:**

O GeoVale deverá identificar os sistemas de coordenadas dos dados utilizados
e empregar referências espaciais e unidades adequadas aos cálculos de área
e distância. Quando necessário, as referências deverão ser compatibilizadas
antes das operações correspondentes. Os resultados deverão permitir identificar
a referência e as unidades utilizadas, com a área apresentada em m² e hectares,
conforme o RF-03. Cálculos cuja referência espacial não possa ser validada
deverão ser impedidos, com mensagem compreensível sobre o problema.

**Critérios de aceitação:**

| Cenário | Resultado esperado |
| --- | --- |
| Consulta das condições de um cálculo geográfico | Identificar o sistema de coordenadas e as unidades utilizados no cálculo. |
| Cálculo com referência espacial validada e adequada | Apresentar a área em m² e hectares e as distâncias nas unidades especificadas, identificando as unidades dos resultados. |
| Dados com referências diferentes que possam ser compatibilizadas | Validar a compatibilização antes de executar as operações correspondentes. |
| Referência ausente ou que não possa ser validada para o cálculo | Impedir os cálculos afetados e informar o problema com mensagem compreensível. |
| Conferência de área e distância em cenários de referência | Obter resultados compatíveis com os valores de referência, dentro da precisão e das tolerâncias especificadas. |

**Dependências e detalhamento pendente:**

O requisito depende da geometria do RF-02 e das camadas geográficas preparadas
para os RF-04 e RF-05. Os sistemas de coordenadas concretos, os procedimentos
de compatibilização, as unidades de distância, a precisão e as tolerâncias
deverão ser definidos e aprovados antes da implementação e da preparação
dos cenários de teste correspondentes, considerando a região e os dados
selecionados. As pendências dos requisitos anteriores permanecem em aberto.

**Momento de verificação:**

As referências dos dados serão conferidas durante sua preparação na Etapa 6.
Os cálculos, as unidades, a compatibilização e os bloqueios serão verificados
na implementação das funcionalidades correspondentes. Este registro especifica
o requisito; ainda não existem bases preparadas nem cálculos implementados
para verificar seu atendimento.

### RN-01 — Restrições eliminatórias na comparação de alternativas

**Estado:** definição e detalhamento da classificação aprovados pelo
responsável pelo projeto em 20/10/2026;
condições e parâmetros das regras demonstrativas ainda pendentes de detalhamento.

**Origem:** separação das restrições prevista nos RNG-05 e RNG-07 e aplicação
nas funcionalidades dos RF-06, RF-09 e RF-13.

**Prioridade:** essencial.

**Descrição aprovada:**

Uma restrição eliminatória identificada para uma alternativa deverá permanecer
separada de sua pontuação multicritério. Pontuações altas e previsões favoráveis
de Machine Learning não poderão compensar, substituir ou remover essa restrição.
A comparação deverá manter identificáveis a regra aplicada e a justificativa
da restrição, inclusive após a integração da previsão ao cálculo multicritério.

Nos cenários com os dados necessários disponíveis, a classificação deverá
conter somente alternativas sem restrição eliminatória identificada. As
alternativas restritas deverão ser apresentadas separadamente, com a regra
e a justificativa, sem posição no ranking. Quando todas as alternativas
estiverem restritas, o resultado deverá informar que nenhuma é elegível
segundo as regras demonstrativas, sem gerar classificação de alternativas
elegíveis.

**Critérios de aceitação:**

| Cenário | Resultado esperado |
| --- | --- |
| Alternativa com restrição eliminatória e pontuação multicritério alta | Preservar a restrição separada da pontuação, sem permitir sua compensação pela nota. |
| Alternativa com restrição eliminatória e previsão favorável de ML utilizada na comparação | Preservar a restrição, sem permitir sua compensação, substituição ou remoção pela previsão. |
| Consulta da restrição na comparação de alternativas | Identificar a regra aplicada e a justificativa da restrição. |
| Cenário com dados necessários disponíveis e alternativas com e sem restrição eliminatória identificada | Classificar somente as alternativas sem restrição identificada e apresentar as restritas separadamente, com regra e justificativa, sem posição no ranking. |
| Cenário com dados necessários disponíveis e todas as alternativas restritas | Informar que nenhuma alternativa é elegível segundo as regras demonstrativas, sem gerar classificação de alternativas elegíveis. |

**Dependências e detalhamento pendente:**

A regra orienta a aplicação das restrições no RF-06, a comparação do RF-09 e
a integração de ML do RF-13. As condições e os parâmetros das regras
demonstrativas deverão ser detalhados e aprovados antes da implementação e
da preparação dos cenários de teste correspondentes. As demais pendências
dos requisitos anteriores permanecem em aberto. O detalhamento da classificação
acima se aplica aos cenários com os dados necessários disponíveis; o tratamento
da indisponibilidade segue o comportamento definido e aprovado na RN-03.
A lista dos dados necessários e os critérios de disponibilidade permanecem
pendentes de detalhamento e aprovação, conforme a RN-03.

**Momento de verificação:**

A preservação das restrições, sua justificativa e os cenários de classificação
com alternativas mistas ou todas restritas serão verificados durante a
implementação dos RF-06 e RF-09. O cenário com previsão favorável será
verificado após a integração do ML na Etapa 8, incluída no MVP final.
Este registro especifica a regra; ainda não existem comparação multicritério
nem modelo implementados para verificar seu atendimento.

### RN-02 — Identificação de informações simuladas

**Estado:** definição aprovada pelo responsável pelo projeto em 20/10/2026;
forma de apresentação ainda pendente de detalhamento nas etapas correspondentes.

**Origem:** identificação das informações simuladas prevista nos RNG-05,
RNG-06 e RNG-07 e rastreabilidade prevista no RNF-02.

**Prioridade:** essencial.

**Descrição aprovada:**

Dados, regras, notas, custos, benefícios e dados de treinamento simulados
utilizados pelo GeoVale deverão ser explicitamente identificados como tais.
Essa identificação deverá manter correspondência entre a análise, o dashboard
e o relatório, permitindo distinguir as informações simuladas das reais.
Quando houver treinamento com dados sintéticos, sua natureza simulada deverá
ser identificável na consulta da origem do treinamento e nos resultados
apresentados no dashboard e no relatório do MVP final.

**Critérios de aceitação:**

| Cenário | Resultado esperado |
| --- | --- |
| Consulta de uma análise com dados, regras, notas, custos ou benefícios simulados | Identificar explicitamente quais dessas informações são simuladas. |
| Consulta do dashboard de uma análise com informações reais e simuladas | Distinguir as informações simuladas das reais, mantendo correspondência com a análise. |
| Conferência do relatório de uma análise com informações simuladas | Preservar a identificação das informações simuladas conforme a análise e o dashboard. |
| Consulta da origem do treinamento e dos resultados após integração de ML treinado com dados sintéticos | Identificar o treinamento sintético na consulta de sua origem e nos resultados apresentados no dashboard e no relatório do MVP final. |

**Dependências e detalhamento pendente:**

A regra orienta a rastreabilidade do RNF-02 e a apresentação prevista nos
RF-10, RF-12 e RF-13. A forma de apresentação deverá ser detalhada e aprovada
nas etapas correspondentes, antes da implementação e da preparação dos
cenários de teste. As pendências dos requisitos anteriores permanecem em
aberto, incluindo a definição dos metadados e de seu armazenamento.

**Momento de verificação:**

A identificação das informações simuladas será verificada durante a
implementação da análise, do dashboard e do relatório. O cenário com
treinamento sintético será verificado após a integração do ML na Etapa 8,
incluída no MVP final. Este registro especifica a regra; ainda não existem
essas funcionalidades implementadas para verificar seu atendimento.

### RN-03 — Distinção entre indisponibilidade de dados e ausência de ocorrência

**Estado:** definição e detalhamento dos efeitos na comparação e no relatório
aprovados pelo responsável pelo projeto em 20/10/2026;
critérios de disponibilidade dos dados e forma de apresentação ainda pendentes
de detalhamento.

**Origem:** distinção prevista no RF-05, apresentação das informações
indisponíveis no RF-10, comparação prevista no RF-09, relatório do RF-12 e
limitações da qualidade dos dados no RNG-06.

**Prioridade:** essencial.

**Descrição aprovada:**

A indisponibilidade dos dados necessários não deverá ser apresentada como
ausência de uma ocorrência. A ausência somente poderá ser indicada como
resultado de uma análise válida realizada com os dados necessários, limitada
aos dados analisados. Quando não for possível avaliar uma ocorrência por
indisponibilidade desses dados, o resultado deverá identificar essa situação.
O dashboard deverá preservar a distinção entre a ausência identificada na
análise e a indisponibilidade dos dados necessários.

Quando faltar um dado necessário para avaliar restrições ou calcular a
comparação, o ranking deverá ser bloqueado e a pendência deverá ser informada.
Os resultados parciais válidos deverão ser preservados, com a indisponibilidade
e o bloqueio do ranking identificados no dashboard e no relatório. Dados
ausentes não deverão ser substituídos automaticamente por zero nem tratados
como ausência de ocorrência. Esse tratamento complementa a classificação
prevista na RN-01.

**Critérios de aceitação:**

| Cenário | Resultado esperado |
| --- | --- |
| Análise válida com os dados necessários disponíveis, sem ocorrência no cenário de referência | Identificar a ausência como resultado limitado aos dados analisados. |
| Dados necessários indisponíveis para avaliar uma ocorrência | Informar a indisponibilidade e não apresentar a ocorrência como ausente. |
| Consulta no dashboard de resultados com ausência identificada e dados indisponíveis | Distinguir as duas situações, mantendo correspondência com os resultados da análise. |
| Falta de dado necessário para avaliar restrições ou calcular a comparação | Bloquear o ranking e informar a pendência correspondente. |
| Consulta do dashboard e do relatório com resultados parciais válidos e ranking bloqueado | Preservar os resultados parciais válidos e identificar a indisponibilidade e o bloqueio do ranking de forma correspondente à análise. |
| Dado numérico necessário ausente | Identificar o dado como ausente, sem substituí-lo automaticamente por zero. |

**Dependências e detalhamento pendente:**

A regra orienta a análise do RF-05, a comparação do RF-09, a apresentação do
RF-10 e o relatório do RF-12, complementando a RN-01. A lista dos dados
necessários para avaliar restrições e calcular a comparação, os critérios de
disponibilidade e a forma de apresentação deverão ser detalhados e aprovados
antes da implementação e da preparação dos cenários de teste correspondentes,
considerando as bases selecionadas e suas limitações.
As demais regras específicas de tratamento de dados ausentes e as pendências
dos requisitos anteriores permanecem em aberto.

**Momento de verificação:**

A distinção, o bloqueio do ranking, a preservação dos resultados parciais e
a ausência de substituição automática por zero serão verificados durante a
implementação da análise, da comparação, do dashboard e do relatório, com
cenários de dados disponíveis sem ocorrência e de dados necessários
indisponíveis. Este registro especifica a regra; essas funcionalidades ainda
não foram implementadas e os cenários ainda não foram testados.
