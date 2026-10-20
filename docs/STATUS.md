# Estado do projeto — GeoVale

**Atualização:** 20/10/2026.
**Etapa atual:** 2 — Engenharia de requisitos do sistema, iniciada com autorização em 20/10/2026.
**Subetapa atual:** atores AT-01 e AT-02 e definições dos RF-01 a RF-04 aprovados, documentados e publicados; detalhes técnicos de entrada, múltiplas áreas, cálculo da área e cruzamento geográfico ainda pendentes.

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
RF-01 a RF-04 foram aprovadas e publicadas. Permanecem pendentes os detalhes
técnicos de entrada, as regras para arquivos com múltiplas áreas e a definição
do sistema de coordenadas adequado, da precisão e da tolerância do cálculo
da área. Para o RF-04, as bases e operações específicas ainda precisam ser
detalhadas.

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

## Arquivos relevantes

| Arquivo | Finalidade |
| --- | --- |
| `.gitignore` | Definir exclusões do versionamento. |
| `README.md` | Apresentar objetivo, escopo planejado, limitações e ambiente atual. |
| `docs/ROADMAP.md` | Organizar etapas, entregas e critérios de conclusão. |
| `docs/STATUS.md` | Registrar progresso real, verificações e pendências. |
| `docs/REQUISITOS.md` | Registrar os RNG-01 a RNG-07, os atores AT-01 e AT-02 e as definições dos RF-01 a RF-04 aprovados; detalhamento técnico e demais requisitos serão tratados em unidades posteriores. |

Os caminhos são relativos à raiz do projeto. O documento de requisitos está
em elaboração incremental; arquitetura e decisões ainda não possuem documentos
próprios e serão tratadas nas etapas correspondentes. Os arquivos locais
excluídos permanecem fora do versionamento.

## Estado do Git

- Branch atual: `main`.
- Histórico anterior a esta entrega: trinta e nove commits locais já publicados, listados abaixo.
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

Esta atualização do status tem a mensagem de commit
`docs: registra definição e pendências do RF-04 no status`. Consulte `git log --oneline` para
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
- A Etapa 2 foi iniciada; atores e definições dos RF-01 a RF-04 foram documentados.
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
- Demais requisitos funcionais, não funcionais, técnicos, regras de negócio,
  prioridades, dependências e critérios de aceitação serão detalhados em
  pequenas unidades.
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
- Discutir e aprovar os demais requisitos do sistema em pequenas unidades;
  próxima proposta: RF-05 — Identificação de distâncias, sobreposições e alertas.
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

Apresentar para discussão o RF-05 — Identificação de distâncias, sobreposições
e alertas, com ator, descrição, prioridade, dependências e critérios de
aceitação.
Após a aprovação do conteúdo, registrar somente essa pequena unidade em
`docs/REQUISITOS.md`, preservando os requisitos e os atores existentes.
Manter as pendências dos RF-01 a RF-04 explícitas. Alterações, commits e
publicação dependem de autorização. Não implementar funcionalidades nesta
unidade.
