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

Todos os componentes usam a mesma fonte CSV `GeoVale_Panorama`, com uma linha por mina. Isso permite que cliques em cidade ou mina filtrem os demais quadros sem multiplicar minas, áreas ou barragens por causa das linhas de setores e classes de cobertura.

| Quadro | Dados e agregação |
|---|---|
| Minas avaliadas | Contagem de linhas (uma por mina) |
| Setores avaliados | Soma de `setores` |
| Barragens | Soma de `barragens` dos recortes selecionados |
| Área dos recortes | Soma de `recorte_ha`, em hectares |
| Área minerada por mina / cidade | Soma de `area_minerada_ha`, por mina / município; barras com valores |
| Uso futuro mais bem avaliado por setor | Contagens de setores com conservação/restauração e ecoturismo/lazer em primeiro lugar, por mina; linha de total filtrada |
| Cobertura da terra | Área nativa e demais coberturas em hectares, por mina |
| Leitura executiva | Mina, uso predominante por área e área minerada em hectares |

Sem filtro: **3 minas, 10 setores, 17 registros de barragens e 24.104,9 ha de recortes**. Clique em Nova Lima: **2 minas, 8 setores, 16 registros e 19.574,9 ha**; os usos somam 6 setores de conservação e 2 de ecoturismo. Clique em Horizontes: **1 mina, 5 setores, 10 registros e 15.308,5 ha**, com 3 setores de conservação e 2 de ecoturismo. Esses fluxos foram conferidos na página de leitura. O botão Redefinir restaura o panorama. O gráfico usado para selecionar destaca a seleção; os outros componentes recebem o filtro.

Os números vêm dos CSVs, sem nova inferência ou texto gerado por IA. A soma dos recortes é uma soma de áreas de estudo, **não uma união espacial nem a superfície exclusivamente lavrada**. Recortes podem se sobrepor; a soma de barragens representa ocorrências cadastradas por recorte, **não uma contagem deduplicada de estruturas físicas**. A cobertura é calculada pela soma das classes do CSV, sem somar percentuais entre minas; pequenos desvios de décimos em relação ao recorte decorrem do arredondamento das classes exportadas.

O cabeçalho do MVP tem um link **Painel BI**, que abre essa página de leitura em nova aba, preservando o mapa. O endereço padrão está em `frontend/src/App.tsx`; `VITE_LOOKER_STUDIO_URL` é uma substituição opcional no build (`frontend/.env.example`). O endereço não contém credenciais. As permissões de leitura são controladas no Looker Studio. O relatório permanece restrito à conta proprietária; leitura por qualquer pessoa com o link depende de autorização explícita do responsável.

Os CSVs de origem são uma exportação datada de 29/10/2026. Para renovar a fonte do panorama:

1. Executar `PYTHONPATH=backend .venv-geovale/bin/python ferramentas/exportar_bi.py`.
2. Executar `python3 ferramentas/preparar_panorama_bi.py`.
3. Substituir o arquivo da fonte `GeoVale_Panorama` por `bi/panorama.csv`, sem anexar cópias das mesmas linhas.

O link do MVP não sincroniza automaticamente os arquivos locais. O script de consolidação recusa minas repetidas, setores incompletos, ausência de cobertura e um novo uso ainda não contemplado no quadro de usos, para impedir uma atualização silenciosamente incompleta. As demais páginas continuam fora desta etapa.
