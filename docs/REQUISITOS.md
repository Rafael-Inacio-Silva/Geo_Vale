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

**Estado:** definição, formato inicial, estrutura, tipos de geometria,
regras de validade das geometrias, limites de entrada e tratamento de
múltiplas partes e registros aprovados pelo responsável pelo projeto
em 20/10/2026.

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
campo `features` deverá ser uma lista com exatamente um objeto `Feature`,
representando a única área de estudo da análise. Essa `Feature` deverá conter
`geometry` como objeto de geometria não nulo e `properties` como objeto de
atributos ou `null`. Essas condições são restrições de entrada do GeoVale;
a RFC admite coleções vazias, várias `Feature` e geometrias nulas, mas essa
entrada do MVP exige um único registro com geometria não nula. A aprovação
estrutural permitirá prosseguir às demais validações, incluindo a conferência
dos tipos, das regras de validade das geometrias e dos limites definidos abaixo.

Os tipos de geometria aceitos para representar a área de estudo serão
`Polygon` e `MultiPolygon`. Um `Polygon` representa uma área contínua; um
`MultiPolygon` reúne partes poligonais em uma única geometria, permitindo
representar partes separadas. Esses tipos representam superfícies adequadas
ao cálculo da extensão do terreno previsto no RF-03.

O engenheiro/analista deverá preparar a área antes do envio. Quando uma mesma
área possuir partes separadas, elas poderão ser representadas por um único
`MultiPolygon` dentro da única `Feature`, respeitando a validade geométrica
e os limites de entrada. Essas partes comporão uma única área para análise
conjunta no RF-02. Para estudos independentes, deverão ser enviados arquivos
separados, em análises distintas.

Arquivos com duas ou mais `Feature` serão rejeitados integralmente, mesmo
quando seus registros representarem partes da mesma mina. A mensagem deverá
explicar a exigência de uma única `Feature` e orientar a preparação da área
antes de um novo envio. O GeoVale não selecionará automaticamente o primeiro
registro nem unirá registros para adequar o arquivo. A quantidade de
`Feature` é uma condição de organização da entrada; não comprova que os
polígonos pertencem à mesma mina.

Geometrias dos tipos `Point`, `MultiPoint`, `LineString`, `MultiLineString`
e `GeometryCollection` serão rejeitadas nessa entrada do MVP. A rejeição de
`GeometryCollection` também se aplica quando seus componentes forem somente
polígonos. A aceitação do tipo não dispensa as verificações de validade
definidas a seguir nem a exigência de exatamente uma `Feature` por arquivo.

A geometria deverá ser não vazia, com `coordinates` presente, não vazio e
com a estrutura de listas correspondente a `Polygon` ou `MultiPolygon`.
Cada posição deverá conter dois ou três valores numéricos finitos: longitude
e latitude, nessa ordem, com altitude opcional. A entrada será interpretada
em WGS 84, em graus, com longitude entre −180° e 180° e latitude entre −90°
e 90°, inclusive. A altitude, quando informada, não participará das
verificações e dos cálculos em duas dimensões; seu valor também deverá ser
numérico e finito. A quantidade de dois ou três valores e os intervalos
aceitos são condições de entrada do MVP, compatíveis com a representação
geográfica da RFC 7946.

