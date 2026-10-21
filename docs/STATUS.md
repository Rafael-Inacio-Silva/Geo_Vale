# Estado do projeto — GeoVale

**Atualização:** 21/10/2026.
**Etapa atual:** 2 — Engenharia de requisitos do sistema, iniciada com autorização em 20/10/2026.
**Subetapa atual:** atores AT-01 e AT-02, definições dos RF-01 a RF-13, RNF-01 a RNF-06, RT-01 a RT-02 e RN-01 a RN-03 aprovadas, documentadas e publicadas; revisões documentais dos seis RNF, dos dois RT e das três RN concluídas; exigência das licenças explícita no RT-01 e classificação da RN-01 detalhada para dados necessários disponíveis e efeitos da indisponibilidade detalhados na RN-03; referência entre RN-01 e RN-03 sincronizada; levantamento das pendências de encerramento organizado em seis blocos e formato inicial GeoJSON `.geojson`, estrutura `FeatureCollection`, tipos `Polygon` e `MultiPolygon`, regras de validade das geometrias e limites de 1 MiB e 20.000 posições por arquivo aprovados no RF-01; opção de uma área preparada por arquivo, com exatamente uma `Feature` e todas as partes válidas de um `MultiPolygon` analisadas em conjunto, aprovada nos RF-01 e RF-02; cruzamentos iniciais com unidades de conservação, rios e drenagem e massas d’água aprovados no RF-04; medidas descritivas iniciais de área, percentual e distância, com referências e limitações, aprovadas no RF-05; condições e mensagens dos alertas informativos iniciais também aprovadas no RF-05; estrutura, fundamentação e comportamento de avaliação das regras demonstrativas e primeira regra concreta RF06-R01 aprovados no RF-06 em 21/10/2026; nome e descrição obrigatórios, validações do cadastro e da seleção e três cenários de referência do MVP aprovados no RF-07 em 21/10/2026; três critérios iniciais, dados, unidades, referências e limitações aprovados no RF-08 em 21/10/2026; demais decisões de comportamento, demais detalhamentos técnicos e verificações da aplicação ainda pendentes.

Este documento registra o estado observado nesta entrega. Não há aplicação
executável nem funcionalidades de geoprocessamento, análise multicritério ou
Machine Learning implementadas. A Etapa 0 foi concluída e aprovada em
19/10/2026. A Etapa 1 foi iniciada com autorização do responsável; o problema
de negócio, o objetivo do sistema, o público-alvo, os benefícios esperados e
o escopo, as limitações e os critérios de sucesso do MVP foram definidos e
validados. A revisão final foi concluída e as inconsistências de andamento
no README e no roadmap foram corrigidas e publicadas. O responsável aprovou
o encerramento da Etapa 1 em 20/10/2026. Os benefícios são pretendidos e o
atendimento aos critérios será verificado após a implementação. O ML integra
o escopo do MVP final, com desenvolvimento previsto na Etapa 8; ainda não foi
implementado. A Etapa 2 foi iniciada com autorização em 20/10/2026, com a
identificação dos atores e de suas responsabilidades. As definições dos
RF-01 a RF-13 foram aprovadas e publicadas. A organização da entrada foi
definida como uma área preparada por arquivo, com exatamente uma `Feature`,
conforme o detalhamento dos RF-01 e RF-02 abaixo. Permanecem pendentes a
definição do sistema de coordenadas adequado, da precisão e da tolerância
do cálculo da área. Para o RF-04, os cruzamentos iniciais estão definidos;
fontes definitivas, cobertura, preparação das bases e demais detalhamentos
continuam pendentes. Para o RF-05, as medidas descritivas e as condições dos
alertas informativos iniciais estão definidas; precisão, tolerâncias, alcance
de consulta e eventuais alertas adicionais permanecem pendentes. Para o RF-06,
a estrutura, o comportamento de avaliação e a primeira regra concreta RF06-R01
estão definidos. Essa regra simulada considera a ausência de superfície fora
da água no cenário de painéis solares em terreno, sem drenagem, aterro ou
estruturas sobre a água. As demais regras, os critérios de disponibilidade,
as bases concretas e os detalhamentos técnicos continuam pendentes.
Para o RF-07, nome e descrição do cenário obrigatórios, validações do
cadastro e da seleção e mensagens estão definidos. Três cenários de referência
estão aprovados: Revegetação com espécies nativas, Lazer e educação ambiental
e Solar em terreno. Descrições, referências e adaptações demonstrativas estão
registradas; condições de avaliação, dados, implementação e testes funcionais
continuam pendentes.
Para o RF-08, três critérios iniciais estão definidos: Declividade do terreno,
Proximidade de vias mapeadas e Proximidade de vegetação nativa remanescente,
com dados necessários, unidades, fontes e limitações. Cálculos e resumos,
critérios específicos adicionais, escalas, notas, limites, pesos e tratamento
detalhado de valores ausentes ainda precisam ser definidos. Para o RF-09, regras de normalização,
precisão, empates e valores ausentes também permanecem pendentes. Para o
RF-10, falta detalhar a apresentação; as previsões de ML serão incorporadas
na Etapa 8 e estarão presentes no dashboard do MVP final. Para o RF-11,
o modelo e as regras de armazenamento serão detalhados na Etapa 5. Para o
RF-12, formato e estrutura do relatório permanecem pendentes; as previsões
de ML integrarão o relatório do MVP final. O RF-13 formaliza a previsão
demonstrativa, com implementação, integração e testes na Etapa 8. Alvo,
atributos, treinamento, avaliação e conversão da previsão em entrada
multicritério permanecem pendentes. O RNF-01 foi aprovado e publicado; seu
checklist de clareza será aplicado após a implementação da interface e dos
fluxos correspondentes. O RNF-02 foi aprovado e publicado; a estrutura de
armazenamento e os metadados das bases concretas ainda serão detalhados, com
verificação funcional após a implementação. O RNF-03 foi aprovado e publicado;
stack, versões, conjuntos de referência e condições de reprodução ainda
precisam ser definidos antes
das verificações da aplicação. O RNF-04 foi aprovado e publicado; os detalhes
de recuperação e registro ainda precisam ser definidos, e os cenários de
falha serão testados após a implementação. O RNF-05 foi aprovado e publicado;
ambiente, dados demonstrativos, operações avaliadas e limites de tempo ainda
precisam ser definidos e aprovados antes das medições, que ocorrerão após
a implementação. O RNF-06 foi aprovado e publicado; arquitetura e convenções
específicas serão definidas e aprovadas na Etapa 4. A organização, os nomes
e a documentação do código serão revisados durante a implementação. A revisão
documental dos seis RNF foi concluída e apresentada ao responsável: não foram
encontradas contradições entre eles, mas os critérios ainda dependem dos
detalhamentos registrados. A lacuna sobre o registro explícito das licenças
das bases geográficas foi tratada na especificação do RT-01, aprovado e
publicado. O requisito define fontes, datas de obtenção, versões disponíveis,
licenças, limitações e indicação de informações indisponíveis. A estrutura de
armazenamento e os metadados das bases concretas ainda serão detalhados; sua
conferência ocorrerá na preparação dos dados e na implementação. A revisão
documental não comprova o atendimento dos requisitos pela aplicação. O RT-02
foi aprovado e publicado, especificando referências espaciais e unidades
adequadas, compatibilização quando necessária e bloqueio de cálculos cuja
referência não possa ser validada. Sistemas concretos, procedimentos de
compatibilização, unidades de distância, precisão e tolerâncias ainda precisam
ser definidos e aprovados antes da implementação e da preparação dos testes.
A RN-01 foi aprovada e publicada, formalizando a preservação das restrições
eliminatórias diante de pontuações altas e previsões favoráveis de ML, com
identificação da regra e da justificativa. A primeira regra concreta RF06-R01
está definida no RF-06; as demais condições e os parâmetros das regras
demonstrativas continuam pendentes. A verificação ocorrerá na implementação
dos RF-06 e RF-09 e, para o cenário com previsão, após a integração da Etapa 8.
A RN-02 foi aprovada e publicada, exigindo a identificação das informações
simuladas na análise, no dashboard e no relatório, incluindo o treinamento
sintético após a integração do ML. A forma de apresentação permanece
pendente; a regra será verificada durante a implementação e, para o ML,
após sua integração na Etapa 8. A RN-03 foi aprovada e publicada, distinguindo
a indisponibilidade dos dados necessários da ausência identificada em uma
análise válida, limitada aos dados analisados. Critérios de disponibilidade
e forma de apresentação continuam pendentes; os cenários serão testados
durante a implementação da análise e do dashboard. A revisão documental dos
dois RT e das três RN foi concluída e apresentada ao responsável, com 19
cenários de aceitação e prioridade essencial nos cinco itens. Não foram
encontradas contradições entre suas definições. O refinamento da classificação
da RN-01 foi aprovado e publicado: com os dados necessários disponíveis,
somente alternativas sem restrição identificada integram o ranking; as
restritas aparecem separadamente, com regra e justificativa. Se todas
estiverem restritas, o resultado informa que nenhuma é elegível segundo as
regras demonstrativas, sem classificação de alternativas elegíveis. A RN-01
agora possui cinco cenários de aceitação. O refinamento da RN-03 também foi
aprovado e publicado, com seis cenários: falta de dado necessário para avaliar
restrições ou calcular a comparação bloqueia o ranking; resultados parciais
válidos são preservados com a indisponibilidade e o bloqueio identificados
no dashboard e no relatório. Dados ausentes não são substituídos
automaticamente por zero nem tratados como ausência de ocorrência. A lista
dos dados necessários, os critérios de disponibilidade e a apresentação
continuam pendentes. A referência da RN-01 ao tratamento da indisponibilidade
foi sincronizada com a RN-03 e publicada, preservando a classificação e os
critérios de aceitação das regras. O levantamento das pendências para concluir
a Etapa 2 foi apresentado ao responsável e organizado em seis blocos de
decisões, com sequência proposta e identificação dos detalhamentos previstos
para etapas posteriores. As decisões abertas continuam pendentes de aprovação;
a Etapa 2 não foi encerrada. O formato inicial do RF-01 foi definido como
GeoJSON com extensão `.geojson` e publicado, com conferência da extensão e
do conteúdo e quatro critérios específicos acrescentados aos cinco existentes.
A estrutura inicial também foi aprovada e publicada: `FeatureCollection`
com `features` não vazio e composto somente por objetos `Feature`, cada um
com geometria não nula e `properties` como objeto ou `null`. Cinco critérios
estruturais foram acrescentados, totalizando 14 naquele momento. Os tipos
de geometria `Polygon` e `MultiPolygon` também foram aprovados e publicados
no commit `a08f135`, após esclarecimento visual ao responsável. Pontos,
linhas e `GeometryCollection`, mesmo contendo somente polígonos, serão
rejeitados. Quatro cenários foram acrescentados, totalizando 18 naquele
momento. As regras de validade das geometrias também foram aprovadas e
publicadas no commit `fa0601c`, com nove cenários adicionais, totalizando
27 naquele momento. A entrada deverá ter coordenadas finitas em WGS 84, longitude
e latitude com altitude opcional, anéis fechados e geometria válida em duas
dimensões. Foram especificados cruzamentos, recortes internos, relações
entre partes de um `MultiPolygon` e aceitação do sentido de percurso
invertido quando as demais condições forem atendidas. Falhas rejeitam o
arquivo e bloqueiam a análise, sem correção automática da geometria. A
altitude não participa dos cálculos em duas dimensões; a referência de
entrada não substitui a definição do sistema adequado aos cálculos do
RF-03 e do RT-02. Os limites de entrada também foram aprovados e publicados
no commit `a8a1b48`: até 1 MiB (1.048.576 bytes) e 20.000 posições por arquivo,
contando todas as partes e anéis, inclusive os fechamentos. Os limites são
inclusivos e simultâneos; exceder qualquer um rejeita o arquivo inteiro e
bloqueia a análise, com mensagem compreensível e sem simplificação ou remoção
automática de posições. Seis cenários foram acrescentados, totalizando 33 no
RF-01 naquele momento. São limites iniciais de escopo, apoiados em comparação
exploratória de arquivos reais, sem comprovar capacidade máxima ou desempenho da aplicação.
As bases ambientais serão preparadas separadamente. A infraestrutura será
avaliada na Etapa 4, e o desempenho seguirá o RNF-05. A opção 1 para o
tratamento de partes e registros também foi aprovada e publicada no commit
`3eede04`: o engenheiro deverá preparar uma única área antes do envio, com
exatamente uma `Feature`. Um `MultiPolygon` poderá reunir várias partes
válidas para análise conjunta. Duas ou mais `Feature` serão rejeitadas,
mesmo se representarem partes da mesma mina; o sistema orientará a preparação
da área, sem escolher o primeiro registro nem unir registros automaticamente.
A quantidade de registros não comprova a identidade da mina. Estudos
independentes utilizarão arquivos separados, em análises distintas. Três
cenários foram acrescentados ao RF-01, totalizando 36, e dois ao RF-02,
totalizando cinco. As demais regras e limites de entrada foram preservados.
A validação e a identificação da área ainda não foram implementadas nem
testadas funcionalmente.

Os cruzamentos iniciais do RF-04 foram aprovados e publicados no commit
`21c5430`: unidades de conservação, incluindo RPPN, rios e trechos de drenagem
e massas d’água. O sistema deverá considerar todas as partes e os recortes
internos da área, identificar elementos, camadas e fontes e distinguir
sobreposição de superfície de contato somente na borda ou em um ponto.
Ausência de ocorrência exige cruzamento válido e fica limitada à camada e
à cobertura analisadas; camada ausente, inválida ou incompleta deverá ser
identificada como indisponível, conforme o tratamento da RN-03. Seis cenários
foram acrescentados, totalizando dez no RF-04, com os quatro anteriores
preservados. Naquele registro, as medidas e os alertas ainda estavam pendentes
no RF-05, e as regras de restrição, no RF-06. Terreno e declividade permanecem no planejamento.
Fontes definitivas, metadados e preparação dos dados serão detalhados na
Etapa 6. A funcionalidade e seus testes ainda não foram implementados nem
executados, respectivamente.

As medidas descritivas iniciais do RF-05 também foram aprovadas e publicadas
no commit `d651b17`: área de interseção em m² e hectares, percentual sobre a
área total e menor distância geométrica em metros, considerando todas as
partes e recortes. Totais por camada poligonal não duplicam superfícies
cobertas por várias feições, mantendo identificáveis as ocorrências individuais.
Contato somente na borda ou em um ponto mantém a identificação, com área
comum e distância zero. Fonte, camada, cobertura, referência, unidades e
parâmetros deverão ser consultáveis. Cobertura insuficiente não permite
distância conclusiva, e ausência de elemento em uma consulta válida não gera
distância numérica. O tratamento da indisponibilidade segue a RN-03.
O estudo de Servou e colaboradores (2023) e as referências técnicas foram
registrados no RF-05. O uso de um resumo da área inteira foi identificado
como adaptação descritiva do MVP; não reproduz diretamente o estudo em células
nem valida notas, pesos ou parâmetros ambientais locais. Sete critérios foram
acrescentados, totalizando 12 naquele momento, com os cinco anteriores
preservados. Os exemplos numéricos são didáticos. A funcionalidade ainda não
foi implementada nem testada; a Etapa 2 permanece em andamento.

