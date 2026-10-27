# Dependências e execução

## Python 3.12

Diretas: FastAPI 0.159.1, Uvicorn 0.54.0, Shapely 2.2.0, Rasterio 1.5.0 e NumPy 2.5.4, mais ReportLab 4.4.9 para PDF. HTTPX 0.28.1 e pytest 9.1.1 e pypdf 6.10.0 nos testes de PDF. Rasterio utiliza GDAL empacotado no wheel; Shapely utiliza GEOS. SQLite, urllib, threading, hashlib, zlib, json e ThreadPoolExecutor são da biblioteca padrão.

`requirements/compatibilidade.in` declara as versões diretas. Locks macOS 15 x86_64 e Linux x86_64 fixam transitivas/hashes. Rasterio acrescenta affine 3.0.1, attrs 26.1.0, cligj 0.7.2 e pyparsing 3.3.3; certifi, click e NumPy já fazem parte do ambiente. Os hashes foram obtidos do PyPI oficial. A existência de lock Linux não comprova execução nessa plataforma.

Use o ambiente virtual dedicado, sem substituir o Python pessoal. Instale com `pip install --require-hashes -r requirements/compatibilidade-macos15-x86_64.txt` no macOS suportado. Não é necessário instalar QGIS ou GDAL pelo sistema para os wheels usados nesta entrega.

ReportLab acrescenta Pillow 12.3.0 e charset-normalizer 3.5.2, fixados com hashes do PyPI oficial. As fontes Vera distribuídas pelo ReportLab são incorporadas ao PDF.

## Node 24

React/React DOM 19.3.1 e Leaflet 1.9.4, com pdfjs-dist 6.4.299 no visualizador sob demanda. TypeScript 7.0.2 e Vite 8.3.5 para compilação. Dependências atuais em `frontend/package.json` e lock npm. `npm test` confere pesquisa; `npm run build` confere tipos e gera frontend/dist. Node não precisa rodar para servir o build pelo backend.

## Dados e rede

Internet para fontes geográficas e atualizações. Tiles/WMS/legendas chegam ao navegador; o backend prepara WFS/WCS/ArcGIS e guarda dados por mina em `.local/territorios.sqlite3`, ignorado pelo Git. Reiniciar conserva o banco. Atualização/repetição só ocorre enquanto o servidor está ligado. Não há credenciais externas no frontend ou ativação de faturamento Google. [Método e limites](DADOS_TERRITORIAIS.md).
