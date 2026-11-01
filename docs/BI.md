# Dados para BI (Looker Studio)

Versão 4.9.0, 29/10/2026. `ferramentas/exportar_bi.py` grava em `bi/` seis CSVs com os números já calculados das três minas, para montar um painel no Looker Studio sem dado novo.

| Arquivo | Grão | Conteúdo |
|---|---|---|
| `minas.csv` | 1 linha por mina | Município, coordenadas, processo ANM, tipo de recorte, recorte, área minerada, cava OSM, vegetação nativa, APP, ZAS, barragens, setores, uso predominante (por área) e se há dado de trilhas |
| `setores.csv` | 1 por setor | Área, 1º e 2º uso com nota, margem, estabilidade a ±20%, % em APP, ZAS e UC, cavidades, declividade, vegetação no entorno e distâncias medianas |
| `notas_uso.csv` | 1 por setor e uso | Posição, nota e % onde a lei permite o uso |
| `cobertura_terra.csv` | 1 por mina e classe | Área e % de cada classe MapBiomas no recorte |
| `pesos.csv` | 1 por critério | Peso AHP |
| `fatos_relatorio.csv` | 1 por dado das fichas | Tema, dado, resumo, valor em texto e origem |
| `panorama.csv` | 1 linha por mina | Campos de `minas.csv`, contagens de setores por uso e áreas de cobertura nativa e outras coberturas, consolidadas por `ferramentas/preparar_panorama_bi.py` |

## Decisões e porquês

| Decisão | Por quê | Evidência |
|---|---|---|
| Mesmos cálculos do relatório | O painel não pode divergir do PDF nem do site: o script usa o banco com dados fixos, as funções das fichas e a sugestão salva em `dados/prontos`. | Área minerada, vegetação nativa, APP e ZAS conferidas com a página 1 dos três relatórios. |
| CSV com ponto decimal | Formato padrão, lido direto pelo conector “Upload de arquivo” do Looker Studio. No Google Sheets em português o ponto pode virar separador de milhar. | Teste de leitura dos arquivos. |
| Tabelas longas (`notas_uso`, `cobertura_terra`) | Gráficos de barras e filtros do Looker trabalham melhor com uma linha por categoria. | — |

Para atualizar: `PYTHONPATH=backend .venv-geovale/bin/python ferramentas/exportar_bi.py`.

## Página 1 e acesso pelo MVP

