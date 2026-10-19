# Estado do projeto — GeoVale

**Atualização:** 19/10/2026.
**Etapa atual:** 0 — Preparação do projeto, em andamento.
**Subetapa atual:** repositório público criado e origin configurado; primeiro envio pendente.

Este documento registra o estado observado nesta entrega. Não há aplicação
executável nem funcionalidades de geoprocessamento, análise multicritério ou
Machine Learning implementadas. A Etapa 1 ainda não foi iniciada.

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
- Remoto `origin` configurado no Git local, sem envio de arquivos.
- README atualizado e versionado com o link do repositório remoto.

## Arquivos relevantes

| Arquivo | Finalidade |
| --- | --- |
| `.gitignore` | Definir exclusões do versionamento. |
| `README.md` | Apresentar objetivo, escopo planejado, limitações e ambiente atual. |
| `docs/ROADMAP.md` | Organizar etapas, entregas e critérios de conclusão. |
| `docs/STATUS.md` | Registrar progresso real, verificações e pendências. |

Os caminhos são relativos à raiz do projeto. Os documentos de requisitos,
arquitetura e decisões ainda não existem; serão criados gradualmente nas etapas
correspondentes. Os arquivos locais excluídos permanecem fora do versionamento.

## Estado do Git

- Branch atual: `main`.
- Histórico anterior a esta entrega: cinco commits locais, listados abaixo.
- Repositório público: [Rafael-Inacio-Silva/Geo_Vale](https://github.com/Rafael-Inacio-Silva/Geo_Vale).
- Remoto `origin`: `https://github.com/Rafael-Inacio-Silva/Geo_Vale.git`.
- O repositório remoto foi criado vazio; nenhum commit local foi enviado.
- Arquivos destinados ao histórico desta preparação: `.gitignore`, `README.md`,
  `docs/ROADMAP.md` e `docs/STATUS.md`.
- Nenhum envio ao GitHub ou implantação realizado.

Commits concluídos antes desta atualização:

| Commit | Mensagem |
| --- | --- |
| `93570f9` | `chore: configura exclusões do versionamento` |
| `de3b305` | `docs: adiciona apresentação inicial do GeoVale` |
| `674d73a` | `docs: adiciona roadmap de desenvolvimento` |
| `14175fe` | `docs: registra estado inicial do projeto` |
| `15e11d0` | `docs: documenta repositório remoto` |

Esta atualização do status tem a mensagem de commit
`docs: atualiza status da integração com GitHub`. Consulte `git log --oneline` para
identificar seu hash e o histórico atualizado, sem depender de contagens fixas
neste documento.

## Verificações realizadas

As verificações abaixo foram executadas durante a preparação em 19/10/2026.
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
| Integração inicial com GitHub | Proprietário, nome, visibilidade pública e tamanho zero confirmados pela consulta ao GitHub; endereço de leitura e envio do origin conferido no Git local. Nenhum push executado. |

O conteúdo deste status foi conferido contra os arquivos existentes, o estado
do Git e o ambiente Python. Os comandos acima foram executados com sucesso.
Resultados de funcionalidades e métricas de ML não existem nesta fase.

## Pendências e problemas conhecidos

- Nenhuma falha foi encontrada nas verificações de preparação executadas.
- Ainda não há suíte de testes, interface, servidor, banco, dados geográficos
  preparados ou modelo de Machine Learning.
- As dependências da aplicação e a compatibilidade da futura stack com o Python
  observado ainda não foram avaliadas.
- A revisão documental e o versionamento inicial foram concluídos; a Etapa 0
  ainda depende da revisão do roadmap com o responsável, da confirmação de
  compreensão da estrutura e da aprovação de encerramento.
- A criação do repositório e a configuração do origin foram autorizadas e
  concluídas. O primeiro envio da branch `main` ainda depende de autorização.
- A permissão efetiva de envio pelo Git local ainda não foi testada.

## Decisões ainda necessárias

- Autorizar o primeiro push dos arquivos e do histórico local para o origin,
  após conferir o conteúdo que será publicado.
- Aprovar o encerramento da Etapa 0 antes de iniciar os requisitos de negócio.
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

Apresentar para autorização o primeiro envio da branch `main` ao origin,
contendo somente os quatro arquivos públicos versionados e o histórico local.
Antes do envio, conferir os arquivos de todo o histórico e as exclusões locais.
Não enviar arquivos de instrução, ambientes virtuais ou segredos. Não usar push
forçado e não alterar outras branches. Após o envio, verificar o resultado e
propor o registro do progresso em uma tarefa separada. O encerramento da Etapa 0
e o início da Etapa 1 continuam sujeitos à aprovação do responsável.
