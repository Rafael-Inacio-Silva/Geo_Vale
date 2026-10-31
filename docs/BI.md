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

## Página 1 e acesso pelo MVP

[GeoVale — Visão geral das minas](https://lookerstudio.google.com/reporting/3dca8a93-d660-4d28-9f93-e3a3e53ff813/page/BCbCG). Uma única página no Looker Studio (apresentado pelo Google como Data Studio), criada em 31/10/2026 com `minas.csv`: cartões de minas catalogadas e setores analisados, filtro por nome da mina e comparação de município, área minerada em hectares, vegetação nativa em porcentagem e setores. Sem filtro, os cartões mostram 3 minas e 10 setores; somente Horizontes mostra 1 e 5. Os demais CSVs continuam disponíveis para uma etapa posterior.

O tema usa as cores do MVP (`#007f73`, `#00594f`, `#153f3b`, `#ffc329` e `#fafbf8`) e a mesma marca. Os números vêm do CSV, sem nova inferência ou texto gerado por IA. Áreas de influência não são somadas, pois os recortes podem se sobrepor. A porcentagem de vegetação é apresentada por mina (agregação média na tabela), nunca pela soma de percentuais entre minas.

O cabeçalho do MVP tem um link **Painel BI**, que abre essa página de leitura em nova aba, preservando o mapa. O endereço padrão está em `frontend/src/App.tsx`; `VITE_LOOKER_STUDIO_URL` é uma substituição opcional no build (`frontend/.env.example`). O endereço não contém credenciais. As permissões de leitura são controladas no Looker Studio. O relatório permanece restrito à conta proprietária; leitura por qualquer pessoa com o link depende de autorização explícita do responsável.

Os CSVs são uma exportação datada de 29/10/2026, importada pelo conector de upload de arquivos CSV. O link não sincroniza automaticamente os arquivos locais: para renovar os números é preciso exportar e substituir o arquivo na fonte de dados, sem anexar uma segunda cópia das mesmas linhas. As ideias específicas e as demais páginas serão definidas pelo engenheiro depois desta primeira página.