As condições dos alertas informativos iniciais do RF-05 foram aprovadas e
publicadas no commit `a0e1b77`: mensagens de sobreposição de superfície,
contato somente na borda ou em um ponto, interseção com drenagem, cruzamento
válido sem ocorrência e impossibilidade de concluir uma avaliação por dados
insuficientes ou inválidos ou falha no processamento. Camada, fonte e condições
da análise deverão ser consultáveis. As mensagens descrevem resultados ou
limitações; não classificam por si só risco, aptidão, segurança ou restrição.
Resultados parciais válidos serão preservados quando outra avaliação falhar;
o ranking será bloqueado quando faltar dado necessário para avaliar restrições
ou calcular a comparação, conforme a RN-03. Seis critérios foram acrescentados,
totalizando 18 no RF-05, com os 12 anteriores preservados. A fundamentação
registrada foi mantida. Referência espacial concreta, precisão, tolerâncias,
alcance de consulta e eventuais alertas adicionais continuam pendentes;
faixas numéricas adicionais exigirão fundamentação específica e aprovação.
A definição documental não implementa a funcionalidade nem executa os testes.

A estrutura, a fundamentação e o comportamento de avaliação das regras do
RF-06 foram aprovados em 21/10/2026 e publicados no commit `4b2d350`.
Cada regra deverá identificar nome, versão, alternativa avaliada, condição,
dados necessários, parâmetros e unidades aplicáveis, fonte, adaptação,
limitações, efeito e justificativa do resultado. A referência ao guia do
IBRAM apoia a fundamentação, sem fornecer limites universais ou validar
condições ambientais locais. Hipóteses simuladas terão origem e caráter
demonstrativo identificados. A avaliação apresentará restrição identificada,
restrição não identificada segundo aquela regra ou avaliação indisponível.
Regras incompletas não serão aplicadas como válidas. A falta de dados seguirá
a RN-03, preservando resultados parciais válidos e bloqueando o ranking quando
faltar dado necessário para avaliar restrições ou calcular a comparação.
A preservação das restrições seguirá a RN-01. Seis critérios foram
acrescentados, totalizando 11 no RF-06 naquele momento, com os cinco anteriores
preservados. Naquele registro, as condições concretas e seus dados e parâmetros
ainda estavam pendentes; a primeira regra foi detalhada posteriormente abaixo.

A primeira regra concreta RF06-R01, versão 0.1, foi aprovada em 21/10/2026 e
publicada no commit `77d763c`. É uma regra demonstrativa simulada para painéis
solares instalados em terreno fora da água, sem drenagem, aterro ou estruturas
sobre a água. Identificará restrição quando não restar superfície da área de
estudo fora da união das massas d’água mapeadas, considerando todas as partes
e recortes, sem duplicar sobreposições. Cobertura parcial ou contato somente
na borda não restringem toda a alternativa por essa regra; percentuais
arredondados não decidirão a cobertura total. Dados ausentes, inválidos ou
insuficientes, ou impossibilidade de concluir o cálculo, gerarão avaliação
indisponível, com tratamento conforme a RN-03. A restrição seguirá a RN-01.
O documento de triagem solar da EPA/NREL foi registrado com a distinção entre
a referência e a adaptação simulada do GeoVale. Não é uma proibição brasileira,
uma validação ambiental nem uma avaliação de soluções solares flutuantes.
Sete critérios foram acrescentados, totalizando 18, com os 11 anteriores
preservados. Somente a seção RF-06 foi alterada. A verificação foi documental;
a regra ainda não foi implementada nem testada funcionalmente. Seleção e
preparação da camada concreta na Etapa 6, adequação da cobertura, critérios
de disponibilidade, referência espacial, precisão e tolerâncias continuam
pendentes. Naquele registro, a definição das alternativas do RF-07 permanecia
aberta; os três cenários de referência foram detalhados posteriormente abaixo.
A Etapa 2 permanece em andamento.

Os campos e as validações do RF-07 foram aprovados em 21/10/2026 e publicados
no commit `a654a8b`. Cada alternativa deverá ter nome e descrição do cenário,
ambos textos obrigatórios. Campo ausente, vazio, somente com espaços ou de
outro tipo impedirá o cadastro, com mensagem que identifique o problema.
Nomes repetidos serão rejeitados, mesmo com descrições diferentes, sem
considerar diferenças de maiúsculas e minúsculas, espaços nas pontas ou
sequências de espaços. A seleção aceitará somente alternativas cadastradas
e exigirá pelo menos duas distintas; repetições da mesma opção não contarão
como alternativas diferentes. Os demais bloqueios, incluindo a RN-03,
continuam válidos. O exemplo de solar em terreno identifica o cenário da
RF06-R01 e não encerra a lista de usos do MVP. Seis critérios foram
acrescentados, totalizando 11, com os cinco anteriores preservados. Somente
a seção RF-07 foi alterada, com verificação documental e publicação conferidas.
Naquele registro, a lista de alternativas permanecia pendente; os três cenários
de referência foram detalhados posteriormente abaixo. O armazenamento, a
implementação e os testes funcionais continuam futuros.

Os três cenários de referência do MVP foram aprovados em 21/10/2026 e
publicados no commit `f0fa236`, somente na seção RF-07: Revegetação com espécies
nativas, Lazer e educação ambiental e Solar em terreno. Os nomes e descrições
foram registrados conforme os campos do cadastro. Revegetação considera
recuperar a cobertura vegetal das superfícies terrestres, com espécies
adequadas à região, a serem definidas posteriormente. Lazer considera um
parque de visitação terrestre, com trilhas, espaços de convivência e atividades
educativas. Solar corresponde ao cenário da RF06-R01, em terreno fora da água,
sem drenagem, aterro ou estruturas sobre a água. Cada cenário representa um
objetivo predominante; um parque também poderá ter vegetação. A comparação
será entre cenários para a mesma área de estudo, sem definir distribuição
automática de usos pelo terreno. O cadastro continuará permitindo outras
alternativas que atendam às validações. O estudo de Servou e colaboradores
(2023) e a triagem solar da EPA/NREL foram referenciados, distinguindo as
famílias de usos abordadas pelas fontes das adaptações demonstrativas do
GeoVale. O registro não comprova viabilidade local nem substitui avaliação
específica. As validações do cadastro e da seleção e os 11 critérios de
aceitação foram preservados integralmente. A conferência documental passou,
com publicação e sincronização verificadas. Condições de avaliação, espécies,
critérios, notas, pesos, demais restrições e dados necessários continuam
pendentes; cadastro e seleção ainda não foram implementados nem testados
funcionalmente. A Etapa 2 permanece em andamento.

Os três critérios iniciais do RF-08 foram aprovados em 21/10/2026 e publicados
no commit `c1fb652`: Declividade do terreno, Proximidade de vias mapeadas e
Proximidade de vegetação nativa remanescente. Declividade exigirá modelo digital
de elevação adequado e terá valores em graus; as proximidades exigirão camadas
de vias e de remanescentes de vegetação nativa, respectivamente, e distâncias
geométricas em metros. As referências de Servou e colaboradores (2023) e
Worden e colaboradores (2024) foram registradas, com seus contextos na Grécia
e na Austrália e as adaptações do GeoVale identificadas. As medidas não
representam por si só notas, restrições ou viabilidade dos usos; acesso
viário efetivo e conectividade ecológica exigem informações e análises
adicionais. A interpretação e a conversão em nota precisarão ser fundamentadas
para cada cenário. Fontes, unidades, adaptações e limitações deverão ser
consultáveis. A indisponibilidade seguirá a RN-03, sem substituir dados por
zero, preservando resultados parciais válidos e bloqueando o ranking quando
necessário; as restrições seguirão a RN-01. Os quatro critérios de aceitação
foram preservados integralmente. Somente a seção RF-08 foi alterada, com
conferência documental e publicação verificadas. Bases, novas camadas de vias
e vegetação, cruzamentos correspondentes no RF-04, cálculo e resumo da
declividade, alcance de consulta, referência espacial, precisão e tolerâncias
continuam pendentes. Critérios específicos de energia solar, como radiação e
rede elétrica, também exigirão detalhamento posterior. Nenhuma nota, peso ou
cálculo foi implementado; testes funcionais futuros e Etapa 2 em andamento.

## Entregas concluídas

- Organização inicial do projeto e orientações locais de desenvolvimento definidas.
- `.gitignore` criado, com exclusões para arquivos locais, ambientes virtuais,
  configurações de editor, caches e segredos.
- Git local inicializado com a branch `main`.
- Ambiente virtual existente verificado: Python 3.13.5 e pip 25.1.1.
- README inicial criado e seus comandos conferidos no ambiente local.
- Roadmap criado com as etapas 0 a 11 e os critérios de conclusão.
- Registro inicial de progresso criado neste arquivo.
- Roadmap sincronizado para registrar a criação e a verificação deste status.
- Quatro arquivos destinados ao versionamento revisados, sem alteração durante a revisão.
- Versionamento local iniciado, com conteúdo e escopo conferidos em cada commit.
- Repositório público `Rafael-Inacio-Silva/Geo_Vale` criado vazio no GitHub.
- Remoto `origin` configurado no Git local.
- README atualizado e versionado com o link do repositório remoto.
- Primeiro push autorizado concluído, publicando os seis commits iniciais e
  os quatro arquivos públicos previstos.
- Branch local `main` vinculada à `origin/main` e sincronização conferida.
- Revisão final concluída, compreensão da estrutura confirmada e encerramento
  da Etapa 0 aprovado pelo responsável em 19/10/2026.
- Encerramento registrado no roadmap e publicado no commit `ae80969`.
- Encerramento da preparação registrado no status e publicado no commit `2607df6`.
- Etapa 1 iniciada com autorização; RNG-01 — Problema de negócio validado pelo
  responsável, documentado e publicado em `docs/REQUISITOS.md` no commit `cf9a0d3`.
- RNG-02 — Objetivo do sistema validado pelo responsável, documentado com seu
  resultado esperado e publicado no commit `e5a6794`, preservando o RNG-01.
- RNG-03 — Público-alvo validado pelo responsável, documentado com os grupos de
  usuários e o cenário de demonstração, e publicado no commit `4d82d0a`,
  preservando os requisitos anteriores.
- RNG-04 — Benefícios esperados validado pelo responsável, documentado e
  publicado no commit `d638bfe`; os quatro benefícios foram identificados como
  pretendidos, sem apresentar ganhos medidos ou resultados comprovados.
- RNG-05 — Escopo do MVP validado pelo responsável e publicado no commit
  `768de4d`, com sete capacidades previstas e o ML explicitamente incluído na
  versão final da demonstração, a ser desenvolvido na Etapa 8.
- RNG-06 — Limitações do MVP validado pelo responsável e publicado no commit
  `52ce5e5`, registrando cinco limitações relativas ao cenário, aos dados, às
  informações demonstrativas, ao ML e à responsabilidade pela decisão.
- RNG-07 — Critérios de sucesso do MVP validado pelo responsável e publicado no
  commit `f90218f`, com sete critérios e suas evidências esperadas. A comprovação
  de atendimento ocorrerá após a implementação; nenhum resultado foi antecipado.
- GeoVale incluído no README do perfil público, seguindo o padrão dos demais
  projetos e identificado como em desenvolvimento.
- Revisão final da Etapa 1 realizada por leitura: RNG-01 a RNG-07 conferidos
  com o roteiro original; requisitos de negócio coerentes, com ML no MVP final.
- README sincronizado no commit `1d8a926`: Etapa 1 em revisão final e ML
  integrado, testado e documentado na entrega final, ainda como escopo previsto.
- Roadmap sincronizado no commit `9888fcf`: sete requisitos aprovados e
  encerramento da Etapa 1 pendente naquele momento, sem antecipar as etapas seguintes.
- Revisão final e correções documentais registradas no status e publicadas
  no commit `0057554`.
- Encerramento da Etapa 1 aprovado pelo responsável em 20/10/2026 e registrado
  no status no commit `f73136d`; requisitos de negócio concluídos, sem iniciar
  a Etapa 2.
- Encerramento registrado também no roadmap no commit `00633ea` e no README
  no commit `100ea80`, com data e situação conferidas contra este status.
- Etapa 2 iniciada com autorização do responsável em 20/10/2026.
- AT-01 — Engenheiro/analista e AT-02 — Gestor aprovados e publicados em
  `docs/REQUISITOS.md` no commit `5eeb0ed`, com responsabilidades baseadas no
  RNG-03 e preservação integral dos sete requisitos de negócio.
- RF-01 — Envio e validação do arquivo geográfico aprovado e publicado no
  commit `50314a4`, com ator, origem, prioridade, descrição, cinco cenários de
  aceitação e dependências. Formatos, limites de entrada e regras de geometria
  permanecem pendentes; a funcionalidade ainda não foi implementada.
- RF-02 — Leitura do arquivo e identificação da área aprovado e publicado no
  commit `d125d07`, com ator, origem, prioridade, descrição e três cenários de
  aceitação. Depende do RF-01 e das regras ainda pendentes para arquivos com
  múltiplas áreas; a funcionalidade ainda não foi implementada.
- RF-03 — Cálculo da extensão do terreno aprovado e publicado no commit
  `e75fde6`, com ator, origem, prioridade, descrição e três cenários de
  aceitação. Prevê resultado em m² e hectares e conferência com uma área de
  referência. Sistema de coordenadas adequado, precisão e tolerância ainda
  pendentes; a funcionalidade ainda não foi implementada.
- RF-04 — Cruzamento com as bases geográficas aprovado e publicado no commit
  `8b9e763`, com ator, origem, prioridade, descrição e quatro cenários de
  aceitação. Prevê cruzamento com camadas públicas, identificação das fontes
  e mensagens para falhas ou indisponibilidade de dados. Bases e operações
  específicas ainda pendentes; a funcionalidade ainda não foi implementada.
- RF-05 — Identificação de distâncias, sobreposições e alertas aprovado e
  publicado no commit `c9574e4`, com ator, origem, prioridade, descrição e
  cinco cenários de aceitação. Prevê unidades, fontes, parâmetros e distinção
  entre ausência de ocorrência e indisponibilidade de dados. Medições,
  tolerâncias e condições dos alertas permanecem pendentes; a funcionalidade
  ainda não foi implementada.
- RF-06 — Aplicação de regras de negócio demonstrativas aprovado e publicado
  no commit `828f4ac`, com ator, origem, prioridade, descrição e cinco cenários
  de aceitação. Prevê justificativas, restrições eliminatórias separadas das
  pontuações e identificação das regras simuladas. Regras específicas,
  parâmetros e tratamento de dados ausentes permanecem pendentes; a
  funcionalidade ainda não foi implementada.