Cada anel deverá estar fechado no arquivo recebido, com pelo menos quatro
posições contando o fechamento e pelo menos três vértices distintos. A
última posição deverá repetir os valores da primeira, conforme a
[RFC 7946, seção 3.1.6](https://www.rfc-editor.org/rfc/rfc7946.html#section-3.1.6).
Contornos que cruzem a si mesmos ou se reduzam a uma linha ou ponto serão
rejeitados. Em um `Polygon`, o primeiro anel representará o contorno externo
e os demais, quando presentes, os recortes internos. Recortes serão aceitos
quando corretamente posicionados e quando a geometria completa for válida.

Em um `MultiPolygon`, cada parte e o conjunto deverão ser válidos. Partes
com sobreposição de superfície ou compartilhamento de um trecho de borda
serão rejeitadas. Contatos isolados em pontos poderão ser aceitos somente
quando a geometria completa continuar válida. Essas verificações seguem
as condições de validade geométrica exemplificadas na
[documentação do Shapely](https://shapely.readthedocs.io/en/stable/manual.html#object.is_valid);
a referência não define a biblioteca da implementação, cuja escolha pertence
à etapa de arquitetura. O sentido de percurso dos vértices, isoladamente,
não será motivo de rejeição, conforme a orientação de compatibilidade da
RFC 7946.

Qualquer falha nessas verificações deverá rejeitar o arquivo, bloquear a
análise e apresentar mensagem compreensível sobre o problema identificado.
O sistema não corrigirá automaticamente a geometria recebida. A referência
de entrada em graus não substitui a definição do sistema adequado aos
cálculos de área e distância exigida no RF-03 e no RT-02.

O arquivo de entrada deverá ter no máximo **1 MiB (1.048.576 bytes)** e
**20.000 posições**, atendendo aos dois limites simultaneamente. O tamanho
será medido em bytes do arquivo completo recebido, incluindo seus atributos
e demais conteúdos. A contagem de posições somará todas as geometrias do
arquivo, todas as partes poligonais e todos os anéis externos e internos,
incluindo as posições repetidas para fechamento. Cada conjunto de longitude,
latitude e altitude opcional contará como uma posição; seus valores numéricos
não serão contados separadamente.

Os limites serão inclusivos: um arquivo com exatamente 1.048.576 bytes ou
20.000 posições poderá prosseguir às demais validações, desde que também
respeite o outro limite. Exceder qualquer um deles deverá rejeitar o arquivo
inteiro, bloquear a análise e apresentar mensagem compreensível com o limite
excedido e seu máximo permitido. O sistema não simplificará geometrias nem
removerá posições automaticamente para adequar o arquivo aos limites.
Permanecer dentro dos limites não dispensa nenhuma outra validação.

Esses limites se aplicam ao arquivo da área de estudo enviado pelo
engenheiro/analista. As bases ambientais de referência serão preparadas
separadamente. São limites iniciais de escopo do MVP, definidos após a
comparação exploratória de arquivos reais; não comprovam a capacidade máxima
nem o desempenho do fluxo completo da aplicação. A compatibilidade com a
infraestrutura será avaliada na Etapa 4, e a verificação de desempenho seguirá
o RNF-05.

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
| `Polygon` ou `MultiPolygon` não vazio, com coordenadas e geometria válidas | Prosseguir às demais validações de entrada. |
| Coordenadas ausentes, vazias ou com estrutura incompatível com o tipo de geometria | Rejeitar o arquivo e informar o problema com mensagem compreensível. |
| Posição com valores não numéricos ou não finitos, ou quantidade diferente de dois ou três valores | Rejeitar o arquivo com mensagem compreensível; aceitar longitude e latitude com altitude opcional, que não participa dos cálculos em duas dimensões. |
| Longitude fora de −180° a 180° ou latitude fora de −90° a 90° | Rejeitar o arquivo com mensagem compreensível; interpretar a entrada em WGS 84, em graus. |
| Anel aberto, com menos de quatro posições contando o fechamento ou com menos de três vértices distintos | Rejeitar o arquivo com mensagem compreensível; a última posição deve repetir os valores da primeira. |
| Contorno que cruza a si mesmo ou se reduz a uma linha ou ponto | Rejeitar o arquivo com mensagem compreensível. |
| Polígono com recortes internos | Prosseguir às demais validações quando os recortes estiverem corretamente posicionados e a geometria completa for válida; caso contrário, rejeitar o arquivo com mensagem compreensível. |
| Partes de um `MultiPolygon` com sobreposição de superfície ou compartilhamento de um trecho de borda | Rejeitar o arquivo com mensagem compreensível; contatos isolados em pontos poderão ser aceitos somente quando a geometria completa continuar válida. |
| Somente o sentido de percurso dos vértices está invertido, com as demais condições de validade atendidas | Não rejeitar somente pelo sentido de percurso; prosseguir às demais validações de entrada. |
| Arquivo abaixo de 1.048.576 bytes e de 20.000 posições | Prosseguir às demais validações de entrada. |
| Arquivo com exatamente 1.048.576 bytes e no máximo 20.000 posições | Não rejeitar pelo tamanho; prosseguir às demais validações de entrada. |
| Arquivo com 1.048.577 bytes ou mais | Rejeitar o arquivo inteiro, bloquear a análise e informar o limite de 1 MiB (1.048.576 bytes), sem simplificação automática. |
| Arquivo com exatamente 20.000 posições e no máximo 1.048.576 bytes | Não rejeitar pela contagem; prosseguir às demais validações de entrada, somando todas as partes e anéis, incluindo os fechamentos. |
| Arquivo com 20.001 posições ou mais, somadas todas as partes e anéis, incluindo os fechamentos | Rejeitar o arquivo inteiro, bloquear a análise e informar o limite de 20.000 posições, sem remover posições ou simplificar automaticamente. |
| Arquivo dentro dos dois limites, mas com geometria inválida | Rejeitar o arquivo e bloquear a análise conforme as regras de validade, com mensagem compreensível. |
| Exatamente uma `Feature` com `Polygon` | Prosseguir às demais validações para uma única área de estudo. |
| Exatamente uma `Feature` com `MultiPolygon` contendo várias partes válidas | Prosseguir às demais validações, considerando todas as partes como uma única área de estudo para análise conjunta. |
| Duas ou mais `Feature`, mesmo representando partes da mesma mina | Rejeitar o arquivo inteiro e bloquear a análise, com mensagem que exija uma única `Feature` e oriente a preparação da área antes do envio; não selecionar o primeiro registro nem unir registros automaticamente. |

**Dependências e detalhamento pendente:**

O formato inicial, a estrutura, os tipos de geometria, as regras de validade,
os limites e o tratamento de múltiplas partes e registros estão definidos
conforme as condições acima: GeoJSON com extensão `.geojson`, objeto principal
`FeatureCollection` com exatamente uma `Feature`, geometria `Polygon` ou
`MultiPolygon` válida e arquivo de até 1 MiB (1.048.576 bytes) e 20.000 posições.
Várias partes válidas de um `MultiPolygon` comporão a área única identificada
no RF-02; arquivos com várias `Feature` serão rejeitados. As definições de
cálculo do RF-03 e do RT-02 e a verificação de desempenho do RNF-05 continuam
pendentes. A preparação dos arquivos de teste válidos e inválidos e a
verificação funcional ocorrerão nas etapas correspondentes.

**Momento de verificação:**

Os critérios serão testados durante a implementação da funcionalidade. Este
registro especifica o comportamento esperado; a funcionalidade ainda não foi
implementada e os testes funcionais ainda não foram executados.

### RF-02 — Leitura do arquivo e identificação da área

**Estado:** definição e tratamento de múltiplas partes e registros aprovados
pelo responsável pelo projeto em 20/10/2026.

**Ator:** AT-01 — Engenheiro/analista.

**Origem:** identificação da área informada prevista no RNG-05.

**Prioridade:** essencial para o fluxo principal do MVP.

**Descrição aprovada:**

O sistema deverá ler o arquivo geográfico aprovado pela validação do RF-01,
identificar a geometria da área de estudo e disponibilizá-la às análises
seguintes. Falhas de leitura ou a impossibilidade de identificar a área
deverão ser informadas com mensagem compreensível e impedir o prosseguimento
para as análises seguintes.

A área será identificada pela geometria da única `Feature` admitida no
RF-01. Um `Polygon` representará uma área contínua; um `MultiPolygon` poderá
representar várias partes válidas, que serão disponibilizadas em conjunto
como uma única área de estudo. O sistema deverá preservar todas essas partes,
sem escolher apenas uma nem criar análises independentes automaticamente.
Arquivos com mais de uma `Feature` serão rejeitados pelo RF-01, mesmo quando
representarem a mesma mina; sua seleção ou união automática não fará parte
dessa entrada do MVP. Para analisar áreas independentemente, o engenheiro
preparará arquivos separados para análises distintas.

**Critérios de aceitação:**

| Cenário | Resultado esperado |
| --- | --- |
| Leitura bem-sucedida e área identificada conforme as regras de entrada | Disponibilizar a geometria da área às análises seguintes. |
| Falha de leitura do arquivo | Apresentar mensagem compreensível e impedir o prosseguimento para as análises seguintes. |
| Impossibilidade de identificar a área no arquivo | Apresentar mensagem compreensível e impedir o prosseguimento para as análises seguintes. |
| Arquivo aprovado pelo RF-01 com uma única `Feature` contendo `Polygon` | Identificar e disponibilizar a geometria como a única área de estudo da análise. |
| Arquivo aprovado pelo RF-01 com uma única `Feature` contendo `MultiPolygon` com várias partes | Disponibilizar todas as partes em conjunto como uma única área de estudo, sem descartar partes ou criar análises independentes automaticamente. |

**Dependências e detalhamento pendente:**

O requisito depende da validação do RF-01, incluindo exatamente uma `Feature`,
os tipos aceitos, a validade geométrica e os limites de entrada. O tratamento
de múltiplas partes e registros está definido acima. A preparação dos cenários
de teste e a verificação funcional permanecem futuras; as definições de
cálculo dos RF-03 e RT-02 não são resolvidas por essa identificação da área.

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

**Estado:** definição e cruzamentos iniciais aprovados pelo responsável pelo
projeto em 20/10/2026; fontes definitivas, preparação das bases e demais
detalhamentos técnicos ainda pendentes.

**Ator:** AT-01 — Engenheiro/analista.

**Origem:** análise geográfica com camadas públicas prevista no RNG-05.

**Prioridade:** essencial para o fluxo principal do MVP.

**Descrição aprovada:**

O sistema deverá cruzar a geometria da área identificada pelo RF-02 com as
camadas geográficas públicas preparadas, identificando as fontes utilizadas.
Falhas no cruzamento ou indisponibilidade de dados deverão ser informadas
com mensagem compreensível.

Os cruzamentos iniciais abrangerão três grupos de camadas públicas de
referência, preparados separadamente do arquivo enviado pelo engenheiro:

- Unidades de conservação, incluindo RPPN: identificar os polígonos com
  alguma parte em comum com a área de estudo.
- Rios e trechos de drenagem: identificar as linhas que atravessem ou toquem
  a área de estudo.
- Massas d’água: identificar os polígonos de água com alguma parte em comum
  com a área de estudo.

O cruzamento deverá considerar a geometria completa identificada pelo RF-02,
incluindo todas as partes de um `MultiPolygon` e respeitando os recortes
internos. Deverá identificar os elementos encontrados e suas camadas e fontes.
Para camadas poligonais, deverá distinguir a sobreposição de superfície do
contato somente na borda ou em um ponto. Um contato sem superfície comum não
será apresentado como sobreposição de área. Interseção inclui os contatos,
conforme a [referência técnica do Shapely](https://shapely.readthedocs.io/en/stable/reference/shapely.intersects.html);
essa referência não define a biblioteca de implementação, cuja escolha
pertence à Etapa 4.

A ausência de ocorrência somente poderá ser informada após um cruzamento
válido, limitada à camada e à cobertura efetivamente analisadas. Camada
ausente, inválida ou incompleta deverá gerar indicação compreensível de
indisponibilidade para o cruzamento afetado, sem concluir ausência de
ocorrência. A seleção das fontes e a preparação dos dados deverão permitir
avaliar essa cobertura. O tratamento dos resultados parciais e da falta de
dados necessários à comparação seguirá a RN-03.

Este detalhamento identifica relações espaciais. As medidas de área de
sobreposição e distância serão detalhadas no RF-05, e as regras demonstrativas
de restrição no RF-06. Terreno e declividade continuam no planejamento,
dependendo da preparação de dados adequados; não são resolvidos pelos três
grupos de camadas acima.

**Critérios de aceitação:**

| Cenário | Resultado esperado |
| --- | --- |
| Cruzamento em um cenário de referência | O resultado deverá corresponder ao esperado para as bases e operações especificadas no cenário. |
| Consulta das informações utilizadas no cruzamento | Identificar as camadas e suas fontes. |
| Falha na execução do cruzamento | Informar o problema com mensagem compreensível. |
| Dados necessários indisponíveis | Informar a indisponibilidade com mensagem compreensível. |
| Polígono de unidade de conservação, incluindo RPPN, ou de massa d’água com superfície em comum com a área estudada | Identificar o elemento, sua camada e fonte e a ocorrência de sobreposição de superfície. |
| Polígono de referência com contato somente na borda ou em um ponto da área estudada | Identificar o contato, a camada e a fonte, sem apresentá-lo como sobreposição de área. |
| Rio ou trecho de drenagem que atravesse ou toque a área estudada | Identificar a interseção com a linha, sua camada e fonte. |
| Cruzamento válido sem ocorrência na camada e cobertura analisadas | Informar a ausência de ocorrência limitada àquela camada e cobertura; respeitar os recortes internos da área. |
| Camada necessária ao cruzamento ausente, inválida ou incompleta | Informar a indisponibilidade do cruzamento afetado com mensagem compreensível, sem concluir ausência de ocorrência; seguir a RN-03 quanto aos resultados parciais e à comparação. |
| Ocorrência em outra parte de um `MultiPolygon`, além da primeira | Identificar a ocorrência considerando todas as partes e seus recortes internos, sem analisar somente a primeira parte. |

**Dependências e detalhamento pendente:**

O requisito depende da geometria disponibilizada pelo RF-02, das camadas
geográficas preparadas e de sistemas de coordenadas compatíveis, conforme
o RT-02. Os três grupos de camadas e os cruzamentos iniciais estão definidos
acima. As fontes definitivas, os metadados e as condições de uso do RT-01,
a cobertura e a preparação das bases serão detalhados na Etapa 6. As
medições, as tolerâncias e as condições dos alertas permanecem pendentes no
RF-05; o alcance de consulta necessário às distâncias também deverá ser
definido antes de sua implementação. A lista de dados necessários à
comparação e os critérios de disponibilidade permanecem pendentes na RN-03.
Dados de terreno e declividade, demais operações e cenários de referência
precisam ser detalhados e aprovados nas unidades correspondentes antes da
implementação e da preparação dos testes. As amostras exploratórias não
substituem essa preparação nem comprovam os testes funcionais do GeoVale.

**Momento de verificação:**

Os critérios serão testados durante a implementação da funcionalidade. Este
registro especifica o comportamento esperado; a funcionalidade ainda não foi
implementada e os testes de cruzamento ainda não foram executados.

### RF-05 — Identificação de distâncias, sobreposições e alertas

**Estado:** definição, medidas descritivas iniciais com suas referências e
limitações e condições dos alertas informativos iniciais aprovadas pelo
responsável pelo projeto em 20/10/2026; precisão, tolerâncias, alcance de
consulta e eventuais alertas adicionais ainda pendentes.

**Ator:** AT-01 — Engenheiro/analista.

**Origem:** identificação de distâncias, sobreposições e alertas prevista no RNG-05.

**Prioridade:** essencial para o fluxo principal do MVP.

**Descrição aprovada:**

O sistema deverá identificar distâncias e sobreposições relevantes a partir
do cruzamento previsto no RF-04 e apresentar os alertas associados, com as
fontes e os parâmetros utilizados. Os resultados deverão apresentar suas
unidades e distinguir a ausência de uma ocorrência da indisponibilidade dos
dados necessários. Falhas deverão ser informadas com mensagem compreensível.

As medidas descritivas iniciais deverão abranger as camadas do RF-04:

- Para polígonos de unidades de conservação e massas d’água, apresentar a
  área de interseção em m² e hectares e seu percentual em relação à área
  total estudada, calculado por `100 × área de interseção / área total`.
  Considerar todas as partes da área e descontar seus recortes internos.
  Identificar os elementos, suas camadas e fontes.
- Em um total consolidado por camada poligonal, considerar a união das
  superfícies de interseção, contando uma única vez os trechos cobertos por
  vários polígonos daquela camada. Manter identificáveis as ocorrências
  individuais. Totais de camadas diferentes não serão somados como se fossem
  uma superfície sem repetição. Essa consolidação dos resultados não altera
  a poligonal recebida nem autoriza várias `Feature` no arquivo de entrada.
- Para elementos de referência dos três grupos do RF-04, apresentar a menor
  distância geométrica em metros entre a área completa e cada elemento
  medido. Considerar todas as partes e recortes internos, sem substituir a
  área por seu centro. Contato ou interseção terá distância zero; contato
  somente na borda ou em um ponto terá área comum zero, mantendo identificada
  a relação espacial conforme o RF-04.

Cada medição deverá permitir consultar sua fonte, camada, cobertura analisada,
sistema de coordenadas e unidades, além dos parâmetros utilizados. Os
cálculos dependerão de referência espacial validada e adequada, conforme o
RT-02, e do cálculo da área total previsto no RF-03.

A menor distância descreverá a proximidade entre as geometrias efetivamente
medidas dentro da cobertura identificada; não caracterizará a distribuição
das distâncias no interior do terreno nem comprovará a proximidade de todos
os elementos existentes fora dessa cobertura. Dados ou cobertura insuficientes
não deverão produzir distância conclusiva nem ser substituídos por zero.
Quando uma consulta válida não encontrar elementos, informar essa ausência
limitada à camada e à cobertura, sem atribuir distância numérica a um elemento
ausente. O tratamento dos resultados parciais e dos dados necessários à
comparação seguirá a RN-03.

**Alertas informativos iniciais:**

As mensagens deverão descrever os resultados dos cruzamentos e das medidas
especificados nos RF-04 e RF-05, com as seguintes condições e exemplos de texto:

- Sobreposição de superfície com um polígono de referência: “Foi identificada
  sobreposição com [elemento]. Consulte a área e o percentual calculados.”
- Contato somente na borda ou em um ponto com um polígono de referência:
  “A área toca [elemento], sem superfície em comum.”
- Interseção com rio ou trecho de drenagem: “Foi identificada interseção com
  [elemento de drenagem].”
- Cruzamento válido sem ocorrência: “Nenhuma interseção foi identificada nesta
  camada, dentro da cobertura analisada.”
- Dados insuficientes ou inválidos, ou falha no processamento: “Não foi possível
  concluir a avaliação de [camada]. Motivo: [explicação compreensível].”

Cada mensagem deverá permitir consultar a camada, a fonte e as condições da
análise. As distâncias calculadas serão apresentadas em metros, acompanhadas
da cobertura considerada, conforme as medidas descritivas acima. As mensagens
comunicarão o resultado geométrico ou a impossibilidade de avaliá-lo; não
classificarão por si só risco, aptidão, segurança ou restrição. Tais
interpretações dependerão de regras fundamentadas e aprovadas em unidades
próprias, sem adotar faixas numéricas de alerta nesta definição.

Quando uma avaliação falhar, seus avisos não deverão ocultar resultados
parciais válidos de outras avaliações. A indisponibilidade e eventual bloqueio
do ranking deverão permanecer identificados conforme a RN-03: o bloqueio
ocorrerá quando faltar dado necessário para avaliar restrições ou calcular
a comparação. Uma falha não será apresentada como ausência de ocorrência.

**Fundamentação e alcance da adaptação:**

O estudo de [Servou e colaboradores, 2023, seções 2.2 e 3.1](https://www.mdpi.com/2071-1050/15/19/14388)
utiliza critérios topográficos e de proximidade em células de mapa para
avaliar usos pós-mineração, com pesos atribuídos por especialistas. Essa
referência fundamenta a investigação de terreno e proximidade; a menor
distância da área inteira e o percentual de interseção definidos aqui são
medidas descritivas propostas para o GeoVale, sem reproduzir diretamente
o método ou validar parâmetros para a região de estudo.

A [interseção geométrica](https://shapely.readthedocs.io/en/stable/reference/shapely.intersection.html),
a [distância entre geometrias](https://shapely.readthedocs.io/en/stable/reference/shapely.distance.html)
e a [união geométrica](https://shapely.readthedocs.io/en/stable/reference/shapely.union_all.html)
fundamentam as operações propostas. A medição de área depende das unidades
e da adequação da referência espacial, conforme a [documentação do GeoPandas](https://geopandas.org/en/stable/docs/reference/api/geopandas.GeoSeries.area.html).
Essas referências técnicas não definem a stack, cuja escolha pertence à
Etapa 4. As medidas não atribuem por si só notas de aptidão, pesos, faixas de
segurança ou restrições; essas definições serão tratadas em unidades próprias.

**Critérios de aceitação:**

| Cenário | Resultado esperado |
| --- | --- |
| Conferência de distâncias, sobreposições e alertas em cenários de referência | Os resultados deverão corresponder ao esperado conforme as medições, tolerâncias e condições de alerta especificadas. |
| Consulta das medições e dos alertas obtidos | Apresentar as unidades das medições e identificar as fontes e os parâmetros utilizados. |
| Ausência de uma ocorrência nos dados analisados | Identificar essa ausência como resultado da análise realizada. |
| Dados necessários indisponíveis | Informar a indisponibilidade de forma distinta da ausência de ocorrência. |
| Falha na identificação das distâncias, sobreposições ou alertas | Informar o problema com mensagem compreensível. |
| Cenário didático com área total de 100 ha e interseção de 10 ha | Apresentar 100.000 m², 10 ha e 10% de interseção, identificando elemento, camada e fonte; valores servem de referência para teste futuro, não de resultado medido em mina real. |
| Duas feições da mesma camada cobrem os mesmos 10 ha da área estudada | Apresentar 10 ha no total consolidado da camada, sem duplicar a superfície, mantendo identificáveis as ocorrências individuais. |
| Contato somente na borda ou em um ponto com um polígono de referência | Apresentar área comum e percentual zero e distância zero, mantendo identificado o contato conforme o RF-04. |
| Cálculo de distância para área com várias partes ou recortes internos | Obter a menor distância entre as geometrias completas, considerando todas as partes e respeitando os recortes internos; não substituir a área por seu centro. |
| Dados necessários ou cobertura insuficientes para uma medição | Informar a indisponibilidade ou limitação com mensagem compreensível, sem produzir distância conclusiva ou substituir a falta por zero; seguir a RN-03. |
| Consulta válida sem elementos encontrados na camada e cobertura analisadas | Informar a ausência limitada àquela camada e cobertura, sem atribuir distância numérica a um elemento ausente. |
| Consulta das condições de uma medida descritiva | Identificar fonte, camada, cobertura, sistema de coordenadas, unidades e parâmetros utilizados. |
| Sobreposição de superfície identificada com polígono de referência | Emitir mensagem informativa de sobreposição, identificando o elemento e permitindo consultar área, percentual, camada, fonte e condições da análise. |
| Contato somente na borda ou em um ponto identificado com polígono de referência | Emitir mensagem de contato sem superfície em comum, distinta da mensagem de sobreposição de área. |
| Interseção identificada com rio ou trecho de drenagem | Emitir mensagem informativa de interseção com o elemento de drenagem, permitindo consultar sua camada, fonte e condições da análise. |
| Cruzamento válido sem ocorrência na camada e cobertura analisadas | Emitir mensagem de que nenhuma interseção foi identificada naquela camada e cobertura, sem apresentar conclusão de segurança ou aptidão. |
| Dados insuficientes ou inválidos, ou falha no processamento de uma avaliação | Informar que a avaliação da camada não pôde ser concluída e apresentar o motivo com explicação compreensível; não informar ausência de ocorrência. |
| Falha em uma avaliação acompanhada de resultados parciais válidos de outras avaliações | Preservar os resultados válidos e identificar a indisponibilidade; bloquear o ranking quando faltar dado necessário para avaliar restrições ou calcular a comparação, conforme a RN-03. |

**Dependências e detalhamento pendente:**

O requisito depende dos cruzamentos do RF-04, da área total do RF-03 e das
referências espaciais do RT-02. As medidas descritivas e as condições dos
alertas informativos iniciais estão definidas acima. Fontes definitivas,
cobertura, preparação e metadados das bases continuam pendentes nas etapas
correspondentes. Sistema de coordenadas concreto,
precisão, tolerâncias e alcance de consulta para distâncias deverão ser
detalhados e aprovados antes da implementação e da preparação dos cenários
de referência. Eventuais alertas adicionais, inclusive aqueles baseados em
faixas numéricas, exigirão fundamentação específica e aprovação prévia.
Notas, pesos, regras demonstrativas e sua fundamentação não são definidos
por essas medidas. Os dados necessários
à comparação e os critérios de disponibilidade permanecem pendentes na RN-03.
Os exemplos numéricos acima são didáticos; os testes funcionais do GeoVale
continuam futuros.

**Momento de verificação:**

Os critérios serão testados durante a implementação da funcionalidade. Este
registro especifica o comportamento esperado; a funcionalidade ainda não foi
implementada e os testes de medições e alertas ainda não foram executados.

### RF-06 — Aplicação de regras de negócio demonstrativas

**Estado:** definição aprovada pelo responsável pelo projeto em 20/10/2026;
estrutura, fundamentação e comportamento de avaliação das regras demonstrativas
aprovados em 21/10/2026. Primeira regra concreta demonstrativa, RF06-R01,
aprovada em 21/10/2026 para o cenário solar descrito abaixo. As demais regras
e os detalhamentos técnicos indicados nas dependências permanecem pendentes.

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

**Estrutura e fundamentação das regras:**

Cada regra deverá registrar as seguintes informações:

- Identificação: nome e versão da regra utilizada.
- Finalidade: alternativa de uso que a regra avalia.
- Condição: dados necessários e condição que identifica a restrição, com
  parâmetros e unidades quando aplicáveis.
- Fundamentação: fonte consultada, adaptação realizada e limitações;
  hipóteses simuladas deverão ter sua origem e seu caráter demonstrativo
  identificados explicitamente.
- Efeito: em qual condição a regra identifica uma restrição para a alternativa.
- Justificativa do resultado: dados e parâmetros utilizados que sustentam
  a conclusão apresentada.

O [Guia de Indicadores para Planejamento do Fechamento de Mina do IBRAM,
2024, página impressa 20](https://ibram.org.br/wp-content/uploads/2024/08/IBRAM_Guia-de-Indicadores-para-Planejamento-do-Fechamento-de-Mina_A4-2.pdf)
orienta fundamentar estudos de alternativas em aptidões, potencialidades e
restrições do território e das estruturas da mina. Essa referência apoia a
necessidade de justificar as regras; não fornece condições ou limites
universais para o GeoVale. A estrutura de registro acima é uma definição de
escopo do MVP, sem representar um modelo de banco ou uma validação ambiental.

**Comportamento da avaliação:**

Uma regra completa, com os dados necessários disponíveis, deverá apresentar
“restrição identificada” quando sua condição de restrição for atendida ou
“restrição não identificada segundo esta regra” quando não for atendida.
Os resultados deverão identificar nome, versão, alternativa, dados e
parâmetros utilizados e a justificativa correspondente. A avaliação de uma
regra não substitui a avaliação das demais regras aplicáveis à alternativa.

Quando faltar dado necessário à avaliação, apresentar “avaliação indisponível”
e identificar a pendência, sem substituir dados ausentes por zero nem concluir
que não existe restrição. Se faltar dado necessário para avaliar restrições
ou calcular a comparação, bloquear o ranking, preservando resultados parciais
válidos e identificando a indisponibilidade conforme a RN-03.

Uma regra incompleta, sem as informações exigidas acima, não deverá ser
aplicada como se fosse válida: informar o problema de configuração com
mensagem compreensível e apresentar sua avaliação como indisponível, sem
inferir presença ou ausência de restrição.

Uma interseção ou outra ocorrência identificada no RF-05 somente produzirá
restrição quando existir uma regra específica, fundamentada e aprovada que
associe aquela condição à alternativa avaliada. As restrições identificadas
seguirão a RN-01, permanecendo separadas da pontuação, inclusive diante de
notas altas ou previsões favoráveis de ML.

**RF06-R01 — Ausência de superfície fora da água para o cenário solar em terreno:**

- Identificação: RF06-R01, versão 0.1 — regra demonstrativa simulada.
- Finalidade: avaliar o cenário de painéis solares instalados em terreno fora
  da água, sem drenagem, aterro ou estruturas sobre a água. A definição desse
  cenário não encerra a escolha das alternativas nem o cadastro do RF-07.
- Dados necessários: geometria completa da área do RF-02; camada de polígonos
  de massas d’água válida e com cobertura suficiente para avaliar toda a área;
  fontes, datas, cobertura e referências espaciais dos dados, com condições
  adequadas às operações conforme os RF-04, RF-05, RT-01 e RT-02.
- Condição: identificar restrição quando não restar superfície da área de
  estudo fora da união dos polígonos de massas d’água mapeadas. Considerar
  todas as partes de um `MultiPolygon` e seus recortes internos, sem duplicar
  a superfície coberta por polígonos de água sobrepostos. Uma interseção
  parcial ou somente na borda não atende a essa condição.
- Parâmetros e unidades: a condição é a ausência de superfície remanescente,
  sem estabelecer tamanho mínimo de instalação ou limite de declividade.
  As áreas de estudo, de sobreposição e remanescente deverão ser consultáveis
  em m² e hectares. Percentuais arredondados exibidos ao usuário não decidirão
  a cobertura total; referência espacial, precisão e tolerâncias deverão ser
  especificadas antes da implementação, conforme o RT-02.
- Efeito: quando a condição for atendida, apresentar “restrição identificada”
  para esse cenário demonstrativo e aplicar a separação da RN-01. Havendo
  superfície fora da água e condições suficientes de avaliação, apresentar
  “restrição não identificada segundo esta regra”, sem declarar que a
  superfície remanescente seja utilizável ou suficiente para uma instalação.
  As demais regras aplicáveis continuarão necessárias.
- Indisponibilidade: dados ausentes, inválidos ou com cobertura insuficiente,
  referências incompatíveis ou condições de cálculo ainda não definidas que
  impeçam concluir a cobertura deverão produzir “avaliação indisponível”, com
  o motivo. Não presumir ausência de água nem substituir dados por zero;
  preservar resultados parciais válidos e bloquear o ranking quando faltar
  dado necessário à avaliação, conforme a RN-03.
- Justificativa do resultado: identificar regra, versão, cenário avaliado,
  caráter simulado, camadas e elementos utilizados, fontes, datas, cobertura,
  referência espacial, condições de cálculo, medidas e relação espacial que
  sustentam a conclusão ou o motivo da indisponibilidade.

A referência consultada é o documento da EPA/NREL
[Screening Sites for Solar PV Potential, páginas 1 e 6, seção I.3](https://www.epa.gov/sites/production/files/2015-04/documents/solar_decision_tree.pdf),
consultado em 21/10/2026. Ele inclui áreas mineradas entre os locais de
interesse e considera água entre as exclusões na triagem de uso do solo para
energia solar. O documento trata de avaliação preliminar no contexto dos
Estados Unidos e não substitui um estudo específico do local.

A condição de cobertura total e sua consequência eliminatória neste cenário
são uma adaptação simulada do GeoVale, aprovada para demonstrar o software;
não são uma regra universal extraída do documento, uma proibição brasileira
ou uma validação ambiental. A regra não avalia soluções solares flutuantes,
nem intervenções para alterar a superfície da área. A ausência dessa restrição
não comprova viabilidade, segurança, autorização de uso ou aptidão da área.
A representação mapeada depende da data, escala, precisão e cobertura dos
dados; não comprova a situação atual da água no terreno. Os dados reais e os
cenários sintéticos de teste deverão permanecer identificados separadamente.

**Critérios de aceitação:**

| Cenário | Resultado esperado |
| --- | --- |
| Cenário de referência com restrição eliminatória | Identificar a restrição conforme a regra especificada e apresentar a justificativa do resultado. |
| Cenário de referência sem restrição eliminatória | Apresentar o resultado esperado conforme a regra especificada e sua justificativa. |
| Restrição eliminatória acompanhada de pontuação alta | Manter a restrição separada da pontuação, sem permitir sua compensação pela nota. |
| Consulta do resultado de uma regra | Identificar a regra utilizada e a justificativa do resultado. |
| Aplicação de regra simulada | Identificar explicitamente seu caráter simulado. |
| Regra completa com dados necessários disponíveis e condição de restrição atendida | Apresentar “restrição identificada”, com nome, versão, alternativa, dados e parâmetros utilizados e justificativa. |
| Regra completa com dados necessários disponíveis e condição de restrição não atendida | Apresentar “restrição não identificada segundo esta regra”, com os dados da avaliação e a justificativa, sem substituir a avaliação das demais regras aplicáveis. |
| Dado necessário à avaliação de uma regra ausente | Apresentar “avaliação indisponível” e identificar a pendência, sem substituir o dado por zero nem concluir ausência de restrição; bloquear o ranking quando faltar dado necessário para avaliar restrições ou calcular a comparação, preservando resultados parciais válidos conforme a RN-03. |
| Consulta de regra ou parâmetro baseado em hipótese simulada | Identificar sua origem e seu caráter demonstrativo, além da adaptação e das limitações registradas, sem apresentar a hipótese como condição ambiental validada. |
| Regra incompleta, sem alguma informação exigida em sua estrutura | Não aplicar a regra como válida; informar o problema de configuração e apresentar “avaliação indisponível”, sem inferir presença ou ausência de restrição. |
| Regra identifica restrição para alternativa com pontuação alta ou previsão favorável de ML | Preservar a restrição e sua justificativa separadas da pontuação, seguindo a RN-01, sem compensação ou remoção pelo resultado favorável. |
| RF06-R01 com toda a superfície da área coberta por massas d’água e avaliação válida | Identificar a restrição somente para o cenário solar em terreno especificado, com justificativa e caráter simulado; manter a restrição separada da pontuação conforme a RN-01. |
| RF06-R01 com cobertura parcial de água e superfície remanescente, inclusive quando o percentual exibido arredondar para 100% | Apresentar “restrição não identificada segundo esta regra”, sem concluir viabilidade ou suficiência da superfície remanescente nem dispensar outras regras. |
| RF06-R01 com massas d’água tocando somente a borda ou um ponto da área | Não identificar restrição por cobertura total; preservar a distinção entre contato e sobreposição de superfície do RF-05. |
| RF06-R01 com uma parte do `MultiPolygon` coberta por água e outra com superfície fora da água | Considerar todas as partes em conjunto e não identificar cobertura total nem descartar a parte remanescente. |
| RF06-R01 com polígonos de água sobrepostos entre si | Considerar a união das superfícies, sem duplicar áreas nem produzir cobertura total pela soma de sobreposições parciais. |
| RF06-R01 com dados ausentes, inválidos, cobertura insuficiente ou impossibilidade de concluir o cálculo | Apresentar “avaliação indisponível” e o motivo, sem presumir ausência de água; aplicar a RN-03 quanto ao ranking e aos resultados parciais válidos. |
| Consulta da fundamentação e do alcance da RF06-R01 | Identificar fonte, adaptação simulada, versão, cenário solar específico e limitações, sem apresentar a restrição como proibição brasileira ou aprovação ambiental. |

**Dependências e detalhamento pendente:**

O requisito depende das informações do RF-05 e da definição das alternativas
a avaliar. A estrutura, o comportamento de avaliação e a primeira regra
concreta RF06-R01 estão definidos acima, com tratamento de indisponibilidade
conforme a RN-03 e preservação das restrições conforme a RN-01. Permanecem
pendentes as demais regras, suas condições, parâmetros e unidades, fontes,
adaptações e dados necessários. Para a RF06-R01, continuam pendentes a seleção
e preparação da camada concreta na Etapa 6, os critérios de disponibilidade
e adequação da cobertura e os detalhamentos de referência espacial, precisão
e tolerâncias do RT-02, antes da implementação e da preparação dos arquivos
de teste. Este registro não escolhe bases definitivas, não implementa cálculos
e não encerra o RF-07 nem a Etapa 2. As demais pendências dos requisitos
anteriores permanecem em aberto.

**Momento de verificação:**

Os critérios serão testados durante a implementação da funcionalidade. Este
registro especifica o comportamento esperado; a funcionalidade ainda não foi
implementada e os testes de aplicação das regras ainda não foram executados.

### RF-07 — Cadastro e seleção de alternativas de uso futuro

**Estado:** definição aprovada pelo responsável pelo projeto em 20/10/2026;
campos obrigatórios e regras de validação do cadastro e da seleção aprovados
em 21/10/2026. Três cenários de referência para o MVP, com nomes, descrições
e referências, também aprovados em 21/10/2026; detalhamentos das condições de
avaliação permanecem pendentes nos requisitos correspondentes.

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

**Campos e validações do cadastro:**

Cada alternativa deverá ter dois campos obrigatórios:

| Campo | Conteúdo | Exemplo ilustrativo |
| --- | --- | --- |
| Nome da alternativa | Texto que identifica a opção de uso futuro. | Solar em terreno. |
| Descrição do cenário | Texto que explica o cenário representado pela alternativa, para permitir compreender sua comparação e as regras aplicáveis. | Painéis em terreno fora da água, sem drenagem, aterro ou estruturas sobre a água. |

Ambos os campos deverão ser textos preenchidos. Campo ausente, vazio ou
composto somente por espaços impedirá o cadastro, com mensagem que identifique
a pendência: “Informe o nome da alternativa.” ou “Informe a descrição do
cenário.” Valor de outro tipo deverá ser rejeitado, informando que o campo
correspondente deve conter texto.

Nomes repetidos deverão impedir o cadastro, mesmo quando a descrição for
diferente. Para comparar os nomes, desconsiderar maiúsculas e minúsculas,
retirar espaços nas pontas e tratar sequências de espaços como um só.
Por exemplo, “Solar em terreno”, “ SOLAR EM TERRENO ” e “Solar  em terreno”
correspondem ao mesmo nome. Informar: “Já existe uma alternativa com esse
nome. Informe um nome diferente.”

O exemplo dos campos descreve o cenário específico da RF06-R01, incluído
entre os cenários de referência abaixo. Sua descrição não comprova aptidão
ou viabilidade do uso.
O cadastro permitirá identificar as opções avaliadas pelas regras do RF-06
e pelas comparações dos RF-08 e RF-09; os pesos dos critérios serão definidos
no RF-08.

**Cenários de referência para o MVP:**

Os três cenários abaixo orientarão a demonstração do MVP, com nomes e
descrições que seguem os campos do cadastro:

| Nome da alternativa | Descrição do cenário |
| --- | --- |
| Revegetação com espécies nativas | Recuperar a cobertura vegetal das superfícies terrestres, com espécies adequadas à região, a serem definidas posteriormente. |
| Lazer e educação ambiental | Criar um parque de visitação terrestre, com trilhas, espaços de convivência e atividades educativas. |
| Solar em terreno | Instalar painéis em terreno fora da água, sem drenagem, aterro ou estruturas sobre a água, conforme o cenário da RF06-R01. |

Cada cenário representa um objetivo predominante para a área estudada. Por
exemplo, o parque de visitação também poderá ter vegetação. A comparação
avaliará os cenários selecionados para a mesma área de estudo; este registro
não define uma distribuição automática de usos pelo terreno. O cadastro
continuará permitindo outras alternativas que atendam às validações acima.

O estudo de [Servou e colaboradores (2023), A Geospatial Analysis Model for
the Selection of Post-Mining Land Uses in Surface Lignite Mines: Application
in the Ptolemais Mines, Greece](https://www.mdpi.com/2071-1050/15/19/14388)
considera usos florestais, parques recreativos e usos industriais que incluem
instalações fotovoltaicas, além do uso agrícola. Isso fundamenta a consideração
dessas famílias de usos, sem validar sua aplicação em Minas Gerais. A escolha
dos três cenários, seus nomes e descrições, incluindo o recorte de revegetação
com espécies nativas e de lazer com educação ambiental, são adaptações
demonstrativas do GeoVale, não uma reprodução direta dos cenários do estudo.

O documento da [EPA/NREL, Screening Sites for Solar PV Potential, página 1](https://www.epa.gov/sites/production/files/2015-04/documents/solar_decision_tree.pdf)
inclui áreas mineradas entre os locais considerados na triagem solar. Seu
alcance é preliminar e não substitui avaliação específica do local, conforme
as limitações já registradas na RF06-R01. Essas referências foram consultadas
em 21/10/2026.

A escolha dos cenários define o que comparar. Espécies, critérios, notas,
pesos, regras adicionais de restrição, dados necessários e condições de
viabilidade ainda serão detalhados e fundamentados nas unidades correspondentes.
O registro não comprova adequação ambiental, segurança ou autorização de uso
da área. O atendimento dos critérios de aceitação do cadastro e da seleção
continuará sendo verificado na implementação, com os cenários de referência
identificáveis na preparação da demonstração.

**Validações da seleção:**

A seleção deverá aceitar somente alternativas cadastradas. Ao receber uma
seleção inexistente no cadastro, informar “Selecione somente alternativas
cadastradas.” e impedir o início da comparação com essa seleção inválida.
Deverão estar selecionadas pelo menos duas alternativas distintas; selecionar
a mesma alternativa mais de uma vez não contará como alternativas diferentes.
Se o mínimo não for atendido, informar “Selecione pelo menos duas alternativas
distintas para comparar.” e impedir o início da comparação.

Atender ao mínimo de alternativas não dispensa as demais condições necessárias
à comparação, incluindo o bloqueio por indisponibilidade dos dados necessários
conforme a RN-03 e o tratamento das restrições conforme a RN-01.

**Critérios de aceitação:**

| Cenário | Resultado esperado |
| --- | --- |
| Cadastro com dados válidos conforme as regras especificadas | Permitir cadastrar e identificar a alternativa. |
| Seleção de alternativas cadastradas | Permitir conferir quais alternativas foram selecionadas para a comparação da área em análise. |
| Seleção de pelo menos duas alternativas distintas | Atender ao mínimo de alternativas necessário para iniciar a comparação. |
| Seleção de menos de duas alternativas distintas | Impedir o início da comparação e informar a necessidade de selecionar pelo menos duas alternativas distintas. |
| Dados de cadastro inválidos | Informar o problema com mensagem compreensível. |
| Nome ausente, vazio ou composto somente por espaços | Impedir o cadastro e solicitar o nome da alternativa, identificando o campo pendente. |
| Descrição do cenário ausente, vazia ou composta somente por espaços | Impedir o cadastro e solicitar a descrição do cenário, identificando o campo pendente. |
| Nome ou descrição informado com valor que não seja texto | Rejeitar o cadastro e informar que o campo correspondente deve conter texto. |
| Nome já cadastrado, inclusive com variações de maiúsculas, minúsculas, espaços nas pontas ou espaços consecutivos | Impedir o novo cadastro e informar que já existe uma alternativa com esse nome, mesmo que a descrição seja diferente. |
| Seleção contendo alternativa inexistente no cadastro | Informar que somente alternativas cadastradas podem ser selecionadas e impedir o início da comparação com essa seleção inválida. |
| Seleção da mesma alternativa mais de uma vez, sem uma segunda alternativa distinta | Contar somente uma alternativa distinta, impedir o início da comparação e solicitar pelo menos duas alternativas distintas. |

**Dependências e detalhamento pendente:**

O requisito depende da área identificada pelo RF-02. Os dois campos
obrigatórios, as validações do cadastro e da seleção e os três cenários de
referência do MVP estão definidos acima. Permanecem pendentes os detalhamentos
das condições de avaliação desses usos, das demais regras do RF-06, dos
critérios, notas e pesos dos RF-08 e RF-09 e dos dados necessários, incluindo
a disponibilidade conforme a RN-03. As espécies para revegetação serão
definidas posteriormente, considerando sua adequação à região. O armazenamento
será detalhado nas etapas correspondentes, conforme o RF-11. Os arquivos de
teste e a verificação funcional serão preparados na implementação; as demais
pendências dos requisitos anteriores permanecem em aberto. Este detalhamento
não implementa o cadastro nem encerra a Etapa 2.

**Momento de verificação:**

Os critérios serão testados durante a implementação da funcionalidade. Este
registro especifica o comportamento esperado; a funcionalidade ainda não foi
implementada e os testes de cadastro e seleção ainda não foram executados.

### RF-08 — Definição de critérios, notas e pesos

**Estado:** definição aprovada pelo responsável pelo projeto em 20/10/2026;
dados, unidades, referências e limitações dos cinco itens geográficos aprovados
em 21/10/2026. Reorganização desses itens como indicadores de apoio e definição
de três dimensões comuns para a comparação aprovadas em 21/10/2026.
Operacionalização, escalas, notas, limites, valores dos pesos e demais
detalhamentos indicados nas dependências permanecem pendentes.

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

**Dimensões comuns da comparação:**

A comparação das alternativas selecionadas utilizará as três dimensões comuns
abaixo, retomando a organização de aptidão, custos e benefícios do planejamento
do GeoVale:

| Dimensão comum | O que avaliar | Detalhamento ainda necessário |
| --- | --- | --- |
| Aptidão física para o uso | Adequação demonstrativa da área ao cenário avaliado. | Atributos pertinentes ao uso, fundamentação da avaliação e conversão em nota. Na Etapa 8, receberá a contribuição do ML, com alvo, integração e limitações detalhados no RF-13. |
| Custo de implantação e adaptação | Esforço financeiro para implantar e adaptar o cenário. | Escopo, período considerado, dados e método de estimativa, unidade e conversão em nota. |
| Benefícios esperados | Resultados pretendidos de cada uso. | Aspectos a avaliar, evidências, forma de avaliação e conversão em nota comparável entre alternativas. |

As alternativas de uma mesma comparação serão avaliadas nessas mesmas
dimensões e com a mesma configuração de pesos. Cada dimensão terá seu próprio
peso, comum às alternativas; as notas serão específicas de cada alternativa.
Notas, escalas, limites e valores dos pesos ainda deverão ser definidos e
aprovados. A configuração utilizada deverá ser consultável.

Os cinco indicadores geográficos registrados abaixo fornecerão informações
de apoio à avaliação de cada uso. Eles não serão adicionados automaticamente
como cinco notas extras ao ranking. Sua interpretação e associação às
dimensões ainda precisarão ser fundamentadas e detalhadas por cenário.

O [Multi-criteria analysis: a manual, edição de 2009, seções 4.3.2 e 5.1](https://assets.publishing.service.gov.uk/media/5a790545e5274a2acd18b975/1132618.pdf)
descreve a matriz de desempenho que avalia cada opção em relação aos critérios
definidos para a decisão. Essa referência apoia a organização comum da
comparação; a escolha das três dimensões e o uso dos indicadores são definições
demonstrativas do GeoVale, não uma validação ambiental ou financeira. A fonte
foi consultada em 21/10/2026.

**Indicadores geográficos de apoio e dados necessários:**

Os três indicadores iniciais abaixo apoiam a avaliação dos cenários de referência
do RF-07: Revegetação com espécies nativas, Lazer e educação ambiental e Solar
em terreno. Sua utilização dependerá da interpretação justificada para cada
uso e da definição dos dados necessários, sem produzir uma pontuação automática.

| Indicador de apoio | O que observar | Dados necessários e unidades |
| --- | --- | --- |
| Declividade do terreno | Inclinação das superfícies dentro da área estudada. | Modelo digital de elevação adequado à área; declividade em graus. |
| Proximidade de vias mapeadas | Localização da área em relação às estradas e outras vias. | Camada de vias com cobertura adequada; distância geométrica em metros. |
| Proximidade de vegetação nativa remanescente | Entorno vegetal, principalmente para o cenário de revegetação. | Camada que identifique remanescentes de vegetação nativa, com cobertura adequada; distância geométrica em metros. |

A medida de declividade depende da seleção de um modelo de elevação adequado,
do método de cálculo e da definição de como resumir os valores existentes
dentro da área, incluindo suas partes. Esses procedimentos ainda deverão
ser detalhados e aprovados. As medidas de proximidade serão geométricas,
conforme o caráter descritivo do RF-05; referências espaciais, precisão,
tolerâncias e alcance das consultas continuam pendentes. Avaliar rotas e
acesso efetivo às vias exige informações adicionais; proximidade de vegetação
é uma medida de localização e exige análise adicional para avaliar conectividade
ecológica. As medidas não constituem por si só nota, restrição ou conclusão
de viabilidade dos usos.

O estudo de [Servou e colaboradores (2023), A Geospatial Analysis Model for
the Selection of Post-Mining Land Uses in Surface Lignite Mines: Application
in the Ptolemais Mines, Greece, seção 2.2.1](https://www.mdpi.com/2071-1050/15/19/14388)
utiliza modelo digital de elevação para declividade e distâncias euclidianas
para vias e outros elementos na avaliação de usos pós-mineração. Sua análise
emprega mapas por células e condições da área estudada na Grécia; o resumo
descritivo da área no GeoVale e sua conversão futura em notas constituem
adaptações, não uma reprodução direta ou validação local do estudo.

O estudo de [Worden e colaboradores (2024), Regional post-mining land use
assessment: An interdisciplinary and multi-stakeholder approach, tabela 2](https://doi.org/10.1016/j.resourpol.2024.104680)
considera proximidade de ecossistemas remanescentes na avaliação de usos
ecológicos em regiões mineradoras de Queensland, Austrália. Para energia
solar, considera também radiação solar e proximidade da rede elétrica, entre
outros critérios. A medida de proximidade de vegetação nativa proposta para
o cenário de revegetação é uma adaptação demonstrativa do GeoVale. As fontes
foram consultadas em 21/10/2026; seus parâmetros não foram adotados como
limites universais para o MVP.

A seleção dos três indicadores é um recorte inicial de escopo apoiado nessas
referências, complementado pelos dois indicadores solares descritos abaixo.
As bases ainda precisam ser selecionadas e preparadas na Etapa 6, incluindo
as novas camadas de vias e vegetação. O detalhamento dos cruzamentos
correspondentes no RF-04 continua futuro.

**Indicadores complementares para Solar em terreno:**

Os dois indicadores a seguir detalham aspectos específicos do cenário Solar
em terreno do RF-07, apoiados na consideração de recurso solar e proximidade
da transmissão no estudo de Worden e colaboradores (2024) referenciado acima.
A definição das medidas e o recorte das fontes candidatas são adaptações de
escopo do GeoVale; os limites usados no estudo australiano não serão adotados
automaticamente como condições ou notas do MVP.

| Indicador solar de apoio | O que representar | Dados necessários e unidade |
| --- | --- | --- |
| Recurso solar disponível | Média anual do total diário da irradiação global horizontal (GHI), representando a energia solar recebida por unidade de superfície horizontal. | Base de GHI com cobertura, período de referência, resolução e unidade identificados; apresentação em kWh/m²/dia. |
| Proximidade de linhas de transmissão existentes | Distância geométrica entre a área estudada e as linhas de transmissão existentes na cobertura consultada. | Camada de linhas de transmissão com situação existente identificável, fonte e cobertura adequadas; distância em metros. |

Como fonte candidata para o recurso solar, o [Atlas Brasileiro de Energia
Solar, 2ª edição (2017), INPE/LABREN](https://labren.ccst.inpe.br/atlas_2017.html)
disponibiliza médias anuais e mensais do total diário da irradiação global
horizontal em Wh/m²/dia. Para a apresentação proposta, converter Wh/m²/dia
em kWh/m²/dia dividindo o valor por 1.000. A média anual do total diário deverá
permanecer identificada, juntamente com o período da base; não confundir
média diária com total anual. A fonte informa resolução de 0,1° × 0,1°,
aproximadamente 10 × 10 km. Essa resolução oferece contexto regional e sua
adequação à área demonstrativa ainda deverá ser avaliada na Etapa 6.
O método para associar ou resumir os registros de GHI para a área também
permanece pendente, sem presumir detalhamento interno compatível com a mina.

Como fonte candidata para a transmissão, o [WEBMAP EPE](https://www.epe.gov.br/pt/publicacoes-dados-abertos/publicacoes/webmap-epe)
permite consultar e obter dados geográficos e metadados de linhas e subestações
de transmissão, com grupos de infraestrutura existente e planejada. O recorte
deste indicador será de linhas de transmissão existentes; manter identificada
a situação da infraestrutura e distinguir as planejadas, que não comporão
a medida de proximidade a linhas existentes. O indicador não representa toda
a rede local de distribuição. A distância seguirá o caráter geométrico do
RF-05, considerando a cobertura efetivamente analisada, sem presumir a linha
mais próxima fora dessa cobertura. Seleção e preparação da camada, alcance
da consulta, referências espaciais, precisão e tolerâncias ainda são pendentes.

A irradiação caracteriza o recurso solar disponível; estimar geração elétrica
exige informações adicionais da instalação. Proximidade de uma linha é um
indicador de localização; a possibilidade real de conexão exige avaliação
específica. As medidas não comprovam geração, conexão disponível ou viabilidade
do uso e não geram, por si só, notas ou restrições eliminatórias. Fontes,
unidades, período, resolução e situação da infraestrutura, conforme aplicáveis,
adaptações e limitações deverão ser consultáveis. As páginas das duas fontes
candidatas foram consultadas em 21/10/2026; elas ainda não foram selecionadas
como bases definitivas ou preparadas para a aplicação. Esta unidade registra
a descrição dos indicadores solares de apoio no RF-08.

**Aplicação dos indicadores e tratamento dos dados:**

A declividade caracteriza o relevo para os três usos, com interpretação
específica por cenário. A proximidade de vias apoia a análise de acesso e
logística, que exige informações adicionais. A proximidade de vegetação
nativa apoia a leitura do contexto ambiental, especialmente da revegetação.
Recurso solar e proximidade da transmissão apoiam especificamente a avaliação
de Solar em terreno. Os indicadores não substituem os estudos necessários
para avaliar cada uso.

A ausência de necessidade de um indicador para determinado uso não deverá
ser transformada automaticamente em nota zero. Por exemplo, não precisar
avaliar conexão elétrica para revegetação não atribui uma nota zero à
alternativa. Isso não dispensa a avaliação das três dimensões comuns nem
altera automaticamente seus pesos. A definição de quais dados cada avaliação
exige e a associação dos indicadores às dimensões permanecem pendentes.

Indicadores, critérios e suas condições de utilização deverão permitir
consultar fontes, unidades, adaptações e limitações. A falta de dado necessário
à comparação seguirá a RN-03: indicar a indisponibilidade e o motivo, sem
substituir dados ausentes por zero ou concluir ausência de ocorrência;
bloquear o ranking quando necessário e preservar resultados parciais válidos.
Dados simulados deverão ser explicitamente identificados conforme a RN-02;
essa possibilidade não autoriza preencher automaticamente dados reais ausentes.
As restrições do RF-06 continuarão separadas da pontuação conforme a RN-01.

**Critérios de aceitação:**

| Cenário | Resultado esperado |
| --- | --- |
| Configuração com valores válidos conforme as regras especificadas | Permitir definir critérios, atribuir notas às alternativas e configurar os pesos dos critérios. |
| Consulta da configuração da comparação | Apresentar os critérios, as notas e os pesos configurados. |
| Consulta de uma nota atribuída | Identificar a alternativa e o critério correspondentes. |
| Informação de valores inválidos | Rejeitar os valores e informar o problema com mensagem compreensível. |
| Consulta da configuração de uma comparação entre alternativas | Identificar as três dimensões comuns, a mesma configuração de pesos utilizada para todas as alternativas e as notas específicas de cada alternativa. |
| Indicador solar sem necessidade de avaliação para revegetação | Não atribuir automaticamente nota zero pela ausência dessa necessidade; preservar as dimensões comuns e a configuração de pesos, sem dispensar dados necessários à avaliação. |
| Dado necessário à avaliação de uma dimensão indisponível | Identificar a pendência e aplicar a RN-03, bloqueando o ranking quando necessário e preservando resultados parciais válidos; não substituir o dado por zero nem preencher automaticamente com valor simulado. |

**Dependências e detalhamento pendente:**

O requisito depende das alternativas do RF-07. As três dimensões comuns,
a configuração de pesos compartilhada entre alternativas e os cinco
indicadores geográficos de apoio, com dados, unidades, fontes e limitações,
estão definidos acima. Permanecem pendentes a associação e interpretação dos
indicadores por cenário, os dados necessários a cada dimensão, os aspectos
dos benefícios esperados, o escopo, período e método de estimativa dos custos,
as escalas comparáveis e a conversão em notas, limites, valores e validação
dos pesos e demais detalhes do tratamento de dados ausentes.

Seleção e preparação das bases, adequação das fontes candidatas, cruzamentos
adicionais do RF-04, cálculo e resumo da declividade, associação ou resumo da
GHI, alcance das consultas, referências espaciais, precisão e tolerâncias
continuam pendentes. As definições deverão ser aprovadas antes da implementação
e da preparação dos cenários de teste. Os reflexos dessa organização no RF-09
e na contribuição do ML prevista no RF-13 serão tratados em unidades próprias;
esses requisitos não foram alterados nesta unidade. As RN-01, RN-02 e RN-03 e
as demais pendências anteriores permanecem válidas. Este registro não implementa
cálculos, não atribui notas ou pesos e não encerra a Etapa 2.

**Momento de verificação:**

Os critérios serão testados durante a implementação da funcionalidade. Este
registro especifica o comportamento esperado; a funcionalidade ainda não foi
implementada e os testes de configuração de critérios, notas e pesos ainda
não foram executados.

### RF-09 — Cálculo multicritério por soma ponderada

**Estado:** definição aprovada pelo responsável pelo projeto em 20/10/2026;
alinhamento às três dimensões comuns e à configuração de pesos compartilhada
do RF-08 aprovado em 21/10/2026. Escalas, notas, valores e validação dos pesos,
normalização, precisão, empates e demais detalhes de valores ausentes
permanecem pendentes de definição.

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

**Composição da pontuação e configuração comum:**

Para cada alternativa, a pontuação será composta pelas notas das três dimensões
definidas no RF-08:

```text
Pontuação =
  nota de aptidão física para o uso × peso da aptidão
+ nota de custo de implantação e adaptação × peso do custo
+ nota de benefícios esperados × peso dos benefícios
```

As alternativas selecionadas para uma mesma comparação utilizarão a mesma
configuração de pesos. Cada dimensão terá seu próprio peso, compartilhado
entre as alternativas, e cada alternativa terá suas notas específicas.
As notas e os pesos efetivamente usados no cálculo deverão ser identificáveis.
A nota de custo dependerá da conversão para uma escala comparável a ser definida
no RF-08; o valor monetário não entrará diretamente nessa soma. Escalas e
conversões em notas, valores dos pesos e sua validação ainda deverão ser
especificados e aprovados antes da implementação do cálculo.

Os cinco indicadores geográficos do RF-08 serão informações de apoio à
avaliação dos usos; não entrarão automaticamente como cinco notas extras
na soma ponderada. O cálculo utilizará as notas das três dimensões comuns,
conforme a configuração aprovada para a comparação.

Entradas de pontuação incompatíveis com as três dimensões e com a configuração
comum de pesos deverão ser rejeitadas, sem calcular a classificação com essas
entradas. Informar a incompatibilidade com mensagem compreensível, sem
substituir automaticamente a configuração de uma alternativa para fazer
prosseguir o cálculo.

As restrições continuarão separadas da pontuação, conforme a RN-01; uma nota
alta não removerá ou compensará uma restrição. A falta de dado necessário
para avaliar restrições ou calcular a comparação bloqueará o ranking, com
preservação dos resultados parciais válidos conforme a RN-03, sem substituir
dados ausentes por zero. Simulações deverão permanecer explicitamente
identificadas conforme a RN-02. Este alinhamento não implementa o cálculo.

**Critérios de aceitação:**

| Cenário | Resultado esperado |
| --- | --- |
| Cálculo com entradas válidas | Calcular as pontuações por soma ponderada e apresentar a classificação das alternativas. |
| Conferência com um cálculo de referência | As pontuações e a classificação deverão corresponder ao esperado conforme as regras e a precisão especificadas. |
| Consulta das entradas utilizadas no cálculo | Identificar as notas e os respectivos pesos utilizados. |
| Alternativa com restrição eliminatória e pontuação alta | Manter a restrição separada da pontuação, sem permitir sua compensação pela nota. |
| Entradas inconsistentes | Informar o problema com mensagem compreensível. |
| Comparação com entradas válidas para as três dimensões do RF-08 | Usar a mesma configuração de pesos para as alternativas e suas notas específicas de aptidão física, custo e benefícios; identificar as entradas efetivamente utilizadas. |
| Entradas de pontuação incompatíveis com as três dimensões ou com a configuração comum de pesos | Rejeitar o cálculo da classificação com essas entradas e informar a incompatibilidade com mensagem compreensível, sem ajustar automaticamente a configuração de uma alternativa. |
| Análise com cinco indicadores geográficos de apoio e notas válidas para as três dimensões comuns | Utilizar na soma ponderada as notas das três dimensões, sem acrescentar automaticamente os indicadores como notas extras. |

**Dependências e detalhamento pendente:**

O requisito depende das regras do RF-06, das alternativas do RF-07 e das três
dimensões comuns, notas e configuração de pesos do RF-08. O alinhamento da
composição da pontuação está definido acima. Permanecem pendentes as escalas
comparáveis e a conversão em notas de cada dimensão, incluindo custo e
benefícios, valores e validação dos pesos, normalização, precisão, empates
e demais detalhes de dados ausentes. Essas definições deverão ser aprovadas
antes da implementação e da preparação dos cenários de teste com cálculo de
referência. Preservar o tratamento das RN-01, RN-02 e RN-03. O reflexo da
organização na contribuição do ML do RF-13 será tratado em unidade posterior;
o RF-13 não foi alterado nesta unidade. As demais pendências anteriores
permanecem em aberto, e a Etapa 2 não está encerrada.

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
alinhamento da contribuição do ML à dimensão de aptidão física do RF-08 e
à soma ponderada do RF-09 e significado demonstrativo do alvo por uso aprovados
em 21/10/2026. Saída por classes e três nomes, ordem e significados qualitativos
aprovados em 21/10/2026: Baixa, Moderada e Alta. Condições e limites técnicos
das classes, atributos, escalas, conversão em nota, treinamento e avaliação
permanecem pendentes de definição.

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

**Significado do alvo e alcance da previsão:**

O alvo será a compatibilidade física demonstrativa entre as características
geográficas consideradas da área e o cenário de uso avaliado. A previsão
procurará representar quanto essas características favorecem esse uso, limitada
aos aspectos cobertos pelos atributos e pelas respostas de referência do
treinamento que vierem a ser especificados e aprovados.

Para os três cenários de referência do RF-07, o significado será:

| Cenário de referência | Significado da aptidão física demonstrativa |
| --- | --- |
| Revegetação com espécies nativas | Condições físicas consideradas que favorecem a implantação da vegetação proposta. |
| Lazer e educação ambiental | Condições físicas consideradas que favorecem a implantação dos espaços e atividades previstos no cenário. |
| Solar em terreno | Condições físicas consideradas que favorecem a implantação de painéis no cenário solar definido no RF-07, preservando o alcance da regra RF06-R01. |

A mesma área poderá receber avaliações diferentes para cada uso. Cada resultado
deverá identificar a alternativa correspondente; a saída do ML não será apenas
um nome de uso vencedor. A escolha comparativa continuará dependendo das notas
de aptidão, custo e benefícios, dos pesos do RF-09 e das restrições da RN-01.
Esta definição não divide automaticamente a área entre usos nem fixa quantidade
de modelos ou arquitetura de treinamento.

O resultado não comprovará segurança, estabilidade geotécnica, ausência de
contaminação, recuperação ambiental ou viabilidade da instalação. Um atributo
geográfico, como declividade, representa somente o aspecto que mede; condições
não cobertas pelos dados não deverão ser presumidas favoráveis. Dados necessários
indisponíveis continuarão sujeitos à RN-03.

A avaliação física por uso tem como referência [Servou e colaboradores (2023)](https://www.mdpi.com/2071-1050/15/19/14388),
que combinaram características físicas e informações específicas da mineração
para avaliar usos pós-mineração em um caso grego. O significado do alvo de ML
acima é uma adaptação demonstrativa do GeoVale; o estudo não valida esse modelo
nem transfere automaticamente critérios, limites ou resultados para a área local.

No treinamento supervisionado, os mapas fornecerão atributos; também serão
necessários exemplos com respostas de referência para o alvo. Essa distinção
entre atributos e valores-alvo é descrita na [documentação conceitual do
scikit-learn](https://scikit-learn.org/stable/getting_started.html), utilizada
como referência sem selecionar a stack nesta unidade. Origem, obtenção e
validação dessas respostas ainda deverão ser especificadas. Quando simuladas,
a previsão demonstrará o aprendizado das relações dessa simulação, conforme
as limitações da RN-02, sem comprovar capacidade preditiva real.

**Representação da saída por classes de aptidão:**

A previsão será apresentada como uma classe de aptidão física demonstrativa
para cada uso avaliado. A tarefa do ML será de classificação em categorias;
essa classificação não corresponde ao ranking das alternativas do RF-09.
A escolha por classes busca facilitar a comunicação do resultado no MVP;
não comprova maior validade técnica ou capacidade preditiva do modelo.

Serão utilizadas três classes, com os mesmos nomes e significados qualitativos
para os três usos de referência, aplicados às características relevantes a cada
uso:

| Classe | Significado qualitativo no MVP |
| --- | --- |
| Baixa | As características físicas consideradas são pouco favoráveis ao uso avaliado. |
| Moderada | As características físicas consideradas apresentam favorabilidade intermediária para o uso avaliado. |
| Alta | As características físicas consideradas são mais favoráveis ao uso avaliado. |

A ordem será Baixa, Moderada e Alta, da menor para a maior aptidão demonstrativa.
Essa ordem não define distâncias numéricas iguais entre as classes nem suas
notas na comparação. A mesma área poderá receber uma classe diferente por uso;
condições e limites técnicos para atribuir cada classe continuam pendentes.

A [FAO, em A Framework for Land Evaluation, capítulo 3](https://www.fao.org/4/x5310e/x5310e04.htm),
apresenta graus de aptidão avaliados por uso. Os três nomes e significados acima
são uma simplificação demonstrativa do GeoVale, sem adoção integral da metodologia,
importação de seus limites ou equivalência automática com as classes oficiais
da FAO. A referência não valida o classificador ou seus resultados locais.

As condições e os limites técnicos das classes deverão ser fundamentados,
especificados e aprovados antes da implementação e da preparação das respostas
de referência para o treinamento. A distinção conceitual entre classificação
e regressão consta da documentação do scikit-learn já referenciada; esta unidade
não seleciona algoritmo ou stack.

A classe prevista e a nota comparável de aptidão física serão informações
distintas. A conversão de classe em nota para os RF-08 e RF-09 exigirá uma regra
fundamentada, especificada e aprovada; eventuais códigos numéricos de categorias
não serão usados automaticamente como notas. A saída escolhida nesta unidade
não será um índice numérico contínuo ou percentual de certeza. Valores dos
pesos continuarão pendentes, sem serem definidos ou alterados pelo formato
da previsão.

Avaliação indisponível será um estado separado das classes de aptidão. A falta
de dado necessário não deverá produzir automaticamente uma classe de menor
aptidão ou uma nota zero. Identificar o motivo, bloquear o ranking e preservar
resultados parciais válidos conforme a RN-03. Restrições da RN-01 permanecem
independentes da classe prevista e simulações continuam identificadas pela RN-02.
Baixa não significará automaticamente restrição eliminatória; Alta não removerá
uma restrição identificada nem comprovará autorização ou viabilidade. Avaliação
indisponível não será uma quarta classe de aptidão.

**Contribuição à dimensão de aptidão física:**

A previsão demonstrativa contribuirá para a nota de Aptidão física para o uso
de cada alternativa, dimensão comum definida no RF-08. A conversão da previsão
em nota comparável ainda deverá ser especificada e aprovada. Deverá ser possível
identificar a alternativa avaliada, os atributos utilizados, a previsão obtida
e sua relação com a nota dessa dimensão, conforme a conversão que vier a ser
aprovada. A origem do treinamento e as limitações deverão permanecer
identificáveis no dashboard e no relatório, conforme os RF-10 e RF-12.

O RF-09 utilizará a nota da dimensão de aptidão física na soma ponderada,
juntamente com as notas de custo e benefícios. A previsão não será acrescentada
como quarta dimensão ou como parcela extra nessa soma. A configuração de pesos
compartilhada entre alternativas permanecerá preservada. O ML deste requisito
não estimará automaticamente custos ou benefícios; essas dimensões terão
avaliações próprias, com dados, métodos e escalas ainda a especificar no RF-08.

As restrições eliminatórias continuarão preservadas conforme a RN-01, mesmo
com previsão favorável. Informações simuladas e treinamento sintético deverão
permanecer explicitamente identificados conforme a RN-02; resultados com
esse treinamento não comprovam capacidade preditiva em áreas reais nem
substituem avaliação especializada.

A falta de dado necessário para produzir a previsão ou convertê-la em nota
necessária à comparação seguirá a RN-03: identificar a indisponibilidade e
seu motivo, bloquear o ranking e preservar resultados parciais válidos. Não
substituir dados ausentes por zero, preencher automaticamente com simulações
ou ajustar automaticamente os pesos para prosseguir com a comparação.

O significado do alvo, a saída por classes e o papel do ML na comparação
estão definidos acima, incluindo os três nomes, a ordem e os significados
qualitativos das classes. Permanecem pendentes as condições e os limites técnicos
das classes, os atributos, as escalas, a conversão em nota, o algoritmo,
o treinamento e a avaliação. Esta unidade não implementa o modelo ou o cálculo
multicritério e não atribui valores aos pesos.

**Critérios de aceitação:**

| Cenário | Resultado esperado |
| --- | --- |
| Previsão com atributos válidos conforme as regras especificadas | Produzir a previsão e permitir identificar os atributos utilizados e o resultado obtido. |
| Integração da previsão ao MVP final | Utilizar a previsão como entrada da comparação e apresentá-la no dashboard e no relatório. |
| Consulta da origem e das limitações do modelo | Disponibilizar a origem dos dados de treinamento e as limitações, identificando treinamento sintético quando utilizado. |
| Reprodução dos testes do modelo | Permitir reproduzir os testes conforme os dados, procedimentos e critérios de avaliação documentados. |
| Entradas inválidas | Informar o problema com mensagem compreensível. |
| Previsão favorável acompanhada de restrição eliminatória | Preservar a restrição, sem permitir sua substituição ou compensação pela previsão. |
| Integração de previsão válida à nota de aptidão física de uma alternativa, conforme conversão aprovada | Contribuir para a nota dessa dimensão no RF-08 e na soma ponderada do RF-09, sem criar quarta dimensão ou parcela extra; preservar a configuração comum de pesos e manter custos e benefícios em avaliações próprias, sem estimá-los automaticamente por este ML. |
| Consulta da contribuição do ML na comparação, no dashboard e no relatório | Identificar a alternativa, os atributos, a previsão e sua relação com a nota de aptidão física, conforme a conversão aprovada, mantendo a origem do treinamento e as limitações consultáveis e as simulações identificadas. |
| Dado necessário à previsão ou à conversão em nota necessária à comparação indisponível | Informar a indisponibilidade e o motivo, bloquear o ranking e preservar resultados parciais válidos conforme a RN-03, sem substituir dados ausentes por zero, preencher automaticamente com simulações ou ajustar automaticamente os pesos. |
| Avaliação da mesma área para os três cenários de referência, com entradas válidas conforme a especificação | Identificar a aptidão física demonstrativa correspondente a cada uso, permitindo avaliações diferentes; não substituir essas avaliações por um único nome de uso vencedor nem pela classificação final do RF-09. |
| Consulta do significado e do alcance de uma previsão | Informar o uso avaliado e o alcance limitado aos aspectos considerados; não apresentar o resultado como comprovação de segurança, estabilidade geotécnica, ausência de contaminação, recuperação ambiental ou viabilidade da instalação, nem presumir condições não avaliadas como favoráveis. |
| Previsão com entradas válidas e classes especificadas e aprovadas | Apresentar a classe de aptidão física demonstrativa e o uso correspondente, distinguindo-a da nota comparável e do ranking final; aplicar somente uma conversão em nota previamente especificada e aprovada, sem usar automaticamente códigos de categorias como notas. |
| Falta de dado necessário à avaliação por classes | Informar avaliação indisponível e o motivo, sem atribuir automaticamente classe de menor aptidão ou nota zero; bloquear o ranking e preservar resultados parciais válidos conforme a RN-03. |
| Consulta dos nomes, da ordem e do significado qualitativo das classes | Apresentar exatamente Baixa, Moderada e Alta, da menor para a maior aptidão demonstrativa, com o significado definido para o uso avaliado, sem atribuir automaticamente notas ou distâncias numéricas iguais entre as classes. |
| Consulta de resultado Baixa ou Alta, de avaliação indisponível e de restrição identificada | Distinguir as classes de aptidão dos estados da avaliação e das restrições: Baixa não indica automaticamente restrição; Alta não remove restrição nem comprova autorização ou viabilidade; indisponibilidade não é uma quarta classe. Preservar RN-01 e RN-03. |

**Dependências e detalhamento pendente:**

O requisito depende dos atributos provenientes da análise geográfica, das
alternativas do RF-07, da dimensão de aptidão física e das escalas comparáveis
do RF-08 e da composição da soma ponderada do RF-09. A contribuição da previsão
para essa dimensão, o significado demonstrativo do alvo por uso e a saída por
classes estão definidos acima, com três nomes, ordem e significados qualitativos.
Permanecem pendentes as condições e os limites técnicos das classes, os atributos
necessários, as respostas de referência para o treinamento, sua origem, obtenção
e validação, as escalas, a conversão das classes em notas, o algoritmo,
o treinamento e a avaliação. Essas definições deverão ser aprovadas antes da implementação e
da preparação dos testes correspondentes. Custos e benefícios continuam com
avaliações próprias a detalhar no RF-08. Preservar as RN-01, RN-02 e RN-03 e as demais pendências
anteriores. Este alinhamento não altera os RF-08 e RF-09 nem encerra a Etapa 2.

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
