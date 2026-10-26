# Dependências e execução

## Python 3.12

Dependências diretas: FastAPI 0.159.1, Uvicorn 0.54.0 e Shapely 2.2.0. HTTPX 0.28.1 e pytest 9.1.1 são usados nos testes. Shapely utiliza NumPy e GEOS para validação/simplificação do contorno estadual, validação das linhas municipais e dos polígonos manuais, cadastral ANM e municipal IBGE.

`requirements/compatibilidade.in` declara as dependências diretas. Os locks macOS 15 x86_64 e Linux x86_64 fixam versões transitivas e hashes. Os pacotes sem uso na etapa territorial foram retirados dos arquivos de instalação. A existência de um lock Linux não comprova execução nessa plataforma.

Use um ambiente virtual dedicado. Não substitua o Python nem o ambiente pessoal do usuário.

## Node 24

React 19.3.1, React DOM 19.3.1 e Leaflet 1.9.4. Leaflet.draw **1.0.4** (MIT) para desenho/edição; `@types/leaflet-draw` **1.0.13** na compilação. TypeScript 7.0.2 e Vite 8.3.5 na compilação. Versões e dependências transitivas constam de `frontend/package-lock.json`.

`npm test` verifica a pesquisa no catálogo. `npm run build` verifica os tipos e gera `frontend/dist`. O build é necessário para `python executar.py`. Node não é necessário no processo do servidor depois da compilação.

## Rede e armazenamento

WFS oficial da IDE-Sisema via HTTPS no backend. Tiles OpenStreetMap/Esri e imagens WMS/legendas IDE-Sisema via HTTPS no navegador. WMS usa suporte nativo do Leaflet. Trilhas: ArcGIS REST via HTTPS no backend para geometria e configuração de cores; GeoJSON e legenda sanitizada para o navegador. As duas primeiras leituras usam ThreadPoolExecutor da biblioteca padrão, sem dependência adicional. Desenho/edição usa Leaflet.draw, instalado pelo npm oficial. Sem credenciais dessas fontes no frontend. O cache do contorno existe apenas na memória do processo, por uma hora. Trilhas usam cache de dez minutos, até 16 enquadramentos. O polígono confirmado existe somente na memória da página; a validação POST não grava arquivos. Não há banco de dados nem instalador Selenium.

O papel e a justificativa de cada ferramenta estão em [Ferramentas e justificativas](FERRAMENTAS.md). Este documento reúne as versões e os procedimentos de instalação.

Na versão 3.3.0, a ANM é consultada por HTTPS/ArcGIS REST e o IBGE por sua API de malhas. `urllib`, gzip, threading e cópias defensivas são da biblioteca padrão; não houve nova dependência. Cache ANM de dez minutos, municipal de uma hora. As barras laterais e a coleção de polígonos usam React/Leaflet já instalados.