- RF-07 — Cadastro e seleção de alternativas de uso futuro aprovado e
  publicado no commit `f6c0ec4`, com ator, origem, prioridade, descrição e
  cinco cenários de aceitação. Prevê alternativas identificáveis e seleção de
  pelo menos duas alternativas distintas para iniciar a comparação. Naquele
  registro, campos e regras de validação do cadastro permaneciam pendentes;
  a funcionalidade ainda não foi implementada.
- RF-08 — Definição de critérios, notas e pesos aprovado e publicado no commit
  `4471b22`, com ator, origem, prioridade, descrição e quatro cenários de
  aceitação. Prevê consulta da configuração, associação de cada nota à
  alternativa e ao critério correspondentes e rejeição de valores inválidos.
  Escalas, limites, validação dos pesos e tratamento de valores ausentes
  permanecem pendentes; a funcionalidade ainda não foi implementada.
- RF-09 — Cálculo multicritério por soma ponderada aprovado e publicado no
  commit `4429780`, com ator, origem, prioridade, descrição e cinco cenários
  de aceitação. Prevê pontuações, classificação, identificação de notas e
  pesos utilizados e restrições eliminatórias separadas da pontuação.
  Normalização, precisão, empates e valores ausentes permanecem pendentes;
  a funcionalidade ainda não foi implementada.
- RF-10 — Apresentação dos resultados no dashboard aprovado e publicado no
  commit `87f58c7`, com dois atores, origem, prioridade, descrição e cinco
  cenários de aceitação. Prevê mapa, características, alertas, restrições,
  classificação, fontes, parâmetros e limitações, distinguindo informações
  reais, simuladas e indisponíveis. Detalhamento da apresentação pendente;
  previsões de ML incluídas no MVP final após a integração da Etapa 8.
  O dashboard ainda não foi implementado.
- RF-11 — Persistência e consulta das análises aprovado e publicado no commit
  `412158e`, com atores, origem, prioridade, descrição e cinco cenários de
  aceitação. Prevê identificar análises salvas e recuperar parâmetros e
  resultados preservados em uma nova sessão, informando falhas e análises
  não encontradas. Modelo e regras de armazenamento pendentes de definição
  na Etapa 5; persistência e consulta ainda não implementadas.
- RF-12 — Exportação de relatório aprovado e publicado no commit `734cddf`,
  com atores, origem, prioridade, descrição e cinco cenários de aceitação.
  Prevê identificação da área, alternativas, classificação, restrições,
  fontes, parâmetros, limitações, informações simuladas e tratamento de
  falhas. Formato e estrutura pendentes; previsões de ML incluídas no
  relatório do MVP final. A exportação ainda não foi implementada.
- RF-13 — Previsão demonstrativa de aptidão física por ML aprovado e publicado
  no commit `bfdb6be`, com atores, origem, prioridade e seis cenários de
  aceitação. Prevê integração à comparação, ao dashboard e ao relatório,
  origem do treinamento, limitações, testes reproduzíveis e preservação das
  restrições eliminatórias. Implementação prevista na Etapa 8, incluída no
  MVP final; alvo, atributos, treinamento, avaliação e conversão da previsão
  em entrada multicritério permanecem pendentes. O modelo não foi implementado.
- O escopo funcional atual possui 13 RF documentados, do RF-01 ao RF-13,
  sujeitos aos detalhamentos pendentes e à revisão da Etapa 2.
- RNF-01 — Clareza da interface e das mensagens aprovado e publicado no
  commit `28e9a94`, com origem, prioridade e três cenários de aceitação.
  Prevê textos em português, campos identificáveis e compreensão das ações,
  dos resultados e dos erros. Verificação futura por checklist em cenários
  válidos e de erro; a interface ainda não foi implementada.
- RNF-02 — Rastreabilidade da análise aprovado e publicado no commit `92a78bb`,
  com origem, prioridade e três cenários de aceitação. Prevê fontes, datas,
  versões disponíveis, parâmetros, limitações e informações simuladas, com
  correspondência entre análise, consulta e relatório. Metadados e
  armazenamento ainda pendentes; verificação funcional futura.
- RNF-03 — Execução e testes reproduzíveis aprovado e publicado no commit
  `72016e7`, com origem, prioridade e quatro cenários de aceitação. Prevê
  instalação e execução documentadas em ambiente limpo, identificação de
  versões, dados e parâmetros, repetição dos cenários conforme as tolerâncias
  e registro de resultados reais. Stack, versões, conjuntos de referência e
  condições de reprodução, incluindo o ML, ainda pendentes; verificações futuras.
- RNF-04 — Tratamento de falhas aprovado e publicado no commit `7b234b3`, com
  origem, prioridade e cinco cenários de aceitação. Prevê erros tratados de
  forma controlada, preservação das análises salvas, nova tentativa após
  correção e proteção de informações sensíveis nas mensagens e registros.
  Detalhes de recuperação e registro pendentes; verificações futuras.
- RNF-05 — Desempenho no cenário demonstrativo aprovado e publicado no commit
  `0d60a9c`, com origem, prioridade e quatro cenários de aceitação. Prevê
  medição das operações e do fluxo completo, registro do ambiente e do volume
  dos dados e comparação com limites aprovados. Ambiente, dados, operações
  avaliadas e limites de tempo pendentes; medições futuras.
- RNF-06 — Organização e manutenção do código aprovado e publicado no commit
  `e488333`, com origem, prioridade essencial e quatro cenários de aceitação.
  Prevê separação de responsabilidades, nomes descritivos, docstrings em todas
  as funções e classes e comentários relevantes em português. Arquitetura e
  convenções específicas pendentes na Etapa 4; revisões durante a implementação.
- Revisão documental dos RNF-01 a RNF-06 concluída e apresentada no chat, com
  conferência de cobertura, prioridades, 23 cenários de aceitação, pendências
  e momentos de verificação. Nenhuma contradição encontrada entre os seis
  requisitos; lacuna sobre o registro explícito das licenças identificada
  para detalhamento técnico. A revisão foi realizada sem alterar arquivos.
- RT-01 — Registro da origem e das condições de uso das bases geográficas
  aprovado e publicado no commit `cf710ab`, com origem, prioridade essencial
  e quatro cenários de aceitação. A exigência de registrar licenças agora
  está explícita no documento de requisitos, junto de fontes, datas de
  obtenção, versões disponíveis, limitações e metadados indisponíveis.
  Estrutura de armazenamento e metadados das bases concretas ainda pendentes;
  verificações futuras na preparação dos dados e na implementação.
- RT-02 — Sistemas de coordenadas e unidades dos cálculos geográficos aprovado
  e publicado no commit `bacc27f`, com origem, prioridade essencial e cinco
  cenários de aceitação. Prevê identificação das referências e unidades,
  compatibilização quando necessária, área em m² e hectares, bloqueio sem
  referência validada e comparação com valores de referência. Sistemas
  concretos, procedimentos, unidades de distância, precisão e tolerâncias
  pendentes; verificações futuras na preparação dos dados e na implementação.
- RN-01 — Restrições eliminatórias na comparação de alternativas aprovada e
  publicada no commit `645e4ea`, com origem, prioridade essencial e três
  cenários de aceitação. Formaliza a preservação das restrições diante de
  pontuação alta e previsão favorável de ML, mantendo regra e justificativa
  identificáveis. Condições e parâmetros demonstrativos ainda pendentes;
  testes futuros na implementação e após a integração do ML na Etapa 8.
- RN-02 — Identificação de informações simuladas aprovada e publicada no
  commit `fe12768`, com origem, prioridade essencial e quatro cenários de
  aceitação. Prevê identificação de dados, regras, notas, custos, benefícios
  e dados de treinamento simulados, com correspondência na análise, no
  dashboard e no relatório. Forma de apresentação ainda pendente; testes
  futuros durante a implementação e após a integração do ML na Etapa 8.
- RN-03 — Distinção entre indisponibilidade de dados e ausência de ocorrência
  aprovada e publicada no commit `a60e897`, com origem, prioridade essencial
  e três cenários de aceitação. Prevê ausência como resultado de análise
  válida limitada aos dados analisados, identificação da indisponibilidade
  e distinção das situações no dashboard. Critérios de disponibilidade e
  apresentação pendentes; testes futuros durante a implementação.
- Revisão documental dos RT-01 a RT-02 e das RN-01 a RN-03 concluída e
  apresentada no chat. Conferidos 19 cenários de aceitação, prioridades,
  dependências, pendências e momentos de verificação. Sem contradições
  encontradas entre as definições; confirmada a exigência explícita das
  licenças no RT-01. Identificados refinamentos sobre alternativas restritas
  na classificação e efeitos da indisponibilidade na comparação e no
  relatório. A revisão foi realizada sem alterar arquivos.
- Refinamento da classificação da RN-01 aprovado e publicado no commit
  `64979eb`. Para dados necessários disponíveis, define ranking somente de
  alternativas sem restrição identificada, apresentação separada das
  restritas e ausência de alternativas elegíveis quando todas estiverem
  restritas. Dois cenários acrescentados, totalizando cinco na RN-01; demais
  seções de requisitos preservadas. Condições, parâmetros e tratamento da
  indisponibilidade continuam pendentes; testes futuros na implementação.
- Refinamento dos efeitos da indisponibilidade na RN-03 aprovado e publicado
  no commit `37909e5`. Define bloqueio do ranking por falta de dado necessário
  à avaliação das restrições ou ao cálculo da comparação, preservação de
  resultados parciais válidos e identificação da indisponibilidade no
  dashboard e no relatório, sem substituição automática por zero. Três
  cenários acrescentados, totalizando seis na RN-03; demais seções preservadas.
  Lista de dados necessários, critérios, apresentação e sincronização da
  referência na RN-01 pendentes; testes futuros durante a implementação.
- Referência da RN-01 ao tratamento da indisponibilidade da RN-03 sincronizada
  e publicada no commit `301539a`. Alterado somente o parágrafo de dependências
  da RN-01, preservando a classificação, os critérios de aceitação e todas
  as demais seções. Lista dos dados necessários, critérios de disponibilidade
  e condições e parâmetros demonstrativos continuam pendentes.
- Levantamento das pendências de encerramento da Etapa 2 concluído e
  apresentado no chat: seis blocos de decisões de comportamento, distinção
  dos detalhamentos previstos para etapas posteriores e sequência proposta
  de pequenas entregas. Conferidos os 13 RF, seis RNF, dois RT e três RN,
  sem identificadores repetidos. Levantamento realizado sem alterar arquivos;
  cinco arquivos versionados preservados integralmente e Git limpo.
- Formato inicial GeoJSON com extensão `.geojson` aprovado para o RF-01 e
  publicado no commit `57b5e7d`, com referência à RFC 7946. Conferência da
  extensão e do conteúdo prevista; quatro critérios específicos acrescentados,
  totalizando nove no RF-01. Apenas essa seção foi alterada, com as demais
  preservadas. Estrutura, limites, geometrias e múltiplas áreas pendentes;
  testes funcionais futuros durante a implementação.
- Estrutura inicial `FeatureCollection` do RF-01 aprovada e publicada no
  commit `0d8835e`, com lista `features` não vazia, itens `Feature`, geometria
  não nula e `properties` como objeto ou `null`. Cinco critérios estruturais
  acrescentados, totalizando 14 no RF-01; demais seções preservadas. Aprovação
  estrutural permite seguir às demais validações. Geometrias, limites e
  tratamento de múltiplas áreas pendentes; testes funcionais futuros.
- Tipos de geometria `Polygon` e `MultiPolygon` aprovados para a área de estudo
  no RF-01 e publicados no commit `a08f135`. Pontos, linhas e
  `GeometryCollection`, mesmo contendo somente polígonos, serão rejeitados.
  Quatro cenários acrescentados, totalizando 18; alterada somente a seção
  RF-01, com as demais seções e arquivos preservados. Regras adicionais de
  validade, limites e tratamento de múltiplas áreas ou `Feature` continuam
  pendentes; a validação ainda não foi implementada nem testada funcionalmente.
- Regras de validade das geometrias do RF-01 aprovadas e publicadas no commit
  `fa0601c`: coordenadas, anéis fechados, cruzamentos, recortes internos e
  relações entre partes de um `MultiPolygon`, com altitude opcional fora dos
  cálculos em duas dimensões e sem rejeição somente pelo sentido de percurso.
  Nove cenários acrescentados, totalizando 27; somente a seção RF-01 foi
  alterada, com os 18 cenários anteriores, demais seções e arquivos preservados.
  Erros bloqueiam a análise, sem correção automática. Limites e tratamento de
  múltiplas áreas ou `Feature` permanecem pendentes; testes funcionais futuros.
- Limites iniciais do RF-01 aprovados e publicados no commit `a8a1b48`: até
  1 MiB (1.048.576 bytes) e 20.000 posições por arquivo, incluindo todos os
  anéis, partes e fechamentos. Limites inclusivos; exceder qualquer um rejeita
  o arquivo e bloqueia a análise, sem simplificação automática. Seis cenários
  acrescentados, totalizando 33, com os 27 anteriores preservados. Somente o
  RF-01 foi alterado; múltiplas áreas ou `Feature` continuam pendentes.
- Comparação exploratória local de três arquivos reais apresentada ao
  responsável para apoiar a decisão: Águas Claras, 11.017 bytes e 410 posições;
  extração mapeada em Itabira, 3.099 bytes e 103 posições; APA Sul RMBH,
  312.924 bytes e 11.231 posições, somente como teste auxiliar de volume,
  não minerário. As posições incluem o fechamento. Fontes OpenStreetMap
  (ODbL 1.0) e IDE-Sisema (CC BY 4.0 para essa camada), sem simplificar os
  contornos. A comparação não seleciona a região final, não comprova o fluxo
  da aplicação nem encerra a preparação de dados da Etapa 6. Arquivos e
  relatórios exploratórios permanecem locais, fora do repositório.
- Opção 1 — uma área preparada por arquivo — aprovada e publicada nos RF-01
  e RF-02 no commit `3eede04`. Exige exatamente uma `Feature`, com `Polygon`
  ou `MultiPolygon` válido. Todas as partes de um `MultiPolygon` compõem uma
  única área para análise conjunta. Arquivos com várias `Feature` serão
  rejeitados, mesmo representando a mesma mina, com orientação compreensível
  e sem seleção ou união automática. Estudos independentes exigem arquivos
  separados, em análises distintas. Três critérios acrescentados ao RF-01
  (36 no total) e dois ao RF-02 (cinco no total); os anteriores e os limites
  preservados. Alteradas somente essas duas seções de `docs/REQUISITOS.md`.
  Funcionalidades e testes da aplicação permanecem futuros.
- Cruzamentos iniciais do RF-04 aprovados e publicados no commit `21c5430`:
  unidades de conservação, incluindo RPPN, rios e trechos de drenagem e massas
  d’água. Especificadas interseções com a geometria completa, identificação
  de elementos, camadas e fontes, distinção entre contato e sobreposição e
  entre ausência de ocorrência e indisponibilidade. Seis critérios acrescentados,
  totalizando dez; quatro anteriores preservados. Somente a seção RF-04 foi
  alterada. Fontes definitivas, preparação das bases, medidas, alertas, regras
  demonstrativas e testes funcionais continuam pendentes nas unidades e etapas
  correspondentes; terreno e declividade preservados no planejamento.
