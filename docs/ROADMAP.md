# Roadmap do GeoVale

Este documento organiza as entregas do MVP demonstrativo. A
**Etapa 0 — Preparação do projeto foi concluída e aprovada em 19/10/2026**.
A **Etapa 1 — Engenharia de requisitos de negócio está em revisão final**,
com os RNG-01 a RNG-07 aprovados e publicados; seu encerramento ainda depende
de aprovação do responsável. As Etapas 2 a 11 permanecem previstas.
As entregas previstas não representam funcionalidades já implementadas.

## Forma de execução

- Detalhar e aprovar cada etapa antes da implementação correspondente.
- Executar uma pequena unidade por vez: arquivo pequeno, função ou alteração delimitada.
- Apresentar objetivo, arquivos envolvidos, funcionamento, verificação e impacto antes de alterar.
- Verificar os critérios de aceitação e revisar os resultados antes de avançar.
- Trabalhar testes e documentação gradualmente, em unidades próprias quando necessário.
- Submeter commits e operações remotas à autorização do responsável pelo projeto.

A documentação de progresso é mantida em `docs/STATUS.md`.
Este roadmap orienta a sequência e os critérios; não substitui o registro dos testes.

## Etapa 0 — Preparação do projeto

**Objetivo:** preparar o ambiente e estabelecer a organização e as regras de trabalho.

Verificações e entregas já realizadas:

- [x] Orientações locais de desenvolvimento registradas.
- [x] Exclusões configuradas e verificadas no `.gitignore`.
- [x] Git local inicializado na branch `main`.
- [x] Ambiente virtual verificado: Python 3.13.5 e pip 25.1.1.
- [x] README inicial criado e seus comandos executados com sucesso.
- [x] Registro inicial de progresso criado e verificado em `docs/STATUS.md`.
- [x] Diferenças dos arquivos revisadas e primeiros commits propostos para autorização.

Verificações finais concluídas:

- [x] Roadmap revisado e verificado com o responsável pelo projeto.
- [x] Integração com GitHub definida; repositório público criado e primeiros envios concluídos com autorização.
- [x] Compreensão da estrutura confirmada e encerramento aprovado pelo responsável em 19/10/2026.

**Entrega:** ambiente preparado, Git funcional e documentação inicial de orientação.
**Conclusão:** estrutura compreendida, verificações registradas e encerramento aprovado.
Não implementar funcionalidades da aplicação nesta etapa.

## Etapa 1 — Engenharia de requisitos de negócio

**Estado atual:** RNG-01 a RNG-07 aprovados e registrados em `docs/REQUISITOS.md`,
abrangendo problema, objetivo, público-alvo, benefícios esperados, escopo,
limitações e critérios de sucesso do MVP. Revisão final em andamento;
encerramento pendente de aprovação.

**Objetivo:** definir problema, público-alvo, benefícios, escopo e limites do MVP.
**Entrega:** visão e requisitos de negócio em `docs/REQUISITOS.md`, com identificadores `RNG-01`, `RNG-02` etc.
**Conclusão:** problema, objetivo, limites e critérios de sucesso claros e aprovados.

## Etapa 2 — Engenharia de requisitos do sistema

**Objetivo:** especificar atores, requisitos funcionais, não funcionais, técnicos e regras de negócio.
**Entrega:** requisitos identificados por `RF`, `RNF` e `RN`, com prioridades, dependências e critérios de aceitação verificáveis.
**Conclusão:** comportamento esperado e restrições aprovados, sem ambiguidades importantes.

## Etapa 3 — Análise e modelagem

**Objetivo:** transformar os requisitos em casos de uso e fluxos compreensíveis.
**Entrega:** diagrama e descrições de casos de uso, pré-condições, pós-condições, fluxos principais, alternativos e de exceção, além do backlog priorizado.
**Conclusão:** funcionamento do GeoVale explicável e backlog revisado antes da implementação.

## Etapa 4 — Arquitetura e tecnologias

**Objetivo:** selecionar e justificar uma arquitetura simples e modular para o MVP.
**Entrega:** componentes, contratos, fluxo de dados e diretórios em `docs/ARQUITETURA.md`; decisões e alternativas em `docs/DECISOES.md`.
**Conclusão:** stack e responsabilidades aprovadas, separando interface, regras de negócio, geoprocessamento, ML e persistência.

Avaliar as tecnologias candidatas antes de adotá-las. Considerar frontend na
Vercel e backend no Railway, verificando a compatibilidade dessa separação com
a proposta inicial de Streamlit. Definir a aplicação das referências visuais
e da paleta indicadas pelo responsável pelo projeto.

## Etapa 5 — Banco de dados

