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

## Decisões e porquês

| Decisão | Por quê | Evidência |
|---|---|---|
| Mesmos cálculos do relatório | O painel não pode divergir do PDF nem do site: o script usa o banco com dados fixos, as funções das fichas e a sugestão salva em `dados/prontos`. | Área minerada, vegetação nativa, APP e ZAS conferidas com a página 1 dos três relatórios. |
| CSV com ponto decimal | Formato padrão, lido direto pelo conector “Upload de arquivo” do Looker Studio. No Google Sheets em português o ponto pode virar separador de milhar. | Teste de leitura dos arquivos. |
| Tabelas longas (`notas_uso`, `cobertura_terra`) | Gráficos de barras e filtros do Looker trabalham melhor com uma linha por categoria. | — |

Para atualizar: `PYTHONPATH=backend .venv-geovale/bin/python ferramentas/exportar_bi.py`.