- Medidas descritivas iniciais do RF-05 aprovadas e publicadas no commit
  `d651b17`, com referências e limitações: interseção em m², hectares e
  percentual sobre a área total; consolidação por camada sem duplicar
  superfícies; menor distância geométrica em metros; identificação de contato,
  fontes, cobertura e condições das medidas. Sete critérios acrescentados,
  totalizando 12, preservando os cinco anteriores. Somente a seção RF-05 foi
  alterada. Adaptação ao MVP distinguida da metodologia do estudo citado;
  notas, pesos, alertas e restrições permanecem para unidades próprias.
  Conferência documental concluída; testes funcionais ainda não executados.
- Alertas informativos iniciais do RF-05 aprovados e publicados no commit
  `a0e1b77`, com condições e exemplos de mensagens para sobreposição, contato,
  interseção com drenagem, ausência após cruzamento válido e avaliação não
  concluída. Preservação dos resultados parciais e bloqueio do ranking conforme
  a RN-03 explicitados. Seis critérios acrescentados, totalizando 18; os 12
  anteriores e a fundamentação preservados. Somente a seção RF-05 foi alterada.
  Precisão, tolerâncias, alcance de consulta e eventuais alertas adicionais
  permanecem pendentes. Verificação documental concluída; testes funcionais
  futuros na implementação.
- Estrutura e avaliação das regras do RF-06 aprovadas em 21/10/2026 e publicadas
  no commit `4b2d350`, com identificação, finalidade, condição, fundamentação,
  efeito e justificativa; três resultados possíveis e tratamento de regras
  incompletas e dados ausentes. Referência do IBRAM incluída com seu alcance
  explicitado; simulações identificadas e restrições preservadas conforme as
  RN-01 e RN-03. Seis critérios acrescentados, totalizando 11, com os cinco
  anteriores e demais seções preservados. Somente RF-06 foi alterado.
  Naquele registro, condições concretas e parâmetros permaneciam pendentes;
  aplicação ainda não implementada nem testada funcionalmente.
- Primeira regra concreta RF06-R01, versão 0.1, aprovada em 21/10/2026 e publicada
  no commit `77d763c`: ausência de superfície fora das massas d’água mapeadas
  para o cenário demonstrativo de painéis solares em terreno, sem drenagem,
  aterro ou estruturas sobre a água. Fonte EPA/NREL, adaptação simulada,
  limitações, dados necessários, unidades e justificativa documentados.
  Sete critérios acrescentados, totalizando 18; os 11 anteriores preservados.
  Somente RF-06 alterado, com conferência documental e publicação confirmadas.
  Bases concretas, disponibilidade, cobertura, referência espacial, precisão
  e tolerâncias ainda pendentes; implementação e testes funcionais futuros.
- Campos e validações do RF-07 aprovados em 21/10/2026 e publicados no commit
  `a654a8b`: nome e descrição do cenário como textos obrigatórios, mensagens
  para entradas inválidas, rejeição de nomes repetidos desconsiderando caixa
  e espaços, seleção somente de alternativas cadastradas e mínimo de duas
  distintas, sem contar repetições da mesma opção. Demais bloqueios mantidos.
  Seis critérios acrescentados, totalizando 11; os cinco anteriores e todas
  as demais seções preservados. Somente RF-07 alterado, com verificação
  documental e publicação confirmadas. Naquele registro, a lista de alternativas
  permanecia pendente; armazenamento, implementação e testes funcionais futuros.
- Três cenários de referência do MVP aprovados em 21/10/2026 e publicados no
  commit `f0fa236`: Revegetação com espécies nativas, Lazer e educação ambiental
  e Solar em terreno, com nomes e descrições, referências de Servou e
  colaboradores (2023) e EPA/NREL, adaptações demonstrativas e limitações.
  Cadastro aberto a outras alternativas válidas e correspondência do cenário
  solar com a RF06-R01 explicitados. Validações e 11 critérios de aceitação
  preservados integralmente. Somente RF-07 alterado; conferência documental
  concluída e publicação confirmada. Condições de avaliação e demais parâmetros
  continuam pendentes; implementação e testes funcionais futuros.
- Três critérios iniciais de comparação do RF-08 aprovados em 21/10/2026 e
  publicados no commit `c1fb652`: Declividade do terreno, Proximidade de vias
  mapeadas e Proximidade de vegetação nativa remanescente. Dados necessários,
  unidades em graus ou metros, referências de Servou e colaboradores (2023)
  e Worden e colaboradores (2024), adaptações e limitações documentados.
  Medidas, notas e restrições separadas; RN-01 e RN-03 preservadas. Os quatro
  critérios de aceitação anteriores foram mantidos integralmente. Somente
  RF-08 alterado; conferência documental concluída e publicação confirmada.
  Dados concretos, procedimentos de cálculo, critérios adicionais, escalas,
  notas e pesos continuam pendentes; implementação e testes funcionais futuros.

## Arquivos relevantes

| Arquivo | Finalidade |
| --- | --- |
| `.gitignore` | Definir exclusões do versionamento. |
| `README.md` | Apresentar objetivo, escopo planejado, limitações e ambiente atual. |
| `docs/ROADMAP.md` | Organizar etapas, entregas e critérios de conclusão. |
| `docs/STATUS.md` | Registrar progresso real, verificações e pendências. |
| `docs/REQUISITOS.md` | Registrar os RNG-01 a RNG-07, os atores AT-01 e AT-02 e as definições dos RF-01 a RF-13, dos RNF-01 a RNF-06, dos RT-01 a RT-02 e das RN-01 a RN-03 aprovados; detalhamento técnico e demais requisitos serão tratados em unidades posteriores. |

Os caminhos são relativos à raiz do projeto. O documento de requisitos está
em elaboração incremental; arquitetura e decisões ainda não possuem documentos
próprios e serão tratadas nas etapas correspondentes. Os arquivos locais
excluídos permanecem fora do versionamento.

## Estado do Git

