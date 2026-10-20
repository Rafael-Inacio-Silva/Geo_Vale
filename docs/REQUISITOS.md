# Requisitos do GeoVale

Este documento está em elaboração incremental na Etapa 1 — Engenharia de
requisitos de negócio. As definições registradas abaixo foram validadas; os demais
requisitos serão discutidos e registrados em entregas posteriores.

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
