# GeoVale

MVP local de apoio à comparação de usos futuros de áreas pós-mineração. **Geoprocessamento + AHP + TOPSIS**, com dados públicos reais e regras exploratórias explícitas. Não utiliza previsão por Machine Learning.

Ao abrir o site, o usuário envia uma poligonal GeoJSON do próprio computador, visualiza o contorno sobre uma imagem aérea, analisa o território, define prioridades e compara **Agricultura, Uso florestal e Recreação em áreas abertas**. Pode salvar a comparação e baixar dois relatórios HTML da mesma revisão: simples e técnico.

**Alcance:** ordenação relativa para aprofundar estudos. Não determina viabilidade, segurança, autorização, custos ou aceitação social. Os parâmetros do protótipo ainda não foram validados por especialistas. A literatura fundamenta o método; não valida as nossas notas ou os resultados destas minas.

## Mapas reais para envio manual

| Mina / licença pública | Recorte de operações | Dados preparados |
|---|---:|---|
| [Rapatee — IL_006](dados/demonstracao/il_006/area.geojson) | 162,29 ha | Contorno, relevo, cobertura 2024, fotografia aérea |
| [Burning Star 3 — IL_071](dados/demonstracao/il_071/area.geojson) | 530,55 ha | Contorno, relevo, cobertura 2024, fotografia aérea |

A entrada é feita exclusivamente pelo envio do arquivo do computador. Para a apresentação, os dois arquivos estão no computador em `~/Desktop/Mapas GeoVale/`: `Rapatee.geojson` e `Burning Star 3.geojson`. Clique em **Enviar GeoJSON** e escolha o arquivo.

São uniões de limites de operações do GeoMine/OSMRE em Illinois, EUA; não certificam a totalidade cadastral de uma mina, nem representam uma mina da Vale. A jornada completa reconhece estas duas geometrias, inclusive se o arquivo for renomeado. Outras poligonais válidas são exibidas, mas precisam de preparação de fontes para serem analisadas. Fotografias e rasters já estão no pacote: a apresentação não depende de consultas externas.

## Executar

Python **3.12** e Node **24**. Execute a partir da raiz do projeto; use um ambiente virtual dedicado, sem apagar seu ambiente existente.

```bash
python3.12 -m venv .venv-mcda
source .venv-mcda/bin/activate
python -m pip install --require-hashes -r requirements/compatibilidade-macos15-x86_64.txt
cd frontend
npm ci
npm run build
cd ..
python executar.py
```

Abra **http://127.0.0.1:8000**. A interface e a API usam a mesma origem e não há tela de login. Para outra porta: `GEOVALE_PORT=8020 python executar.py`. O servidor escuta somente no computador local. O build da interface é obrigatório antes de executar. O comando não abre o navegador automaticamente.

O lock macOS foi usado no ambiente Python 3.12 de verificação. Existe lock Linux x86_64, mas **esta nova versão não foi executada em Linux**. Outros sistemas exigem ambiente compatível; não utilize o lock macOS em Windows.

Para desenvolvimento, execute a API e, em outro terminal, `cd frontend && npm run dev`: o Vite encaminha `/api` para a porta 8000. Não coloque credenciais no frontend. Não há configuração de implantação pública nesta versão.

## Verificar

```bash
PYTHONPATH=backend PYTHONDONTWRITEBYTECODE=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest -q -p no:cacheprovider tests
PYTHONPATH=backend python validacao/verificar_pacotes.py
cd frontend
npm test
npm run build
```

## Organização

- `backend/geovale/geografia`: validação da entrada.
- `backend/geovale/decisao`: extração territorial, AHP, TOPSIS e sensibilidade.
- `backend/geovale/mvp`: API, sessão, revisões SQLite e relatórios.
- `frontend`: React e Leaflet; interface sem painéis de bastidores.
- `dados/demonstracao`: dois pacotes reais, com fontes, datas e hashes.
- `dados/qgis`: GeoPackage e projeto auxiliar para inspeção no QGIS.
- `tests` e `validacao`: verificações automatizadas e inspeção dos pacotes.
- `.local`: banco e arquivos gerados localmente, fora do Git.

Verificação em macOS: **119 testes Python e 2 testes frontend aprovados**, TypeScript e build Vite aprovados, integridade dos dois pacotes conferida. Detalhes em [Validação](docs/VALIDACAO.md).

Leia [Metodologia](docs/METODOLOGIA.md), [Roteiro de apresentação](docs/DEMONSTRACAO.md) e [Índice da documentação](docs/INDICE.md).
