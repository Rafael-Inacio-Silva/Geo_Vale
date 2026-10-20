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

**Estado:** definição aprovada pelo responsável pelo projeto em 20/10/2026;
detalhamento técnico das validações pendente.

**Ator:** AT-01 — Engenheiro/analista.

**Origem:** capacidade de envio e validação definida no RNG-05.

**Prioridade:** essencial para o fluxo principal do MVP.

**Descrição aprovada:**

O sistema deverá permitir que o engenheiro/analista envie o arquivo geográfico
da área de estudo e verificar sua adequação antes de iniciar a análise.
Um arquivo válido permitirá prosseguir; arquivos vazios, corrompidos ou
incompatíveis deverão ser rejeitados com mensagem compreensível. Falhas de
validação deverão impedir o processamento da análise.

**Critérios de aceitação:**

| Cenário | Resultado esperado |
| --- | --- |
| Arquivo válido conforme as regras de entrada especificadas | Permitir prosseguir para a análise. |
| Arquivo vazio | Rejeitar o arquivo e informar o problema com mensagem compreensível. |
| Arquivo corrompido | Rejeitar o arquivo e informar o problema com mensagem compreensível. |
| Arquivo incompatível com as regras de entrada especificadas | Rejeitar o arquivo e informar o problema com mensagem compreensível. |
| Falha em uma validação | Impedir o processamento da análise a partir do arquivo rejeitado. |

**Dependências e detalhamento pendente:**

Os formatos aceitos, os limites de entrada e as regras de geometria deverão
ser especificados e aprovados antes da implementação. Esses detalhes ainda
estão pendentes; sua definição permitirá preparar arquivos de teste válidos
e inválidos para os cenários acima.

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
