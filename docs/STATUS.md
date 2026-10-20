# Estado do projeto — GeoVale

**Atualização:** 20/10/2026.
**Etapa atual:** 1 — Engenharia de requisitos de negócio, em andamento.
**Subetapa atual:** RNG-01 a RNG-06 validados, documentados e publicados; critérios de sucesso ainda pendentes.

Este documento registra o estado observado nesta entrega. Não há aplicação
executável nem funcionalidades de geoprocessamento, análise multicritério ou
Machine Learning implementadas. A Etapa 0 foi concluída e aprovada em
19/10/2026. A Etapa 1 foi iniciada com autorização do responsável; o problema
de negócio, o objetivo do sistema, o público-alvo, os benefícios esperados e
o escopo e as limitações do MVP foram validados até o momento. Os benefícios
são pretendidos e ainda dependem de verificação na demonstração. O ML integra
o escopo do MVP final, com desenvolvimento previsto na Etapa 8; ainda não foi
implementado.

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
- GeoVale incluído no README do perfil público, seguindo o padrão dos demais
  projetos e identificado como em desenvolvimento.

## Arquivos relevantes

| Arquivo | Finalidade |
| --- | --- |
| `.gitignore` | Definir exclusões do versionamento. |
| `README.md` | Apresentar objetivo, escopo planejado, limitações e ambiente atual. |
| `docs/ROADMAP.md` | Organizar etapas, entregas e critérios de conclusão. |
| `docs/STATUS.md` | Registrar progresso real, verificações e pendências. |
| `docs/REQUISITOS.md` | Registrar os RNG-01 a RNG-06 aprovados e os demais requisitos discutidos gradualmente. |

Os caminhos são relativos à raiz do projeto. O documento de requisitos está
em elaboração incremental; arquitetura e decisões ainda não possuem documentos
próprios e serão tratadas nas etapas correspondentes. Os arquivos locais
excluídos permanecem fora do versionamento.

## Estado do Git

- Branch atual: `main`.
- Histórico anterior a esta entrega: vinte commits locais já publicados, listados abaixo.
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

Esta atualização do status tem a mensagem de commit
`docs: registra conclusão das limitações no status`. Consulte `git log --oneline` para
identificar seu hash e o histórico atualizado, sem depender de contagens fixas
neste documento.

## Verificações realizadas

As verificações abaixo foram executadas durante a preparação e a documentação
inicial dos requisitos entre 19/10/2026 e 20/10/2026.
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
| README do perfil | Uma entrada do GeoVale adicionada no padrão existente, com funcionalidades apresentadas como previstas; conteúdo publicado conferido e demais entradas preservadas. |

O conteúdo deste status foi conferido contra os arquivos existentes, o estado
do Git e o ambiente Python. Os comandos acima foram executados com sucesso.
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
- A Etapa 1 está em andamento. Os critérios de sucesso do MVP ainda precisam
  ser detalhados e validados; o encerramento da etapa não foi solicitado.
- Os benefícios registrados no RNG-04 ainda serão verificados na demonstração;
  não há medições de ganhos de tempo ou custo nesta fase.
- Os resumos de andamento do README e do roadmap ainda refletem a preparação;
  sua sincronização será tratada em unidades próprias. Este status e o documento
  de requisitos registram o progresso atual.

## Decisões ainda necessárias

- Definir e validar os critérios de sucesso como próxima pequena unidade da
  Etapa 1 (proposta de identificador RNG-07), antes de registrá-los como aprovados.
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

Propor e discutir no chat o RNG-07 — Critérios de sucesso do MVP, tomando
o objetivo, os benefícios, o escopo e as limitações aprovados como referência.
Definir evidências verificáveis para avaliar a demonstração, sem declarar
resultados ou métricas ainda não obtidos. Validar a formulação com o responsável
antes de propor sua inclusão em `docs/REQUISITOS.md`. Não alterar arquivos,
encerrar a Etapa 1 ou avançar de etapa automaticamente. Documentação, commits e
envios continuam sujeitos às aprovações correspondentes.
