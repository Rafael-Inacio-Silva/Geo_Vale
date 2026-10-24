# Ambiente e dependências

Verificação da versão 2.0: Python 3.12.15 em macOS x86_64; Node 24.22.1. Reutilizado ambiente de provas compatível, sem apagar ou modificar o ambiente virtual do PyCharm.

Dependências diretas estão em `requirements/compatibilidade.in`; os dois locks preservam versões e hashes de distribuição anteriormente levantados. Foram retirados scikit-learn, SciPy, joblib, threadpoolctl e cloudpickle da solução ativa, pois não são usados nesta rota. Não executar scripts/modelos arquivados com este conjunto reduzido.

Python: FastAPI 0.159.1, Uvicorn 0.54.0, Shapely 2.2.0, PyProj 3.8.0, GeoPandas 1.2.0, Rasterio 1.5.2, NumPy 2.5.4, Jinja2 3.1.6, Matplotlib 3.11.2, python-multipart 0.0.32. Testes com pytest 9.1.1 e HTTPX 0.28.1. Versões transitivas e hashes: arquivos de lock.

Frontend: React/ReactDOM 19.3.1, Leaflet 1.9.4, TypeScript 7.0.2, Vite 8.3.5. `package-lock.json` preserva dependências; somente a versão do aplicativo mudou para 2.0.0. `npm ci` instala conforme o lock. Não há APIs de mapas que exijam chave.

A execução nova foi verificada em macOS. O lock Linux não significa execução em Linux. QGIS não estava instalado: GeoPackage foi lido por GeoPandas; o projeto auxiliar não foi aberto na interface QGIS.

A suíte emite um aviso de depreciação do TestClient/HTTPX pela versão Starlette. Isso não falhou os testes, mas merece revisão futura conjunta das dependências; não foi introduzida atualização de framework fora desta entrega.