- Branch atual: `main`.
- Histórico anterior a esta entrega: cento e dezesseis commits locais já publicados, listados abaixo.
- Repositório público: [Rafael-Inacio-Silva/Geo_Vale](https://github.com/Rafael-Inacio-Silva/Geo_Vale).
- Remoto `origin`: `https://github.com/Rafael-Inacio-Silva/Geo_Vale.git`.
- O repositório foi criado vazio e recebeu o histórico no primeiro push.
- Marco do primeiro envio: `ac71da7`, confirmado na branch remota `main`.
- A branch local acompanha `origin/main`; a sincronização foi verificada após o envio.
- Arquivos públicos versionados: `.gitignore`, `README.md`, `docs/ROADMAP.md`,
  `docs/STATUS.md` e `docs/REQUISITOS.md`.
- Primeiro envio ao GitHub realizado; nenhuma implantação da aplicação efetuada.

Commits concluídos antes desta atualização:

| Commit | Mensagem |
| --- | --- |
| `93570f9` | `chore: configura exclusões do versionamento` |
| `de3b305` | `docs: adiciona apresentação inicial do GeoVale` |
| `674d73a` | `docs: adiciona roadmap de desenvolvimento` |
| `14175fe` | `docs: registra estado inicial do projeto` |
| `15e11d0` | `docs: documenta repositório remoto` |
| `ac71da7` | `docs: atualiza status da integração com GitHub` |
| `90f572f` | `docs: registra primeiro envio ao GitHub` |
| `ae80969` | `docs: registra encerramento da preparação no roadmap` |
| `2607df6` | `docs: registra encerramento da preparação no status` |
| `cf9a0d3` | `docs: registra problema de negócio do GeoVale` |
| `d67257c` | `docs: registra início dos requisitos de negócio` |
| `e5a6794` | `docs: registra objetivo do GeoVale` |
| `3714069` | `docs: registra progresso dos requisitos de negócio` |
| `4d82d0a` | `docs: registra público-alvo do GeoVale` |
| `f4e5963` | `docs: registra conclusão do público-alvo no status` |
| `d638bfe` | `docs: registra benefícios esperados do GeoVale` |
| `2f5ac0f` | `docs: registra conclusão dos benefícios no status` |
| `768de4d` | `docs: registra escopo do MVP GeoVale` |
| `6027cda` | `docs: registra conclusão do escopo no status` |
| `52ce5e5` | `docs: registra limitações do MVP GeoVale` |
| `00ce0f2` | `docs: registra conclusão das limitações no status` |
| `f90218f` | `docs: registra critérios de sucesso do MVP` |
| `70e09eb` | `docs: registra conclusão dos critérios de sucesso no status` |
| `1d8a926` | `docs: sincroniza apresentação com requisitos de negócio` |
| `9888fcf` | `docs: sincroniza roadmap com requisitos de negócio` |
| `0057554` | `docs: registra revisão final dos requisitos de negócio` |
| `f73136d` | `docs: registra encerramento dos requisitos de negócio` |
| `00633ea` | `docs: registra encerramento da etapa 1 no roadmap` |
| `100ea80` | `docs: registra encerramento da etapa 1 no README` |
| `5ca1290` | `docs: consolida registros de encerramento da etapa 1` |
| `5eeb0ed` | `docs: identifica atores e responsabilidades do GeoVale` |
| `c279da9` | `docs: registra início da etapa 2 e atores no status` |
| `50314a4` | `docs: especifica envio e validação do arquivo geográfico` |
| `2d9ff6a` | `docs: registra definição e pendências do RF-01 no status` |
| `d125d07` | `docs: especifica leitura do arquivo e identificação da área` |
| `fa3e0f5` | `docs: registra definição e pendências do RF-02 no status` |
| `e75fde6` | `docs: especifica cálculo da extensão do terreno` |
| `eb32bc4` | `docs: registra definição e pendências do RF-03 no status` |
| `8b9e763` | `docs: especifica cruzamento com as bases geográficas` |
| `bfa80cc` | `docs: registra definição e pendências do RF-04 no status` |
| `c9574e4` | `docs: especifica distâncias, sobreposições e alertas` |
| `a2ddb4b` | `docs: registra definição e pendências do RF-05 no status` |
| `828f4ac` | `docs: especifica aplicação de regras de negócio demonstrativas` |
| `a43dc48` | `docs: registra definição e pendências do RF-06 no status` |
| `f6c0ec4` | `docs: especifica cadastro e seleção de alternativas de uso futuro` |
| `d613513` | `docs: registra definição e pendências do RF-07 no status` |
| `4471b22` | `docs: especifica definição de critérios, notas e pesos` |
| `47bec1e` | `docs: registra definição e pendências do RF-08 no status` |
| `4429780` | `docs: especifica cálculo multicritério por soma ponderada` |
| `7c07d97` | `docs: registra definição e pendências do RF-09 no status` |
| `87f58c7` | `docs: especifica apresentação dos resultados no dashboard` |
| `46e18ab` | `docs: registra definição e pendências do RF-10 no status` |
| `412158e` | `docs: especifica persistência e consulta das análises` |
| `7d3715f` | `docs: registra definição e pendências do RF-11 no status` |
| `734cddf` | `docs: especifica exportação de relatório` |
| `ec19ef6` | `docs: registra definição e pendências do RF-12 no status` |
| `bfdb6be` | `docs: especifica previsão demonstrativa de aptidão física por ML` |
| `969e571` | `docs: registra definição e pendências do RF-13 no status` |
| `28e9a94` | `docs: especifica clareza da interface e das mensagens` |
| `583e3d1` | `docs: registra definição e verificação futura do RNF-01 no status` |
| `92a78bb` | `docs: especifica rastreabilidade da análise` |
| `6cd2663` | `docs: registra definição e verificação futura do RNF-02 no status` |
| `72016e7` | `docs: especifica execução e testes reproduzíveis` |
| `6d84e38` | `docs: registra definição e verificação futura do RNF-03 no status` |
| `7b234b3` | `docs: especifica tratamento de falhas` |
| `f0e50a7` | `docs: registra definição e verificação futura do RNF-04 no status` |
| `0d60a9c` | `docs: especifica desempenho no cenário demonstrativo` |
| `8659167` | `docs: registra definição e medições futuras do RNF-05 no status` |
| `e488333` | `docs: especifica organização e manutenção do código` |
| `51870cd` | `docs: registra definição e revisão futura do RNF-06 no status` |
| `908e49f` | `docs: registra revisão dos requisitos não funcionais no status` |
| `cf710ab` | `docs: especifica origem e condições de uso das bases geográficas` |
| `58b6253` | `docs: registra definição e verificação futura do RT-01 no status` |
| `bacc27f` | `docs: especifica referências espaciais e unidades dos cálculos` |
| `2f686fa` | `docs: registra definição e verificação futura do RT-02 no status` |
| `645e4ea` | `docs: especifica restrições eliminatórias na comparação` |
| `073b158` | `docs: registra definição e verificação futura da RN-01 no status` |
| `fe12768` | `docs: especifica identificação de informações simuladas` |
| `07dd5c3` | `docs: registra definição e verificação futura da RN-02 no status` |
| `a60e897` | `docs: distingue dados indisponíveis de ausência de ocorrência` |
| `cc15488` | `docs: registra definição e verificação futura da RN-03 no status` |
| `2f1ded1` | `docs: registra revisão dos requisitos técnicos e regras de negócio no status` |
| `64979eb` | `docs: detalha classificação das alternativas com restrição` |
| `6efd4c6` | `docs: registra detalhamento da classificação na RN-01 no status` |
| `37909e5` | `docs: detalha efeitos de dados indisponíveis na comparação e no relatório` |
| `bb3adcb` | `docs: registra detalhamento da indisponibilidade na RN-03 no status` |
| `301539a` | `docs: sincroniza referência da RN-01 ao tratamento da RN-03` |
| `d1d5d35` | `docs: registra sincronização entre RN-01 e RN-03 no status` |
| `3ea2a0e` | `docs: organiza pendências para concluir a etapa 2 no status` |
| `57b5e7d` | `docs: define GeoJSON como formato inicial de entrada` |
| `a356874` | `docs: registra formato GeoJSON do RF-01 no status` |
| `0d8835e` | `docs: define estrutura FeatureCollection para entrada` |
| `e831032` | `docs: registra estrutura FeatureCollection do RF-01 no status` |
| `a08f135` | `docs: define tipos de geometria aceitos no RF-01` |
| `4164f56` | `docs: registra tipos de geometria do RF-01 no status` |
| `fa0601c` | `docs: especifica validade das geometrias no RF-01` |
| `9854ec2` | `docs: registra validade das geometrias do RF-01 no status` |
| `a8a1b48` | `docs: define limites de entrada do RF-01` |
| `4f59a1a` | `docs: registra limites de entrada do RF-01 no status` |
| `3eede04` | `docs: define área única por arquivo nos RF-01 e RF-02` |
| `c7ae111` | `docs: registra área única dos RF-01 e RF-02 no status` |
| `21c5430` | `docs: detalha cruzamentos iniciais do RF-04` |
| `8a7631f` | `docs: registra cruzamentos iniciais do RF-04 no status` |
| `d651b17` | `docs: fundamenta medidas descritivas do RF-05` |
| `2121f9b` | `docs: registra medidas descritivas do RF-05 no status` |
| `a0e1b77` | `docs: define alertas informativos iniciais do RF-05` |
| `3725063` | `docs: registra alertas informativos do RF-05 no status` |
| `4b2d350` | `docs: define estrutura e avaliação das regras do RF-06` |
| `195d32b` | `docs: registra estrutura das regras do RF-06 no status` |
| `77d763c` | `docs: define primeira regra demonstrativa solar do RF-06` |
| `b23a073` | `docs: registra primeira regra demonstrativa do RF-06 no status` |
| `a654a8b` | `docs: define campos e validações do cadastro do RF-07` |
| `d90890e` | `docs: registra campos e validações do RF-07 no status` |
| `f0fa236` | `docs: define cenários de referência do MVP no RF-07` |
| `711114d` | `docs: registra cenários de referência do RF-07 no status` |
| `c1fb652` | `docs: define critérios iniciais de comparação do RF-08` |

Esta atualização do status tem a mensagem de commit
`docs: registra critérios iniciais do RF-08 no status`. Consulte `git log --oneline` para
identificar seu hash e o histórico atualizado, sem depender de contagens fixas
neste documento.

## Verificações realizadas

As verificações abaixo foram executadas durante a preparação, a documentação
e a revisão dos requisitos entre 19/10/2026 e 21/10/2026.
São verificações de configuração e documentação e ensaios exploratórios
locais com dados reais; não são testes da aplicação.

| Verificação | Resultado observado |
| --- | --- |
| Exclusões do `.gitignore` em repositório temporário | 35 cenários de exclusão e 16 cenários permitidos passaram; repositório temporário removido. |
| Inicialização do Git | Sete checagens passaram: raiz, branch, ausência de commits, índice vazio, ausência de remoto, estado dos arquivos e exclusões locais. |
| Interpretador Python | Python 3.13.5 usando a `.venv` do projeto; ambiente virtual confirmado e operação simples executada com sucesso. |
| Pacotes instalados | Somente pip 25.1.1; as consultas da preparação confirmaram esse estado. |
| Integridade das dependências | `python -m pip check` retornou `No broken requirements found.` |
| README | Estrutura Markdown conferida e comandos documentados executados com sucesso. |
| Roadmap | Nomes e ordem das 12 etapas e das 12 subetapas funcionais conferidos com o roteiro original; todas as etapas possuem entrega e critério de conclusão. Criação do status registrada como concluída. |
| Revisão dos quatro arquivos para versionamento | Formatação e arquivos disponíveis no Git conferidos; não foram identificados credenciais, e-mails ou caminhos pessoais na leitura e na busca de padrões. Exclusões locais confirmadas e status atualizado. |
| Três commits iniciais | Mensagem, conteúdo e arquivo incluído conferidos em cada commit; demais arquivos preservados e instruções locais mantidas fora do histórico. |
| Versionamento do status e atualização do README | Commits `14175fe` e `15e11d0` conferidos: um arquivo por commit e área de trabalho limpa ao concluir cada unidade. |
| Integração inicial com GitHub | Na criação, proprietário, nome, visibilidade pública e repositório vazio confirmados pela consulta ao GitHub; endereço de leitura e envio do origin conferido no Git local. |
| Primeiro envio ao GitHub | `git push -u origin main` concluído; seis commits e quatro arquivos publicados. SHA local e remoto iguais a `ac71da7`, upstream configurado, diferença de commits igual a zero e área de trabalho limpa ao final. Referência e árvore remotas conferidas pela API do GitHub. |
| Revisão final e encerramento | Documentação inicial, Git local, exclusões e referência remota conferidos sem falhas técnicas. Encerramento aprovado pelo responsável; roadmap publicado no commit `ae80969`, antes do início da Etapa 1. |
| RNG-01 — Problema de negócio | Descrição comparada com a formulação aprovada; somente o RNG-01 registrado nessa entrega. Commit `cf9a0d3` contém apenas `docs/REQUISITOS.md`; sincronização com o GitHub confirmada. |
| RNG-02 — Objetivo do sistema | Descrição e resultado esperado comparados com a formulação aprovada; RNG-01 preservado e demais arquivos sem alteração. Commit `e5a6794` contém somente `docs/REQUISITOS.md`; publicação e sincronização conferidas. |
| RNG-03 — Público-alvo | Grupos de usuários e cenário de demonstração comparados com a proposta aprovada; requisitos anteriores preservados. Commit `4d82d0a` contém somente `docs/REQUISITOS.md`; publicação e sincronização conferidas. |
| RNG-04 — Benefícios esperados | Quatro benefícios e ressalva de resultados pretendidos comparados com o texto aprovado; requisitos anteriores preservados. Commit `d638bfe` contém somente `docs/REQUISITOS.md`; publicação e sincronização conferidas. |
| RNG-05 — Escopo do MVP | Em 20/10/2026, sete capacidades e sequência do ML conferidas com a proposta aprovada; ML explícito na entrega final e requisitos anteriores preservados. Commit `768de4d` contém somente `docs/REQUISITOS.md`; publicação e sincronização conferidas. |
| RNG-06 — Limitações do MVP | Cinco limitações comparadas com a proposta aprovada; requisitos anteriores e ML no MVP final preservados. Commit `52ce5e5` contém somente `docs/REQUISITOS.md`; publicação e sincronização conferidas. |
| RNG-07 — Critérios de sucesso do MVP | Sete critérios e evidências comparados com a proposta aprovada, com comprovação futura explícita; requisitos anteriores preservados. Commit `f90218f` contém somente `docs/REQUISITOS.md`; publicação e sincronização conferidas. |
| README do perfil | Uma entrada do GeoVale adicionada no padrão existente, com funcionalidades apresentadas como previstas; conteúdo publicado conferido e demais entradas preservadas. |
| Revisão final da Etapa 1 | RNG-01 a RNG-07 comparados com o roteiro original. Identificadas duas inconsistências documentais: andamento desatualizado no README e no roadmap, com ML apresentado como possibilidade no README. Correções publicadas nas unidades abaixo; na ocasião, o encerramento ainda dependia de aprovação. |
| Sincronização do README | Commit `1d8a926` contém somente `README.md`: etapa atual e participação do ML no MVP final conferidas com os requisitos; diff sem erros de espaços, demais arquivos preservados e sincronização com o GitHub confirmada. |
| Sincronização do roadmap | Commit `9888fcf` contém somente `docs/ROADMAP.md`: andamento conferido com os requisitos e o README, etapas seguintes preservadas, diff sem erros de espaços e sincronização com o GitHub confirmada. |
| Encerramento da Etapa 1 | Responsável aprovou o encerramento em 20/10/2026 após a revisão dos sete requisitos e as correções documentais. Registro de conclusão conferido com a aprovação; naquele momento, a Etapa 2 ainda não havia sido iniciada. |
| Registro do encerramento no roadmap | Commit `00633ea` contém somente `docs/ROADMAP.md`; aprovação e data conferidas com o status, etapas seguintes preservadas, diff sem erros de espaços e publicação confirmada com Git limpo e sincronizado. |
| Registro do encerramento no README | Commit `100ea80` contém somente `README.md`; conclusão e data consistentes com o status e o roadmap, Etapa 2 ainda não iniciada naquele momento, diff sem erros de espaços e publicação confirmada com Git limpo e sincronizado. |
| Atores da Etapa 2 | Commit `5eeb0ed` contém somente `docs/REQUISITOS.md`; AT-01 e AT-02 conferidos com o RNG-03, sete requisitos de negócio preservados integralmente, diff sem erros de espaços e publicação confirmada com Git limpo e sincronizado. |
| RF-01 — Envio e validação | Definição comparada com a proposta aprovada e com o RNG-05. Commit `50314a4` contém somente `docs/REQUISITOS.md`; conteúdo anterior preservado integralmente, cenários válidos, inválidos e de falha registrados, pendências técnicas explícitas, diff sem erros de espaços e publicação confirmada com Git limpo e sincronizado. Testes funcionais ainda não executados, pois a funcionalidade não foi implementada. |
| RF-02 — Leitura e identificação da área | Definição comparada com a proposta aprovada, o RF-01 e o escopo do RNG-05. Commit `d125d07` contém somente `docs/REQUISITOS.md`; conteúdo anterior preservado integralmente, três cenários de aceitação e dependências explícitas, diff sem erros de espaços e publicação confirmada com Git limpo e sincronizado. Testes funcionais ainda não executados, pois a funcionalidade não foi implementada. |
| RF-03 — Cálculo da extensão do terreno | Definição comparada com a proposta aprovada, o RF-02 e o escopo do RNG-05. Commit `e75fde6` contém somente `docs/REQUISITOS.md`; conteúdo anterior preservado integralmente, unidades em m² e hectares, referência para conferência e pendências técnicas explícitas, diff sem erros de espaços e publicação confirmada com Git limpo e sincronizado. Testes de cálculo ainda não executados, pois a funcionalidade não foi implementada. |
| RF-04 — Cruzamento com as bases geográficas | Definição comparada com a proposta aprovada, o RF-02 e o escopo do RNG-05. Commit `8b9e763` contém somente `docs/REQUISITOS.md`; conteúdo anterior preservado integralmente, fontes, quatro cenários de aceitação e dependências explícitas, diff sem erros de espaços e publicação confirmada com Git limpo e sincronizado. Testes de cruzamento ainda não executados, pois a funcionalidade não foi implementada. |
| RF-05 — Distâncias, sobreposições e alertas | Definição comparada com a proposta aprovada, o RF-04 e o escopo do RNG-05. Commit `c9574e4` contém somente `docs/REQUISITOS.md`; conteúdo anterior preservado integralmente, cinco cenários de aceitação, unidades, fontes, parâmetros e pendências explícitos, diff sem erros de espaços e publicação confirmada com Git limpo e sincronizado. Testes de medições e alertas ainda não executados, pois a funcionalidade não foi implementada. |
| RF-06 — Aplicação de regras demonstrativas | Definição comparada com a proposta aprovada, o RF-05 e os RNG-05 e RNG-06. Commit `828f4ac` contém somente `docs/REQUISITOS.md`; conteúdo anterior preservado integralmente, cinco cenários de aceitação, justificativas, restrições separadas das pontuações e pendências explícitas, diff sem erros de espaços e publicação confirmada com Git limpo e sincronizado. Testes de aplicação das regras ainda não executados, pois a funcionalidade não foi implementada. |
| RF-07 — Cadastro e seleção de alternativas | Definição comparada com a proposta aprovada, o RF-02 e os RNG-05 e RNG-07. Commit `f6c0ec4` contém somente `docs/REQUISITOS.md`; conteúdo anterior preservado integralmente, cinco cenários de aceitação, mínimo de duas alternativas distintas e pendências explícitos, diff sem erros de espaços e publicação confirmada com Git limpo e sincronizado. Testes de cadastro e seleção ainda não executados, pois a funcionalidade não foi implementada. |
| RF-08 — Critérios, notas e pesos | Definição comparada com a proposta aprovada, o RF-07 e os RNG-05 e RNG-07. Commit `4471b22` contém somente `docs/REQUISITOS.md`; conteúdo anterior preservado integralmente, quatro cenários de aceitação, associação das notas e pendências explícitas, diff sem erros de espaços e publicação confirmada com Git limpo e sincronizado. Testes de configuração ainda não executados, pois a funcionalidade não foi implementada. |
| RF-09 — Cálculo multicritério | Definição comparada com a proposta aprovada, os RF-06, RF-07 e RF-08 e os RNG-05 e RNG-07. Commit `4429780` contém somente `docs/REQUISITOS.md`; conteúdo anterior preservado integralmente, cinco cenários de aceitação, soma ponderada, classificação, restrições separadas e pendências explícitas, diff sem erros de espaços e publicação confirmada com Git limpo e sincronizado. Testes de cálculo multicritério ainda não executados, pois a funcionalidade não foi implementada. |
| RF-10 — Dashboard | Definição comparada com a proposta aprovada, os requisitos anteriores e os RNG-05 e RNG-07. Commit `87f58c7` contém somente `docs/REQUISITOS.md`; conteúdo anterior preservado integralmente, dois atores, cinco cenários de aceitação, fontes, parâmetros, limitações e ML no MVP final explícitos, diff sem erros de espaços e publicação confirmada com Git limpo e sincronizado. Testes do dashboard ainda não executados, pois a funcionalidade não foi implementada. |
| RF-11 — Persistência e consulta | Definição comparada com a proposta aprovada e os RNG-05 e RNG-07. Commit `412158e` contém somente `docs/REQUISITOS.md`; conteúdo anterior preservado integralmente, atores, cinco cenários de aceitação, recuperação em nova sessão e pendências explícitos, diff sem erros de espaços e publicação confirmada com Git limpo e sincronizado. Testes de persistência e consulta ainda não executados, pois a funcionalidade não foi implementada. |
| RF-12 — Exportação de relatório | Definição comparada com a proposta aprovada e os RNG-05 e RNG-07. Commit `734cddf` contém somente `docs/REQUISITOS.md`; conteúdo anterior preservado integralmente, atores, cinco cenários de aceitação, rastreabilidade, identificação de informações simuladas e ML no relatório final explícitos, diff sem erros de espaços e publicação confirmada com Git limpo e sincronizado. Testes de exportação ainda não executados, pois a funcionalidade não foi implementada. |
| RF-13 — Previsão demonstrativa por ML | Definição comparada com a proposta aprovada e os RNG-05, RNG-06 e RNG-07. Commit `bfdb6be` contém somente `docs/REQUISITOS.md`; conteúdo anterior preservado integralmente, atores, seis cenários de aceitação, integração, origem, limitações, restrições e implementação na Etapa 8 explícitos, diff sem erros de espaços e publicação confirmada com Git limpo e sincronizado. Treinamento, avaliação e testes ainda não executados, pois o modelo não foi implementado. |
| RNF-01 — Clareza da interface e das mensagens | Definição comparada com a proposta aprovada e os RNG-02 e RNG-07. Commit `28e9a94` contém somente `docs/REQUISITOS.md`; sete RNG, 13 RF e atores preservados integralmente, três cenários de aceitação e checklist futuro explícitos, diff sem erros de espaços e publicação confirmada com Git limpo e sincronizado. Verificação de usabilidade ainda não executada, pois a interface não foi implementada. |
| RNF-02 — Rastreabilidade da análise | Definição comparada com a proposta aprovada e os RNG-02, RNG-06 e RNG-07. Commit `92a78bb` contém somente `docs/REQUISITOS.md`; conteúdo anterior preservado integralmente, três cenários de aceitação, informações simuladas, correspondência entre análise, consulta e relatório e pendências explícitos, diff sem erros de espaços e publicação confirmada com Git limpo e sincronizado. Verificação funcional ainda não executada, pois a rastreabilidade não foi implementada. |
| RNF-03 — Execução e testes reproduzíveis | Definição comparada com a proposta aprovada e o RNG-07. Commit `72016e7` contém somente `docs/REQUISITOS.md`; conteúdo anterior preservado integralmente, quatro cenários de aceitação, ambiente limpo, identificação das condições de reprodução, tolerâncias, ML e verificações futuras explícitos, diff sem erros de espaços e publicação confirmada com Git limpo e sincronizado. Verificações da aplicação ainda não realizadas, pois não existe aplicação executável. |
| RNF-04 — Tratamento de falhas | Definição comparada com a proposta aprovada, os RF-01, RF-11 e RF-12 e o RNF-01. Commit `7b234b3` contém somente `docs/REQUISITOS.md`; conteúdo anterior preservado integralmente, cinco cenários de aceitação, preservação das análises, nova tentativa, proteção das mensagens e registros e verificações futuras explícitos, diff sem erros de espaços e publicação confirmada com Git limpo e sincronizado. Cenários de falha ainda não testados, pois o tratamento de falhas da aplicação não foi implementado. |
| RNF-05 — Desempenho no cenário demonstrativo | Definição comparada com a proposta aprovada, o RNG-07 e a Etapa 9 do roadmap. Commit `0d60a9c` contém somente `docs/REQUISITOS.md`; conteúdo anterior preservado integralmente, quatro cenários de aceitação, medições das operações e do fluxo completo, condições de medição, comparação com limites e pendências explícitos, diff sem erros de espaços e publicação confirmada com Git limpo e sincronizado. Tempos da aplicação ainda não medidos, pois não existe aplicação executável. |
| RNF-06 — Organização e manutenção do código | Definição comparada com a proposta aprovada e a separação de responsabilidades prevista na Etapa 4 do planejamento. Commit `e488333` contém somente `docs/REQUISITOS.md`; conteúdo anterior preservado integralmente, quatro cenários de aceitação, nomes descritivos, docstrings e comentários em português, revisões futuras e pendências explícitos, diff sem erros de espaços e publicação confirmada com Git limpo e sincronizado. Atendimento ainda não verificado, pois não existe código da aplicação para revisão. |
| Revisão documental dos seis RNF | Conferidos com o planejamento, o roadmap e os requisitos existentes: todos possuem estado, origem, prioridade, descrição, critérios de aceitação, forma e momento de verificação; 23 cenários no total. Cinco RNF são essenciais e o RNF-05 é importante para a demonstração. Não foram encontradas contradições entre eles; detalhamentos continuam pendentes, incluindo limites mensuráveis de desempenho. Identificada a ausência do registro explícito das licenças nos critérios do documento de requisitos, embora previsto no planejamento. Nenhum arquivo foi alterado durante a revisão e o Git permaneceu limpo; nenhum teste da aplicação foi executado. |
| RT-01 — Origem e condições de uso das bases geográficas | Definição comparada com a proposta aprovada, o RNF-02 e a Etapa 6 do planejamento. Commit `cf710ab` contém somente `docs/REQUISITOS.md`; conteúdo anterior preservado integralmente, quatro cenários de aceitação, referência das fontes e condições de uso, identificação de metadados indisponíveis e correspondência com a base utilizada explícitos. Exigência das licenças incluída nos critérios; diff sem erros de espaços e publicação confirmada com Git limpo e sincronizado. Atendimento ainda não verificado, pois não existem bases preparadas nem armazenamento implementado. |
| RT-02 — Sistemas de coordenadas e unidades dos cálculos geográficos | Definição comparada com a proposta aprovada e os RF-03 a RF-05. Commit `bacc27f` contém somente `docs/REQUISITOS.md`; conteúdo anterior preservado integralmente, cinco cenários de aceitação, referências e unidades identificáveis, compatibilização, bloqueio de cálculos sem referência validada, comparação com valores de referência e pendências explícitos. Diff sem erros de espaços e publicação confirmada com Git limpo e sincronizado. Atendimento ainda não verificado, pois não existem bases preparadas nem cálculos implementados. |
| RN-01 — Restrições eliminatórias na comparação de alternativas | Definição comparada com a proposta aprovada e os RF-06, RF-09 e RF-13. Commit `645e4ea` contém somente `docs/REQUISITOS.md`; conteúdo anterior preservado integralmente, três cenários de aceitação, preservação das restrições diante de pontuação alta e previsão favorável, identificação da regra e da justificativa e pendências explícitos. Diff sem erros de espaços e publicação confirmada com Git limpo e sincronizado. Atendimento ainda não verificado, pois a comparação multicritério e o modelo não foram implementados. |
| RN-02 — Identificação de informações simuladas | Definição comparada com a proposta aprovada, os RNG-05 a RNG-07, o RNF-02 e os RF-10, RF-12 e RF-13. Commit `fe12768` contém somente `docs/REQUISITOS.md`; conteúdo anterior preservado integralmente, quatro cenários de aceitação, identificação das informações simuladas, correspondência entre análise, dashboard e relatório, treinamento sintético e pendências explícitos. Diff sem erros de espaços e publicação confirmada com Git limpo e sincronizado. Atendimento ainda não verificado, pois as funcionalidades correspondentes não foram implementadas. |
| RN-03 — Indisponibilidade de dados e ausência de ocorrência | Definição comparada com a proposta aprovada, os RF-05 e RF-10 e o RNG-06. Commit `a60e897` contém somente `docs/REQUISITOS.md`; conteúdo anterior preservado integralmente, três cenários de aceitação, ausência limitada aos dados analisados, identificação da indisponibilidade, correspondência no dashboard e pendências explícitos. Diff sem erros de espaços e publicação confirmada com Git limpo e sincronizado. Atendimento ainda não verificado, pois a análise e o dashboard não foram implementados. |
| Revisão documental dos dois RT e das três RN | Conferidos com o planejamento, o roadmap e os requisitos existentes: cinco itens com estado, origem, prioridade essencial, descrição, critérios de aceitação, dependências e momento de verificação; 19 cenários no total. Não foram encontradas contradições entre as definições e a exigência das licenças está explícita no RT-01. Identificados refinamentos pendentes para alternativas restritas na classificação, incluindo todas restritas, e para efeitos da indisponibilidade na comparação e sua preservação no relatório. Cinco arquivos versionados preservados integralmente e Git limpo durante a revisão; nenhum teste da aplicação executado. |
| Refinamento da classificação da RN-01 | Conferido com a proposta aprovada e os RF-06, RF-09 e RF-13. Commit `64979eb` altera somente a seção RN-01 em `docs/REQUISITOS.md`; demais seções preservadas integralmente. Dois cenários acrescentados, totalizando cinco: classificação apenas das alternativas sem restrição identificada, apresentação separada das restritas com regra e justificativa e nenhuma alternativa elegível quando todas estiverem restritas, para dados necessários disponíveis. Pendências preservadas, diff sem erros de espaços e publicação confirmada com Git limpo e sincronizado. Cenários ainda não testados, pois a comparação não foi implementada. |
| Refinamento dos efeitos da indisponibilidade na RN-03 | Conferido com a proposta aprovada, os RF-05, RF-09, RF-10 e RF-12 e a classificação da RN-01. Commit `37909e5` altera somente a seção RN-03 em `docs/REQUISITOS.md`; demais seções preservadas integralmente. Três cenários acrescentados, totalizando seis, com bloqueio do ranking por dados necessários indisponíveis, preservação de resultados parciais, identificação no dashboard e no relatório e ausência de substituição automática por zero. Pendências preservadas, diff sem erros de espaços e publicação confirmada com Git limpo e sincronizado. Identificada remissão desatualizada na RN-01, a sincronizar em unidade própria. Testes da aplicação ainda não executados. |
| Sincronização da referência entre RN-01 e RN-03 | Commit `301539a` altera somente o parágrafo de dependências da RN-01 em `docs/REQUISITOS.md`, substituindo a pendência desatualizada pela referência ao tratamento já aprovado na RN-03. Correspondência entre as regras conferida; classificação, critérios de aceitação e conteúdo fora do parágrafo preservados integralmente. Pendências sobre dados necessários, disponibilidade e condições demonstrativas mantidas. Diff sem erros de espaços e publicação confirmada com Git limpo e sincronizado. Verificação documental, sem testes da aplicação. |
| Levantamento das pendências para encerrar a Etapa 2 | Planejamento original, requisitos, roadmap e status comparados. Confirmados 13 RF, seis RNF, dois RT e três RN, com identificadores únicos. Identificados seis blocos de decisões de comportamento e detalhamentos previstos para etapas posteriores; propostas revisão final e atualização do andamento no README e no roadmap antes do encerramento. Nenhum arquivo alterado durante o levantamento, cinco arquivos versionados preservados integralmente e Git limpo. Sem testes da aplicação e sem encerramento da etapa. |
| Formato inicial do RF-01 | GeoJSON com extensão `.geojson` conferido com a proposta aprovada e a RFC 7946. Commit `57b5e7d` altera somente a seção RF-01 em `docs/REQUISITOS.md`; demais seções preservadas integralmente. Quatro critérios acrescentados, totalizando nove: conteúdo GeoJSON válido segue às demais validações; arquivo vazio, JSON malformado, JSON que não represente GeoJSON e extensão não aceita são rejeitados. Pendências preservadas, diff sem erros de espaços e publicação confirmada com Git limpo e sincronizado. Validação ainda não implementada nem testada funcionalmente. |
| Estrutura inicial do RF-01 | Conferida com a proposta aprovada e a RFC 7946. Commit `0d8835e` altera somente a seção RF-01 em `docs/REQUISITOS.md`; demais seções preservadas integralmente. Cinco critérios estruturais acrescentados, totalizando 14 no RF-01: objeto principal `FeatureCollection`, lista `features` não vazia com itens `Feature`, geometria não nula e `properties` como objeto ou `null`. Restrições do MVP distinguidas das possibilidades da RFC; pendências preservadas. Diff sem erros de espaços e publicação confirmada com Git limpo e sincronizado. Validação ainda não implementada nem testada funcionalmente. |
| Tipos de geometria do RF-01 | Commit `a08f135` conferido contra a proposta aprovada: `Polygon` e `MultiPolygon` seguem às demais validações; pontos, linhas e `GeometryCollection` são rejeitados, inclusive quando a coleção contém somente polígonos. Quatro cenários acrescentados, totalizando 18. Somente a seção RF-01 de `docs/REQUISITOS.md` foi alterada; demais seções e arquivos preservados. Pendências de validade, limites e múltiplas áreas mantidas. Diff sem erros de espaços, diretório limpo e igualdade entre HEAD, origin/main e referência consultada no GitHub confirmados após o envio. Validação ainda não implementada nem testada funcionalmente. |
| Validade das geometrias do RF-01 | Commit `fa0601c` conferido contra a proposta aprovada: nove cenários acrescentados, totalizando 27; os 18 anteriores foram preservados. Condições de coordenadas, fechamento dos anéis, cruzamentos, recortes, relações entre partes e sentido de percurso registradas, com rejeição e bloqueio sem correção automática. Apenas a seção RF-01 de `docs/REQUISITOS.md` foi alterada; demais seções e arquivos preservados. Limites, múltiplas áreas e definições de cálculo do RF-03 e do RT-02 continuam pendentes. Diff sem erros de espaços e publicação confirmada, com igualdade entre HEAD, origin/main e referência consultada no GitHub e diretório limpo. Conferência documental; validação ainda não implementada nem testada funcionalmente. |
| Comparação exploratória de arquivos reais para os limites do RF-01 | Três GeoJSON conferidos localmente quanto à estrutura e à validade geométrica, com 410, 103 e 11.231 posições e 11.017, 3.099 e 312.924 bytes, respectivamente. Águas Claras e Itabira são contornos de extração mapeados no OpenStreetMap; não representam perímetros oficiais. A APA Sul RMBH, obtida da camada estadual de unidades de conservação da IDE-Sisema, foi somente teste auxiliar não minerário. Leituras, validade, reprojeção e área foram exercitadas em ambiente exploratório separado; não houve teste do GeoVale, comprovação de capacidade máxima ou aprovação do desempenho do RNF-05. |
| Limites de entrada do RF-01 | Commit `a8a1b48` conferido contra a proposta aprovada: máximo de 1 MiB (1.048.576 bytes) e 20.000 posições por arquivo, incluindo partes, recortes e fechamentos, com os dois limites inclusivos. Seis cenários acrescentados, totalizando 33; os 27 anteriores preservados. Rejeição integral e bloqueio ao exceder qualquer limite, sem simplificação automática, e prosseguimento às demais validações quando dentro dos limites. Somente RF-01 alterado, demais seções e arquivos preservados; múltiplas áreas e definições de cálculo e desempenho continuam pendentes. Diff sem erros de espaços e publicação confirmada, com HEAD, origin/main e referência consultada no GitHub iguais e diretório limpo. Conferência documental; validação ainda não implementada nem testada funcionalmente. |
| Área única por arquivo nos RF-01 e RF-02 | Commit `3eede04` conferido contra a opção 1 aprovada: exatamente uma `Feature`, com `Polygon` ou `MultiPolygon` válido e todas as partes disponibilizadas em conjunto; várias `Feature` rejeitadas mesmo quando representam partes da mesma mina, com orientação e sem seleção ou união automática. Somente essas duas seções de `docs/REQUISITOS.md` alteradas; RF-01 com 36 critérios e RF-02 com cinco, preservando os 33 e os três anteriores, respectivamente. Limites de tamanho e posições mantidos; demais seções e arquivos preservados. Diff sem erros de espaços e publicação confirmada, com HEAD, origin/main e referência consultada no GitHub iguais e diretório limpo. Conferência documental; funcionalidades ainda não implementadas e testes da aplicação ainda não executados. |
| Cruzamentos iniciais do RF-04 | Commit `21c5430` conferido contra a proposta aprovada: três grupos de camadas, geometria completa com todas as partes e recortes, identificação dos elementos e de suas fontes, distinção entre contato e sobreposição e entre ausência de ocorrência e indisponibilidade. Seis cenários acrescentados, totalizando dez; quatro anteriores preservados. Somente a seção RF-04 de `docs/REQUISITOS.md` alterada; demais seções e arquivos intactos. Pendências de fontes, cobertura, preparação, medidas, alertas, restrições, terreno e declividade explícitas. Diff sem erros de espaços e publicação confirmada, com HEAD, origin/main e referência consultada no GitHub iguais e diretório limpo. Conferência documental; cruzamentos do GeoVale ainda não implementados nem testados funcionalmente. |
| Medidas descritivas iniciais do RF-05 | Commit `d651b17` conferido contra a proposta aprovada: áreas em m² e hectares, percentual sobre a área total, consolidação por camada sem duplicar superfícies e menor distância geométrica em metros, com todas as partes e recortes considerados. Fonte, cobertura, referência, unidades e parâmetros consultáveis; contato, ausência e indisponibilidade distinguidos. Referência de Servou e colaboradores e documentação das operações registradas, com adaptação ao MVP e limites de interpretação explícitos. Sete cenários acrescentados, totalizando 12; cinco anteriores preservados. Somente a seção RF-05 de `docs/REQUISITOS.md` alterada, demais seções e arquivos intactos. Exemplos numéricos identificados como didáticos; pendências mantidas. Diff sem erros de espaços e publicação confirmada, com HEAD, origin/main e referência consultada no GitHub iguais e diretório limpo. Conferência documental; medidas do GeoVale ainda não implementadas nem testadas funcionalmente. |
| Alertas informativos iniciais do RF-05 | Commit `a0e1b77` conferido contra a proposta aprovada: cinco condições de mensagens, consulta de camada, fonte e condições da análise, preservação dos resultados parciais válidos e bloqueio do ranking quando faltar dado necessário, conforme a RN-03. Seis critérios acrescentados, totalizando 18; 12 anteriores e fundamentação preservados. Mensagens descritivas sem classificação automática de risco, aptidão, segurança ou restrição. Somente a seção RF-05 de `docs/REQUISITOS.md` alterada, demais seções e arquivos intactos. Pendências de precisão, tolerâncias, alcance e eventuais alertas adicionais mantidas. Diff sem erros de espaços e publicação confirmada, com HEAD, origin/main e referência consultada no GitHub iguais e diretório limpo. Conferência documental; alertas ainda não implementados nem testados funcionalmente. |
| Estrutura e avaliação das regras do RF-06 | Commit `4b2d350` conferido contra a proposta aprovada em 21/10/2026: identificação, finalidade, condição, fundamentação, efeito e justificativa, com referência ao guia do IBRAM e limitações explícitas. Resultados de restrição identificada, não identificada segundo a regra e avaliação indisponível definidos; regras incompletas não aplicadas como válidas; falta de dados tratada conforme a RN-03 e restrições preservadas conforme a RN-01. Seis critérios acrescentados, totalizando 11; cinco anteriores preservados. Somente a seção RF-06 de `docs/REQUISITOS.md` alterada, demais seções e arquivos intactos. Condições específicas e parâmetros mantidos como pendências. Diff sem erros de espaços e publicação confirmada, com HEAD, origin/main e referência consultada no GitHub iguais e diretório limpo. Conferência documental; regras ainda não implementadas nem testadas funcionalmente. |
| Primeira regra concreta RF06-R01 do RF-06 | Commit `77d763c` conferido contra a proposta aprovada: versão 0.1, cenário solar em terreno, condição de ausência de superfície fora da união das massas d’água, dados necessários, unidades, fonte EPA/NREL, adaptação simulada e limitações explícitas. Cobertura total, parcial, contato na borda, todas as partes de um `MultiPolygon`, sobreposições entre polígonos de água, arredondamento e indisponibilidade contemplados. Sete cenários acrescentados, totalizando 18; os 11 anteriores preservados em tabela contínua. Somente a seção RF-06 de `docs/REQUISITOS.md` alterada; demais seções e quatro arquivos versionados preservados. `git diff --check` sem problemas; conteúdo do commit e publicação conferidos, com HEAD, origin/main e referência remota iguais a `77d763c48ae36ae05c013558f5a1108c06a348b6` e árvore de trabalho limpa ao concluir. Conferência documental; implementação, testes funcionais, bases definitivas e parâmetros técnicos continuam futuros. |
| Campos e validações do cadastro e da seleção do RF-07 | Commit `a654a8b` conferido contra a proposta aprovada: nome e descrição do cenário obrigatórios, validação de texto, campos ausentes, vazios ou somente com espaços, rejeição de nomes repetidos desconsiderando maiúsculas, minúsculas, espaços nas pontas e espaços consecutivos, mensagens compreensíveis, seleção somente de alternativas cadastradas e pelo menos duas distintas, sem duplicar a contagem da mesma opção. RN-01 e RN-03 preservadas; pesos continuam associados aos critérios no RF-08. Seis cenários acrescentados, totalizando 11; os cinco anteriores preservados em tabela contínua. Somente a seção RF-07 de `docs/REQUISITOS.md` alterada; demais seções e quatro arquivos versionados preservados. `git diff --check` sem problemas; conteúdo do commit e publicação conferidos, com HEAD, origin/main e referência remota iguais a `a654a8bf988a26b36d534470a8fe67c095feb7eb` e árvore de trabalho limpa ao concluir. Conferência documental; cadastro e seleção ainda não implementados nem testados funcionalmente, lista definitiva de alternativas e armazenamento pendentes. |
| Cenários de referência do MVP no RF-07 | Commit `f0fa236` conferido contra a proposta aprovada: três nomes e descrições registrados para Revegetação com espécies nativas, Lazer e educação ambiental e Solar em terreno. Correspondência do cenário solar com a RF06-R01, objetivo predominante de cada cenário, comparação para a mesma área e possibilidade de cadastrar outras alternativas válidas explicitados. Duas referências, Servou e colaboradores (2023) e EPA/NREL, registradas com adaptações demonstrativas e limitações, sem afirmar viabilidade local. Campos, validações do cadastro e da seleção e 11 critérios de aceitação preservados integralmente; três linhas de cenários e estrutura da tabela conferidas. Somente a seção RF-07 de `docs/REQUISITOS.md` alterada; demais seções e quatro arquivos versionados preservados. `git diff --check` sem problemas; conteúdo do commit e publicação conferidos, com HEAD, origin/main e referência remota iguais a `f0fa236566886a078fc4fcad7757d580fd6ab491` e árvore de trabalho limpa ao concluir. Conferência documental; condições de avaliação, implementação e testes funcionais continuam futuros. |
| Critérios iniciais de comparação do RF-08 | Commit `c1fb652` conferido contra a proposta aprovada: Declividade do terreno em graus, Proximidade de vias mapeadas em metros e Proximidade de vegetação nativa remanescente em metros, com dados necessários, fontes de Servou e colaboradores (2023) e Worden e colaboradores (2024), adaptações e limitações. Medidas descritivas separadas de notas, pesos e restrições; interpretação por cenário, disponibilidade conforme a RN-03 e preservação das restrições conforme a RN-01 explicitadas. Três linhas de critérios e unidades conferidas; quatro critérios de aceitação anteriores preservados integralmente. Somente a seção RF-08 de `docs/REQUISITOS.md` alterada; demais seções e quatro arquivos versionados preservados. `git diff --check` sem problemas; conteúdo do commit e publicação conferidos, com HEAD, origin/main e referência remota iguais a `c1fb652f6cb3144f8d41a71381d9a76dc6744fdc` e árvore de trabalho limpa ao concluir. Conferência documental; dados concretos, cálculos e resumos, critérios específicos adicionais, escalas, notas e pesos ainda pendentes. Nenhuma implementação ou teste funcional realizado. |

Os registros de preparação do ambiente Python são históricos. Nesta revisão,
foram conferidos os documentos, os commits e o estado do Git; as verificações
do ambiente Python não foram repetidas.
Resultados de funcionalidades e métricas de ML não existem nesta fase.

## Pendências e problemas conhecidos

- Nenhuma falha foi encontrada nas verificações de preparação executadas.
- Ainda não há suíte de testes, interface, servidor, banco, conjunto de dados
  geográficos integrado à aplicação ou modelo de Machine Learning. As amostras
  exploratórias locais não constituem a preparação final dos dados da Etapa 6.
- As dependências da aplicação e a compatibilidade da futura stack com o Python
  observado ainda não foram avaliadas.
- A Etapa 0 foi encerrada com aprovação; não há pendências impeditivas
  conhecidas da preparação. As funcionalidades e decisões técnicas futuras
  pertencem às etapas seguintes.
- A criação do repositório, a configuração do origin e o primeiro envio foram
  autorizados e concluídos. A autenticação de envio pelo Git local funcionou.
- Os sete requisitos de negócio foram validados, revisados e publicados.
  A Etapa 1 foi encerrada com aprovação em 20/10/2026.
- O atendimento aos critérios do RNG-07 será verificado na validação e na
  demonstração do MVP, após sua implementação.
- Os benefícios registrados no RNG-04 ainda serão verificados na demonstração;
  não há medições de ganhos de tempo ou custo nesta fase.
- As inconsistências identificadas na revisão foram corrigidas e publicadas.
  Status, roadmap e README registram o encerramento aprovado da Etapa 1;
  não há pendência de sincronização desse marco.
- A Etapa 2 foi iniciada; atores e definições dos RF-01 a RF-13 foram documentados.
  O formato inicial do RF-01 está definido como GeoJSON com extensão `.geojson`
  e estrutura `FeatureCollection`, com tipos de geometria `Polygon` e
  `MultiPolygon`, regras de validade das geometrias e limites de até 1 MiB
  (1.048.576 bytes) e 20.000 posições por arquivo aprovados no requisito.
  O tratamento de partes e registros está aprovado nos RF-01 e RF-02:
  exatamente uma `Feature` por arquivo, admitindo várias partes válidas em um
  `MultiPolygon` para análise conjunta; arquivos com várias `Feature` serão
  rejeitados mesmo quando representarem a mesma mina. A preparação da área
  ocorrerá antes do envio; o GeoVale não selecionará nem unirá registros
  automaticamente. Os 36 critérios do RF-01 e os cinco do RF-02 ainda deverão
  ser testados na implementação. Os ensaios exploratórios locais não comprovam
  a capacidade máxima ou o desempenho do fluxo completo.
- A pendência de definição sobre múltiplas partes e registros dos RF-01 e
  RF-02 está resolvida. A validação, a leitura, a identificação e a preparação
  dos cenários funcionais de teste permanecem futuras.
- Para o RF-03, sistema de coordenadas adequado, precisão e tolerância de
  comparação precisam ser especificados e aprovados antes da implementação
  e da preparação dos testes com área de referência. A geometria de entrada
  deverá respeitar as regras já aprovadas nos RF-01 e RF-02.
- Para o RF-04, os três grupos de camadas e os cruzamentos iniciais estão
  aprovados. Permanecem pendentes as fontes definitivas, a cobertura, os
  metadados e as condições de uso do RT-01 e a preparação das bases na Etapa 6.
  O cruzamento depende da geometria do RF-02 e de sistemas de coordenadas
  compatíveis segundo o RT-02. As medidas descritivas iniciais estão definidas
  no RF-05, juntamente com os alertas informativos iniciais. Precisão,
  tolerâncias, alcance de consulta e eventuais alertas adicionais continuam
  pendentes. A lista dos dados
  necessários à comparação e os critérios de disponibilidade permanecem
  pendentes na RN-03. Terreno, declividade, demais operações e cenários de
  referência serão detalhados e aprovados nas unidades correspondentes.
  Os dez critérios do RF-04 ainda não foram testados funcionalmente.
- Para o RF-05, as medidas descritivas com suas referências e os alertas
  informativos iniciais estão aprovados, com 18 critérios. Referência espacial
  concreta, precisão, tolerâncias e alcance de consulta precisam ser detalhados
  e aprovados antes da implementação e da preparação dos cenários de referência.
  Eventuais alertas adicionais, inclusive por faixas numéricas, exigirão
  fundamentação específica e aprovação prévia. Fontes definitivas, cobertura,
  preparação e metadados das bases continuam pendentes nas etapas correspondentes. A lista de dados
  necessários à comparação e os critérios de disponibilidade permanecem
  pendentes na RN-03. Medidas descritivas não definem notas, pesos, faixas de
  segurança ou restrições; essas definições exigem fundamentação própria.
  Os exemplos são didáticos; os testes funcionais continuam futuros.
- Para o RF-06, a estrutura, a fundamentação, o comportamento de avaliação
  e a primeira regra concreta RF06-R01 estão aprovados, com 18 critérios.
  As demais regras, condições, parâmetros e unidades, fontes, adaptações e
  dados necessários ainda precisam ser detalhados e aprovados. A RF06-R01
  depende da seleção e preparação da camada concreta na Etapa 6, de critérios
  de disponibilidade e adequação da cobertura e dos detalhamentos de referência
  espacial, precisão e tolerâncias do RT-02 antes da implementação e dos
  arquivos de teste. Os três cenários de referência do RF-07 estão definidos;
  as demais regras de avaliação desses usos continuam pendentes.
  O tratamento de indisponibilidade segue a RN-03, e a preservação das
  restrições, a RN-01. A adaptação simulada não representa proibição brasileira
  ou validação ambiental; cobertura parcial de água não restringe toda a área
  por essa regra. Implementação e testes funcionais futuros.
- Para o RF-07, os dois campos obrigatórios, as validações do cadastro e da
  seleção e os três cenários de referência do MVP estão aprovados; os 11
  critérios de aceitação foram preservados. Permanecem pendentes as condições
  de avaliação dos usos, espécies para revegetação adequadas à região, demais
  regras do RF-06, demais critérios, notas e pesos dos RF-08 e RF-09 e dados necessários,
  incluindo a disponibilidade conforme a RN-03. O armazenamento será detalhado
  nas etapas correspondentes, conforme o RF-11. A dependência da área do RF-02
  e as demais pendências anteriores permanecem em aberto. Implementação e
  testes funcionais futuros.
- Para o RF-08, três critérios iniciais, dados necessários, unidades, fontes
  e limitações estão aprovados; os quatro critérios de aceitação foram
  preservados. Permanecem pendentes as bases concretas e camadas de vias e
  vegetação na Etapa 6, os cruzamentos adicionais do RF-04, o cálculo e resumo
  da declividade, o alcance das consultas, referência espacial, precisão e
  tolerâncias. Critérios específicos adicionais, incluindo radiação e rede
  elétrica para solar, interpretação e conversão em notas por cenário,
  escalas, limites, valores e validação dos pesos e detalhes do tratamento de
  valores ausentes ainda exigem definição e aprovação antes da implementação
  e dos arquivos de teste, preservando as RN-01 e RN-03. A dependência do
  RF-07 e as demais pendências anteriores permanecem em aberto. Implementação
  e testes funcionais futuros.
- Para o RF-09, regras de normalização, precisão, empates e valores ausentes
  precisam ser definidas e aprovadas antes da implementação e da preparação
  dos cenários de teste com cálculo de referência. As dependências dos
  RF-06, RF-07 e RF-08 e as pendências anteriores permanecem em aberto.
- Para o RF-10, o detalhamento da apresentação precisa ser aprovado antes da
  implementação e da preparação dos cenários de teste. O dashboard depende
  dos resultados anteriores; a apresentação das previsões depende da
  integração de ML prevista na Etapa 8, incluída na entrega final do MVP.
- Para o RF-11, o modelo e as regras de armazenamento serão detalhados na
  Etapa 5 e deverão ser aprovados antes da implementação e da preparação
  dos cenários de teste. A dependência dos dados e resultados da análise e
  as pendências anteriores permanecem em aberto.
- Para o RF-12, formato e estrutura do relatório precisam ser definidos e
  aprovados antes da implementação e da preparação dos cenários de teste.
  A exportação depende dos dados e resultados da análise; a inclusão das
  previsões depende da integração de ML prevista na Etapa 8, incluída na
  entrega final do MVP.
- Para o RF-13, alvo, atributos, treinamento, avaliação e conversão da previsão
  em entrada multicritério precisam ser definidos e aprovados antes da
  implementação e da preparação dos testes. O modelo depende dos atributos da
  análise geográfica; implementação, integração e testes permanecem na Etapa 8
  e incluídos no MVP final.
- Para o RNF-01, fluxos e interface serão detalhados nas etapas correspondentes.
  Os cenários do checklist precisam ser definidos e aprovados antes da
  verificação de usabilidade, que ocorrerá após a implementação.
- Para o RNF-02, a estrutura de armazenamento e os metadados das bases
  concretas precisam ser detalhados e aprovados nas etapas correspondentes,
  considerando o RT-01, antes da implementação e da preparação do cenário
  de referência. A verificação funcional ocorrerá após a implementação.
- Para o RNF-03, stack, versões, conjuntos de referência, tolerâncias e
  condições de reprodução, incluindo o ML, precisam ser definidos e aprovados
  antes das verificações nas etapas de implementação, validação e preparação
  da entrega. Ainda não existe aplicação executável para essas verificações.
- Para o RNF-04, detalhes de recuperação e registro precisam ser definidos e
  aprovados antes da implementação e da preparação dos cenários. A verificação
  ocorrerá após a implementação de cada funcionalidade correspondente.
- Para o RNF-05, ambiente, dados demonstrativos, operações avaliadas e limites
  de tempo precisam ser definidos e aprovados antes das medições. Os tempos
  das operações e do fluxo completo serão medidos após a implementação, com
  registro das condições e comparação com os limites aprovados.
- Para o RNF-06, arquitetura e convenções específicas precisam ser definidas
  e aprovadas na Etapa 4, antes da implementação correspondente. A estrutura,
  os nomes, as docstrings e os comentários serão revisados durante a
  implementação; ainda não existe código da aplicação para essa verificação.
- A revisão documental dos seis RNF foi concluída. A lacuna de especificação
  sobre as licenças foi tratada no RT-01; essa exigência está explícita nos
  critérios do documento de requisitos.
- Para o RT-01, a estrutura de armazenamento e os metadados das bases
  concretas ainda precisam ser detalhados nas etapas correspondentes. Os
  registros serão conferidos na preparação das bases na Etapa 6 e sua
  correspondência com os dados utilizados será verificada na implementação.
  Nenhuma base concreta teve seus metadados verificados nesta entrega.
- Para o RT-02, sistemas concretos, procedimentos de compatibilização,
  unidades de distância, precisão e tolerâncias precisam ser definidos e
  aprovados antes da implementação e da preparação dos testes correspondentes.
  As referências serão conferidas na preparação dos dados na Etapa 6; os
  cálculos, as unidades, a compatibilização e os bloqueios serão verificados
  durante a implementação. Nenhum cálculo foi testado nesta entrega.
- Para a RN-01, a primeira regra concreta RF06-R01 está definida no RF-06;
  as demais condições e os parâmetros das regras demonstrativas precisam
  ser detalhados e aprovados antes da implementação e da preparação dos
  cenários de teste. O tratamento geral da indisponibilidade está definido
  na RN-03, com referência sincronizada na RN-01. A
  preservação das restrições e sua justificativa serão verificadas nos RF-06
  e RF-09; o cenário com previsão favorável será testado após a integração
  do ML na Etapa 8. Nenhum desses testes foi executado nesta entrega.
- Para a RN-02, a forma de apresentação precisa ser detalhada e aprovada
  antes da implementação e da preparação dos cenários de teste. Metadados e
  armazenamento continuam pendentes de detalhamento. A identificação será
  verificada durante a implementação da análise, do dashboard e do relatório;
  o cenário com treinamento sintético será testado após a integração do ML
  na Etapa 8. Nenhum desses testes foi executado nesta entrega.
- Para a RN-03, a lista dos dados necessários para avaliar restrições e calcular
  a comparação, os critérios de disponibilidade e a forma de apresentação
  precisam ser detalhados e aprovados antes da implementação e da preparação
  dos testes, considerando as bases e suas limitações. As demais regras
  específicas de tratamento de dados ausentes permanecem em aberto. Os seis
  cenários serão verificados durante a implementação da análise, da comparação,
  do dashboard e do relatório; ainda não foram testados.
- A revisão documental dos dois RT e das três RN foi concluída. O tratamento
  das alternativas restritas na classificação foi detalhado na RN-01, aprovado
  e publicado, para cenários com os dados necessários disponíveis. Cenários
  mistos e de todas as alternativas restritas serão verificados durante a
  implementação. Condições e parâmetros demonstrativos continuam pendentes.
- Os efeitos gerais da indisponibilidade na comparação e no relatório foram
  detalhados e aprovados na RN-03. A referência desatualizada na RN-01 foi
  corrigida e publicada em unidade própria no commit `301539a`; essa pendência
  documental está resolvida. As definições concretas sobre dados necessários
  e disponibilidade continuam pendentes, conforme os registros anteriores.
- O RNF-05 ainda não possui limites de tempo mensuráveis para aprovação do
  desempenho; eles precisam ser definidos antes da avaliação.
- Os 13 RF do escopo atual, os RNF-01 a RNF-06, os RT-01 a RT-02 e as RN-01 a RN-03
  estão documentados.
  Refinamentos, eventuais complementos dos RNF, requisitos técnicos e regras
  de negócio, com
  prioridades, dependências e critérios de aceitação, ainda serão detalhados
  em pequenas unidades. A Etapa 2 permanece em andamento.
- Os resumos do README e do roadmap ainda antecedem o início da Etapa 2;
  sua atualização será tratada em unidades documentais próprias. Este status
  e o documento de requisitos registram o andamento atual.

## Plano de pendências para encerramento da Etapa 2

O levantamento foi apresentado ao responsável pelo projeto em 20/10/2026.
A sequência abaixo organiza as decisões ainda abertas; cada bloco será dividido
em pequenas entregas, com conteúdo e alterações aprovados antes do registro.
Este plano não define os comportamentos pendentes nem encerra a etapa.

| Ordem | Bloco | Decisões ainda necessárias |
| --- | --- | --- |
| 1 | Arquivo e área — RF-01 e RF-02 | Formato GeoJSON `.geojson`, estrutura `FeatureCollection`, tipos `Polygon` e `MultiPolygon`, regras de validade das geometrias e limites de até 1 MiB (1.048.576 bytes) e 20.000 posições por arquivo definidos. Tratamento definido: exatamente uma `Feature` por arquivo; várias partes válidas de um `MultiPolygon` compõem uma única área para análise conjunta; arquivos com várias `Feature` são rejeitados. Implementação e verificação funcional futuras. |
| 2 | Análise e restrições — RF-04 a RF-06 e RN-01/RN-03 | Cruzamentos iniciais do RF-04 definidos para unidades de conservação, rios e drenagem e massas d’água. Medidas descritivas e alertas informativos iniciais do RF-05 definidos. Pendentes fontes definitivas e preparação, demais operações, precisão, tolerâncias, alcance de consulta, eventuais alertas adicionais, demais condições concretas das regras de restrição e identificação dos dados necessários à comparação. Estrutura, comportamento de avaliação e primeira regra concreta RF06-R01 definidos no RF-06. Para essa regra, bases concretas, disponibilidade, cobertura e parâmetros técnicos permanecem pendentes. |
| 3 | Comparação — RF-07 a RF-09 | Nome e descrição obrigatórios, validações do cadastro e da seleção e três cenários de referência definidos no RF-07: Revegetação com espécies nativas, Lazer e educação ambiental e Solar em terreno. Três critérios iniciais do RF-08 definidos, com dados, unidades, fontes e limitações: declividade e proximidade de vias e de vegetação nativa remanescente. Pendentes operacionalização e condições de avaliação, critérios adicionais, escalas, notas, pesos, normalização, empates e precisão da pontuação; armazenamento nas etapas correspondentes. |
| 4 | Resultados — RF-10 a RF-12 | Confirmar informações mínimas para consulta e persistência, formato do relatório e apresentação dos resultados completos ou parciais. |
| 5 | ML — RF-13 | Significado da aptidão prevista e forma de utilização da previsão na pontuação. |
| 6 | Aceitação | Completar critérios verificáveis e estabelecer quando serão fixadas as metas dependentes do ambiente e dos dados, especialmente desempenho. |

Detalhamentos previstos para as etapas posteriores, conforme o planejamento:

| Etapa | Detalhamento previsto |
| --- | --- |
| 3 — Análise e modelagem | Casos de uso, fluxos e backlog. |
| 4 — Arquitetura e tecnologias | Arquitetura, stack, versões, convenções e compatibilidade da implantação. |
| 5 — Banco de dados | Modelo do banco e estrutura de armazenamento. |
| 6 — Dados geográficos | Região, bases concretas, metadados, referências espaciais e conjuntos de teste. |
| 8 — Machine Learning | Treinamento, avaliação e integração do ML, obrigatório no MVP final. |

Essa organização preserva as dependências: os detalhamentos precisam ser
aprovados antes da implementação e da preparação dos testes correspondentes.
A definição do significado da saída e de sua utilização na comparação pertence
aos requisitos; o treinamento e a integração permanecem na Etapa 8.

Antes do encerramento, será necessário revisar a especificação e atualizar o
andamento no README e no roadmap, que ainda apresentam a Etapa 2 como não
iniciada. Essas atualizações serão tratadas em unidades documentais próprias.
O encerramento depende de revisão e aprovação do responsável pelo projeto.

## Decisões ainda necessárias

- Especificar e aprovar sistema de coordenadas adequado, precisão e tolerância
  de comparação do RF-03 antes da implementação.
- Detalhar e aprovar fontes definitivas, cobertura, preparação das bases,
  dados de terreno e declividade e demais operações do RF-04 antes da
  implementação correspondente; os cruzamentos iniciais já estão definidos.
- Detalhar e aprovar referência espacial concreta, precisão, tolerâncias e
  alcance de consulta do RF-05 antes da implementação; as medidas descritivas
  e os alertas informativos iniciais já estão definidos. Eventuais alertas
  adicionais exigirão fundamentação específica e aprovação.
- Detalhar e aprovar as demais regras do RF-06, suas condições específicas,
  parâmetros e unidades, fontes, adaptações e dados necessários. A estrutura,
  o comportamento de avaliação e a primeira regra concreta RF06-R01 estão
  definidos; bases concretas, disponibilidade, cobertura, referência espacial,
  precisão e tolerâncias dessa regra permanecem pendentes antes da implementação.
- Detalhar as condições de avaliação dos três cenários de referência do RF-07,
  incluindo espécies adequadas à região para revegetação, demais regras,
  critérios e dados necessários nos requisitos correspondentes. Campos,
  validações e cenários estão definidos; armazenamento nas etapas correspondentes,
  implementação e testes funcionais futuros.
- Completar os critérios específicos e a operacionalização do RF-08; definir
  e aprovar escalas, conversão em notas por cenário, limites, valores e
  validação dos pesos e detalhes do tratamento de valores ausentes antes
  da implementação. Os três critérios iniciais, dados, unidades, fontes e
  limitações já estão definidos.
- Definir e aprovar regras de normalização, precisão, empates e valores
  ausentes do RF-09 antes da implementação.
- Detalhar e aprovar a apresentação do RF-10 antes da implementação.
- Definir e aprovar o modelo e as regras de armazenamento do RF-11 na Etapa 5,
  antes da implementação.
- Definir e aprovar formato e estrutura do relatório do RF-12 antes da
  implementação.
- Definir e aprovar alvo, atributos, treinamento, avaliação e conversão da
  previsão em entrada multicritério do RF-13 antes da implementação.
- Definir e aprovar os cenários do checklist do RNF-01 antes da verificação.
- Detalhar e aprovar a estrutura de armazenamento e os metadados das bases
  concretas previstos no RNF-02 e no RT-01 nas etapas correspondentes,
  antes da implementação.
- Definir e aprovar as condições de reprodução do RNF-03 antes das verificações
  da aplicação.
- Definir e aprovar os detalhes de recuperação e registro do RNF-04 antes da
  implementação.
- Definir e aprovar ambiente, dados demonstrativos, operações avaliadas e
  limites de tempo do RNF-05 antes das medições.
- Definir e aprovar arquitetura e convenções específicas do RNF-06 na Etapa 4,
  antes da implementação correspondente.
- Definir e aprovar sistemas concretos, procedimentos de compatibilização,
  unidades de distância, precisão e tolerâncias do RT-02 antes da implementação
  e da preparação dos testes correspondentes.
- Detalhar e aprovar as condições e os parâmetros das regras demonstrativas
  da RN-01 antes da implementação e da preparação dos testes correspondentes.
- Detalhar e aprovar a forma de apresentação da identificação das informações
  simuladas da RN-02 antes da implementação e da preparação dos testes.
- Detalhar e aprovar a lista dos dados necessários, os critérios de
  disponibilidade e a forma de apresentação da RN-03 antes da implementação
  e da preparação dos testes.
- Discutir e aprovar os conteúdos das pequenas unidades da sequência
  registrada no plano de pendências; próxima discussão recomendada: critérios
  complementares de radiação solar e proximidade da rede elétrica para o
  cenário Solar em terreno, com dados, unidades, fundamentação e limitações.
  A proposta ainda depende de aprovação; a Etapa 2 permanece em andamento.
- Discutir e aprovar os demais detalhamentos da Etapa 2.
- Na Etapa 4, escolher stack e versão suportada de Python, avaliando a proposta
  de Streamlit e a separação entre frontend na Vercel e backend no Railway.
- Na Etapa 6, selecionar a região de estudo em Minas Gerais e as fontes públicas.

## Como verificar o ambiente atual

Ainda não existe comando para iniciar a aplicação. No terminal do macOS ou
Linux, a partir da raiz do projeto e com a `.venv` existente:

```bash
source .venv/bin/activate
python --version
python -m pip --version
python -m pip check
git status --short
```

Esses comandos consultam o ambiente e o estado do repositório. Não instalam
pacotes, não criam commits e não publicam arquivos. As instruções de instalação
reproduzível serão detalhadas após a definição da stack.

## Próxima tarefa recomendada

Levantar e discutir no chat os critérios complementares de radiação solar e
proximidade da rede elétrica para o cenário Solar em terreno. Identificar o
que cada medida representará, dados necessários, unidades, referências,
adaptações e limitações; distinguir proximidade geométrica de possibilidade
real de conexão e medida de recurso solar de previsão de geração. Apresentar
uma proposta delimitada antes de qualquer registro, sem importar parâmetros
de outros estudos como limites universais nem criar notas, pesos ou conclusões
ambientais sem fundamentação. Preservar as RN-01 e RN-03 e identificar hipóteses
simuladas. Não alterar arquivos nessa discussão nem antecipar implementação.
Os três critérios iniciais do RF-08 estão definidos, mas sua operacionalização,
interpretação e conversão em notas, bases e parâmetros permanecem pendentes.
As demais regras do RF-06 e os critérios de disponibilidade também continuam
pendentes; esses requisitos não estão encerrados.
A Etapa 2 permanece em andamento; alterações, commits, publicação e
encerramento dependem de autorização.
