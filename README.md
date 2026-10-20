# GeoVale

**Sistema de Apoio à Decisão para Uso Futuro de Áreas Pós-Mineração**

Projeto demonstrativo em desenvolvimento para apoiar a comparação de possíveis
usos futuros de áreas pós-mineração, combinando geoprocessamento, análise de
dados, análise multicritério e Machine Learning demonstrativo. O modelo será
integrado, testado e documentado na versão final do MVP.

## Objetivo

Organizar informações sobre uma área de estudo e comparar alternativas de uso
futuro de forma compreensível e rastreável, permitindo identificar as fontes,
os parâmetros e as limitações de cada análise.

O MVP será desenvolvido gradualmente, com documentação e verificação de cada
entrega, priorizando simplicidade e facilidade de manutenção.

## Fluxo planejado

As funcionalidades abaixo representam o escopo previsto e ainda não estão
implementadas:

1. Enviar e validar um arquivo geográfico da área de estudo.
2. Analisar características do terreno e cruzar camadas geográficas públicas.
3. Identificar sobreposições, distâncias, alertas e restrições eliminatórias.
4. Comparar alternativas de uso por critérios, notas e pesos definidos.
5. Apresentar mapa, características e ranking em um dashboard.
6. Exportar um relatório com resultados, fontes, parâmetros e limitações.

Após o fluxo principal funcionar, será desenvolvida e integrada, na Etapa 8,
uma Árvore de Decisão demonstrativa para estimar aptidão física como uma das
entradas da análise multicritério. O ML fará parte da demonstração final do MVP.

## Estado atual

A **Etapa 1 — Engenharia de requisitos de negócio foi concluída e teve seu
encerramento aprovado em 20/10/2026**. A Etapa 0 foi concluída e aprovada em
19/10/2026. A Etapa 2 — Engenharia de requisitos do sistema ainda não foi
iniciada e depende de autorização.

Os requisitos de negócio **RNG-01 a RNG-07** foram aprovados e registrados em
[docs/REQUISITOS.md](docs/REQUISITOS.md): problema, objetivo, público-alvo,
benefícios esperados, escopo, limitações e critérios de sucesso do MVP.

- Repositório Git local inicializado na branch `main`.
- Exclusões de arquivos locais configuradas no `.gitignore`.
- Ambiente virtual Python existente e verificado.
- Nenhuma funcionalidade da aplicação implementada.
- Repositório público [Rafael-Inacio-Silva/Geo_Vale](https://github.com/Rafael-Inacio-Silva/Geo_Vale)
  criado no GitHub e configurado como remoto `origin` no Git local.
- Nenhum serviço implantado.

A arquitetura, as bibliotecas e as versões das dependências da aplicação ainda
serão avaliadas e documentadas. Não há interface, servidor ou suíte de testes
da aplicação para executar neste momento.

## Verificação do ambiente local

Na preparação inicial, foram verificados Python **3.13.5** e pip **25.1.1**.
Essas versões descrevem o ambiente observado; a versão de Python suportada pelo
projeto ainda será definida junto às dependências.

No terminal do macOS ou Linux, a partir da raiz do projeto e com a pasta `.venv`
já existente, ative o ambiente e confira o interpretador e o gerenciador de pacotes:

```bash
source .venv/bin/activate
python --version
python -m pip --version
python -m pip check
```

A ativação seleciona o Python do ambiente virtual para a sessão do terminal.
O comando `pip check` verifica a compatibilidade declarada entre os pacotes
instalados; ele não substitui os testes da aplicação.

Somente o pip estava instalado na verificação inicial. As instruções completas
de instalação e execução serão adicionadas quando a stack for definida.

## Limitações e uso responsável

- O sistema tem finalidade demonstrativa e de apoio à decisão.
- Os dados geográficos deverão ter fontes, datas, licenças e limitações registradas.
- Uma área demonstrativa não deverá ser apresentada como perímetro oficial de mina.
- Regras, notas e dados simulados deverão ser identificados explicitamente.
- Restrições eliminatórias deverão ser aplicadas separadamente das pontuações;
  uma pontuação alta não poderá compensar uma restrição eliminatória.
- Treinamento com dados sintéticos poderá demonstrar o funcionamento do algoritmo,
  mas não comprovará capacidade preditiva em áreas reais.
- Os resultados não substituirão avaliações de especialistas, ambientais, legais
  ou de segurança, nem constituirão autorização para uso de uma área.

## Evolução prevista

A próxima etapa prevista é o detalhamento dos requisitos do sistema, seguido
pela modelagem e pela arquitetura. A implementação seguirá com persistência,
dados geográficos, funcionalidades do fluxo principal, Machine Learning,
validação final, implantação e preparação da demonstração.