**Objetivo:** modelar e implementar a persistência necessária, avaliando a proposta inicial de SQLite conforme a arquitetura aprovada.
**Entrega:** entidades, relacionamentos, DER e operações graduais para áreas, arquivos, critérios, análises e resultados, incluindo fontes, versões e parâmetros.
**Conclusão:** uma análise demonstrativa pode ser salva e recuperada, com integridade verificada por testes.

## Etapa 6 — Dados geográficos

**Objetivo:** preparar um cenário real de demonstração em Minas Gerais.
**Entrega:** região selecionada, camadas públicas, pequenos conjuntos de teste e registro de fontes, datas, licenças, formatos, sistemas de coordenadas e limitações.
**Conclusão:** arquivos conferidos no QGIS, carregados e analisados corretamente; qualquer perímetro demonstrativo identificado como tal.

## Etapa 7 — Desenvolvimento incremental das funcionalidades

**Objetivo:** implementar o fluxo principal sem depender do Machine Learning.

| Ordem | Funcionalidade prevista |
| --- | --- |
| 7.1 | Envio e validação do arquivo geográfico. |
| 7.2 | Leitura do arquivo e identificação da área. |
| 7.3 | Cálculo da extensão do terreno. |
| 7.4 | Cruzamento com as bases geográficas. |
| 7.5 | Identificação de distâncias, sobreposições e alertas. |
| 7.6 | Aplicação de regras de negócio demonstrativas. |
| 7.7 | Cadastro e seleção de alternativas de uso futuro. |
| 7.8 | Definição de critérios, notas e pesos. |
| 7.9 | Cálculo multicritério por soma ponderada. |
| 7.10 | Apresentação dos resultados no dashboard. |
| 7.11 | Persistência e consulta das análises. |
| 7.12 | Exportação de relatório. |

Cada subetapa terá critérios de aceitação e cenários válidos, inválidos e de erro,
definidos antes da implementação. Uma subetapa pode exigir várias unidades pequenas.

**Entrega:** fluxo principal funcional com dados demonstrativos.
**Conclusão:** um usuário consegue concluir o fluxo completo, com os testes relacionados executados e resultados registrados.

## Etapa 8 — Machine Learning

**Objetivo:** integrar uma Árvore de Decisão demonstrativa para estimar aptidão física.
**Entrega:** alvo e atributos definidos, origem dos dados e rótulos documentada, conjuntos de treino e teste separados, modelo avaliado e previsão integrada como entrada multicritério.
**Conclusão:** o modelo recebe atributos, retorna previsões e permite reproduzir os testes; limitações registradas explicitamente.

Dados sintéticos demonstram o funcionamento técnico e não comprovam capacidade
preditiva no mundo real. A previsão não substitui restrições eliminatórias.

## Etapa 9 — Testes e garantia da qualidade

**Objetivo:** complementar os testes contínuos com a validação final do sistema.
**Entrega:** relatório de testes unitários, de integração e do fluxo completo, incluindo entradas inválidas, cálculos espaciais, pesos, persistência, relatórios, segurança, limitações do ML e desempenho básico observado.
**Conclusão:** critérios de aceitação atendidos, resultados reais registrados e problemas remanescentes documentados.

## Etapa 10 — Implantação e documentação final

**Objetivo:** disponibilizar uma versão reproduzível para demonstração.
**Entrega:** dependências e ambientes preparados, instruções de instalação e execução, documentação revisada e versão final preparada para publicação autorizada.
**Conclusão:** outra pessoa consegue instalar e executar o sistema seguindo o repositório, com execução conferida a partir de instalação limpa e implantação verificada conforme a arquitetura aprovada.

## Etapa 11 — Demonstração e entrega

**Objetivo:** preparar a apresentação técnica para o gestor da Vale.
**Entrega:** cenário e arquivo geográfico de exemplo, roteiro do fluxo completo, relatório exportado e explicações sobre arquitetura, banco, dificuldades, decisões, limitações e possibilidades de evolução.
**Conclusão:** demonstração ensaiada com mapa, análise geográfica, previsão de ML, comparação multicritério, dashboard e relatório funcionando no cenário escolhido.

## Regras transversais de conclusão

- Identificar fontes geográficas reais e distinguir dados, notas e regras simulados.
- Aplicar restrições eliminatórias separadamente das pontuações multicritério.
- Não apresentar previsões sintéticas como avaliações ambientais confiáveis.
- Não substituir decisões de especialistas nem avaliações legais, ambientais ou de segurança.
- Informar somente testes executados; registrar verificações pendentes e seus motivos.
- Registrar mudanças de escopo e decisões em tarefas aprovadas, sem antecipar etapas.
