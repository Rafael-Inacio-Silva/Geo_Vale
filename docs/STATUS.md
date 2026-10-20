# Estado do projeto — GeoVale

**Atualização:** 20/10/2026.
**Etapa atual:** 2 — Engenharia de requisitos do sistema, iniciada com autorização em 20/10/2026.
**Subetapa atual:** atores AT-01 e AT-02, definições dos RF-01 a RF-13, RNF-01 a RNF-06, RT-01 a RT-02 e RN-01 a RN-03 aprovadas, documentadas e publicadas; revisões documentais dos seis RNF, dos dois RT e das três RN concluídas; exigência das licenças explícita no RT-01 e classificação da RN-01 detalhada para dados necessários disponíveis e efeitos da indisponibilidade detalhados na RN-03; referência entre RN-01 e RN-03 sincronizada; demais detalhamentos técnicos e verificações da aplicação ainda pendentes.

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
RF-01 a RF-13 foram aprovadas e publicadas. Permanecem pendentes os detalhes
técnicos de entrada, as regras para arquivos com múltiplas áreas e a definição
do sistema de coordenadas adequado, da precisão e da tolerância do cálculo
da área. Para o RF-04, as bases e operações específicas ainda precisam ser
detalhadas. Para o RF-05, medições, tolerâncias e condições dos alertas também
permanecem pendentes. Para o RF-06, as regras de negócio, os parâmetros e o
tratamento de dados ausentes ainda precisam ser especificados. Para o RF-07,
os campos e as regras de validação do cadastro também permanecem pendentes.
Para o RF-08, escalas, limites, validação dos pesos e tratamento de valores
ausentes ainda precisam ser definidos. Para o RF-09, regras de normalização,
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
identificação da regra e da justificativa. Condições e parâmetros das regras
demonstrativas continuam pendentes; a verificação ocorrerá na implementação
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
critérios de aceitação das regras.

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
  pelo menos duas alternativas distintas para iniciar a comparação. Campos
  e regras de validação do cadastro permanecem pendentes; a funcionalidade
  ainda não foi implementada.
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
- Histórico anterior a esta entrega: oitenta e sete commits locais já publicados, listados abaixo.
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

Esta atualização do status tem a mensagem de commit
`docs: registra sincronização entre RN-01 e RN-03 no status`. Consulte `git log --oneline` para
identificar seu hash e o histórico atualizado, sem depender de contagens fixas
neste documento.

## Verificações realizadas

As verificações abaixo foram executadas durante a preparação, a documentação
e a revisão dos requisitos entre 19/10/2026 e 20/10/2026.
São verificações de configuração e documentação; não são testes da aplicação.

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

Os registros de preparação do ambiente Python são históricos. Nesta revisão,
foram conferidos os documentos, os commits e o estado do Git; as verificações
do ambiente Python não foram repetidas.
Resultados de funcionalidades e métricas de ML não existem nesta fase.

## Pendências e problemas conhecidos

- Nenhuma falha foi encontrada nas verificações de preparação executadas.
- Ainda não há suíte de testes, interface, servidor, banco, dados geográficos
  preparados ou modelo de Machine Learning.
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
  Formatos aceitos, limites de entrada e regras de geometria do RF-01 precisam
  ser especificados e aprovados antes de sua implementação e da preparação
  dos arquivos de teste.
- As regras para arquivos com múltiplas áreas do RF-02 precisam ser
  especificadas e aprovadas antes da implementação e da preparação dos
  cenários de teste correspondentes. A dependência do RF-01 permanece aberta.
- Para o RF-03, sistema de coordenadas adequado, precisão e tolerância de
  comparação precisam ser especificados e aprovados antes da implementação
  e da preparação dos testes com área de referência. As pendências dos
  RF-01 e RF-02 permanecem em aberto.
- Para o RF-04, as bases e operações específicas precisam ser detalhadas e
  aprovadas antes da implementação e da preparação do cenário de referência.
  O cruzamento depende da geometria do RF-02, de camadas preparadas e de
  sistemas de coordenadas compatíveis. As pendências anteriores continuam
  em aberto.
- Para o RF-05, medições, tolerâncias e condições dos alertas precisam ser
  especificadas e aprovadas antes da implementação e da preparação dos
  cenários de referência. A dependência do RF-04 e as pendências anteriores
  continuam em aberto.
- Para o RF-06, regras de negócio, parâmetros e tratamento de dados ausentes
  precisam ser especificados e aprovados antes da implementação e da
  preparação dos cenários de teste. A dependência do RF-05 e as pendências
  anteriores permanecem em aberto.
- Para o RF-07, campos e regras de validação do cadastro precisam ser
  especificados e aprovados antes da implementação e da preparação dos
  cenários de teste. A dependência da área identificada pelo RF-02 e as
  pendências anteriores permanecem em aberto.
- Para o RF-08, escalas, limites, validação dos pesos e tratamento de valores
  ausentes precisam ser definidos e aprovados antes da implementação e da
  preparação dos cenários de teste. A dependência do RF-07 e as pendências
  anteriores permanecem em aberto.
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
- Para a RN-01, condições e parâmetros das regras demonstrativas precisam
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

## Decisões ainda necessárias

- Especificar e aprovar os detalhes técnicos pendentes do RF-01 antes de
  implementar a funcionalidade.
- Especificar e aprovar as regras para arquivos com múltiplas áreas do RF-02
  antes da implementação.
- Especificar e aprovar sistema de coordenadas adequado, precisão e tolerância
  de comparação do RF-03 antes da implementação.
- Detalhar e aprovar as bases e operações específicas do RF-04 antes da
  implementação.
- Especificar e aprovar medições, tolerâncias e condições dos alertas do RF-05
  antes da implementação.
- Especificar e aprovar regras de negócio, parâmetros e tratamento de dados
  ausentes do RF-06 antes da implementação.
- Especificar e aprovar campos e regras de validação do cadastro do RF-07
  antes da implementação.
- Definir e aprovar escalas, limites, validação dos pesos e tratamento de
  valores ausentes do RF-08 antes da implementação.
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
- Mapear as pendências para o encerramento da Etapa 2, distinguindo decisões
  sobre o comportamento do sistema de detalhamentos previstos nas etapas
  seguintes; apresentar a proposta de próximas unidades para aprovação.
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

Mapear as pendências necessárias para encerrar a Etapa 2, conferindo o
planejamento, os requisitos e este status. Identificar as decisões sobre o
comportamento do sistema ainda abertas e os detalhamentos previstos nas
etapas seguintes, propondo a sequência de pequenas unidades. Apresentar o
resultado no chat, sem alterar arquivos ou encerrar a etapa nessa revisão.
A Etapa 2 permanece em andamento; futuras alterações, commits, publicação
e encerramento dependem de autorização.