[GeoVale — Visão geral das minas](https://lookerstudio.google.com/reporting/3dca8a93-d660-4d28-9f93-e3a3e53ff813/page/BCbCG). Página única no Looker Studio (apresentado pelo Google como Data Studio), preenchida em 01/11/2026 dentro dos quadros e do desenho preparados pelo responsável pelo projeto. Os cartões apresentam somente os valores, sem subtítulos abaixo deles.

Os cartões, a comparação por mina, o filtro de município, a cobertura e os destaques usam a fonte CSV `GeoVale_Panorama`, com uma linha por mina. A rosca usa `GeoVale_Usos_por_Setor`: combinação externa à esquerda de `GeoVale_Panorama` com `GeoVale_Setores` (`setores.csv`), ligada somente por `mina_id`. A combinação inclui `mina_curta` (nome de exibição Mina), `mina_id` e `municipio` da fonte do panorama, além de `uso_1`, `Record Count` e soma de `area_ha` da fonte de setores. Isso mantém os filtros de mina e município sem multiplicar os totais dos cartões. A métrica da rosca é a soma das contagens de registros dos setores agrupados por `uso_1`. As métricas da tabela de minas não são somadas depois da ligação de um para muitos.

| Quadro | Dados e agregação |
|---|---|
| Minas avaliadas | Contagem de linhas (uma por mina) |
| Setores avaliados | Soma de `setores` |
| Barragens | Soma de `barragens` dos recortes selecionados |
| Área dos recortes | Soma de `recorte_ha`, em hectares |
| Área minerada por mina | Soma de `area_minerada_ha`, por mina; barras com valores |
| Filtrar por município | Lista suspensa nativa sobre `municipio` da fonte `GeoVale_Panorama`, com seleção única e sem métricas/contagens visíveis. Selecionar Nova Lima ou Sabará filtra a lista de minas acima e mantém os demais indicadores sincronizados. O botão Redefinir remove a seleção |
| Uso futuro mais bem avaliado por setor | Rosca nativa: proporção das contagens de setores por `uso_1`. Total de setores no centro; legenda com contagem e hectares de cada alternativa, calculados na fonte do panorama |
| Cobertura da terra | Barra horizontal nativa empilhada a 100%: somas de vegetação nativa e outras coberturas em uma única categoria constante, com os percentuais calculados por razão de somas abaixo da barra |
| Leitura executiva | Três frases calculadas que acompanham os filtros: setores de conservação / total; participação de Horizontes na área minerada selecionada; barragens / quantidade de minas selecionadas |

Sem filtro: **3 minas, 10 setores, 17 registros de barragens e 24.104,9 ha de recortes**. Clique em Nova Lima: **2 minas, 8 setores, 16 registros e 19.574,9 ha**; os usos somam 6 setores de conservação e 2 de ecoturismo. Clique em Horizontes: **1 mina, 5 setores, 10 registros e 15.308,5 ha**, com 3 setores de conservação e 2 de ecoturismo. Esses fluxos foram conferidos na página de leitura. O botão Redefinir restaura o panorama. O gráfico usado para selecionar destaca a seleção; os outros componentes recebem o filtro.

Os números vêm dos CSVs, sem nova inferência ou texto gerado por IA. A soma dos recortes é uma soma de áreas de estudo, **não uma união espacial nem a superfície exclusivamente lavrada**. Recortes podem se sobrepor; a soma de barragens representa ocorrências cadastradas por recorte, **não uma contagem deduplicada de estruturas físicas**. A cobertura é calculada pela soma das classes do CSV, sem somar percentuais entre minas; pequenos desvios de décimos em relação ao recorte decorrem do arredondamento das classes exportadas.

O cabeçalho do MVP tem um link **Painel BI**, que abre essa página de leitura em nova aba, preservando o mapa. O endereço padrão está em `frontend/src/App.tsx`; `VITE_LOOKER_STUDIO_URL` é uma substituição opcional no build (`frontend/.env.example`). O endereço não contém credenciais. As permissões de leitura são controladas no Looker Studio. O relatório permanece restrito à conta proprietária; leitura por qualquer pessoa com o link depende de autorização explícita do responsável.

Os CSVs de origem são uma exportação datada de 29/10/2026. Para renovar a fonte do panorama:

1. Executar `PYTHONPATH=backend .venv-geovale/bin/python ferramentas/exportar_bi.py`.
2. Executar `python3 ferramentas/preparar_panorama_bi.py`.
3. Substituir o arquivo da fonte `GeoVale_Panorama` por `bi/panorama.csv` e o da fonte `GeoVale_Setores` por `bi/setores.csv`, sem anexar cópias das mesmas linhas.

O link do MVP não sincroniza automaticamente os arquivos locais. O script de consolidação recusa minas repetidas, setores incompletos, ausência de cobertura e um novo uso ainda não contemplado no quadro de usos, para impedir uma atualização silenciosamente incompleta. As demais páginas continuam fora desta etapa.

## Cálculos dos destaques e legendas

São campos calculados do próprio Looker, apresentados em cartões no modo dimensão, sem nome do campo, borda ou subtítulo. `CONCAT`, `CAST` e `REPLACE` montam as frases; os números são agregações sobre os dados selecionados, sem geração de texto por IA.

- Conservação: `SUM(conservacao_setores)` de `SUM(setores)` setores.
- Participação de Horizontes: `100 * SUM(CASE WHEN mina_id = "horizontes" THEN area_minerada_ha ELSE 0 END) / SUM(area_minerada_ha)`, arredondada a uma casa decimal. A referência continua sendo Horizontes; se ela não estiver na seleção, sua participação é zero.
- Barragens: `SUM(barragens)` registros em `COUNT_DISTINCT(mina_id)` áreas selecionadas; o texto usa singular quando existe apenas uma área.
- Percentual nativo: `100 * SUM(vegetacao_nativa_ha) / SUM(cobertura_total_ha)`; o percentual de outras coberturas usa o mesmo denominador. Nunca se calcula a média simples dos percentuais das minas.
- Legendas de usos: `SUM(conservacao_setores)` / `SUM(conservacao_ha)` e `SUM(ecoturismo_setores)` / `SUM(ecoturismo_ha)`.

Sem filtro, a rosca corresponde a 7 e 3 setores (70% e 30%); as áreas das alternativas são 2.195,7 ha e 2.009,8 ha. A cobertura corresponde a 72,0% de vegetação nativa e 28,0% de outras coberturas. Os gráficos são componentes nativos do Looker, sem um serviço externo de imagens.

Verificação da correção dos três quadros em 01/11/2026: a exportação CSV da própria rosca, sob seleção de Nova Lima, retornou conservação = 6 e ecoturismo = 2; a exportação da barra retornou uma categoria Cobertura com 14.012,2 ha nativos e 5.563,8 ha de outras coberturas. Os cartões de texto mostraram 6 de 8 setores, 76% de participação de Horizontes, 16 barragens em 2 áreas, 71,6% nativos e 28,4% de outras coberturas. A imagem enviada pelo responsável confirmou a renderização da rosca nativa em seu navegador. No navegador integrado usado para edição, os dois gráficos nativos em iframe não renderizaram; a validação das consultas usou as exportações CSV, além da conferência dos parâmetros e dos textos na página.

A seleção individual de Horizontes também foi conferida nos cartões: 1 mina, 5 setores, 10 barragens, 3 de 5 setores de conservação, participação de Horizontes de 100%, cobertura nativa de 71,1% e outras coberturas de 28,9%. A frase de barragens trata singular/plural conforme a quantidade de minas selecionadas.

O filtro de município foi verificado em 01/11/2026: Nova Lima mostrou somente Horizontes (3.173,3 ha) e Abóboras (1.001,9 ha), com 2 minas e 8 setores; Sabará mostrou somente Trindade (194,5 ha), com 1 mina e 2 setores. O controle substitui a comparação agregada de área por cidade; os dados originais de município continuam na fonte.
