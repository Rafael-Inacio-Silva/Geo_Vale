# GeoVale

Mapa territorial com navegação mundial, aberto em **Minas Gerais**, contorno oficial do estado e pesquisa de uma única mina: **Mina Horizontes — Vale — Nova Lima/MG**. A seleção mostra o contorno de Nova Lima pelo IBGE e enquadra município e referência da mina. A seta do cartão revela empresa, município, complexo e dados cadastrais consultados diretamente na ANM (processo, titular, fase e área cadastrada). Cinco temas territoriais permitem sobrepor relevo, água, solos, vegetação/conservação e entorno/infraestrutura, com intensidade ajustável e legendas oficiais. Uma sexta opção mostra **Trilhas de Nova Lima**, de fonte municipal independente, com cores e nomes da configuração oficial e legenda dos traçados no enquadramento. O engenheiro pode **desenhar, ajustar e confirmar várias áreas de estudo independentes**, ou adicionar o polígono cadastral do processo ANM diretamente no mapa.

A interface usa React, TypeScript e Leaflet. A API local usa Python/FastAPI e consulta o WFS público da IDE-Sisema para obter o limite estadual. O fundo cartográfico é carregado por região e zoom, por OpenStreetMap ou Esri World Imagery. Temas da IDE-Sisema são carregados diretamente pelo navegador via WMS, somente quando marcados e para a região visível. A cobertura desses temas é estadual; a navegação de fundo é mundial. As trilhas são consultadas via API local no ArcGIS REST da Prefeitura de Nova Lima, em GeoJSON e somente para a região visível. A confirmação do desenho usa validação geométrica local, sem enviar o polígono aos fornecedores. **É necessário acesso à internet para as fontes geográficas.**

O ponto da Horizontes é uma referência aproximada para navegação, derivada do centroide de um processo minerário vinculado documentalmente ao empreendimento. Não representa um limite físico da mina. Fontes e precisão estão em [Dados geográficos](docs/DADOS_GEOGRAFICOS.md).

## Executar

Python **3.12** e Node **24**. Na raiz do projeto:

```bash
python3.12 -m venv .venv-geovale
source .venv-geovale/bin/activate
python -m pip install --require-hashes -r requirements/compatibilidade-macos15-x86_64.txt
cd frontend
npm ci
npm run build
cd ..
python executar.py
```

Abra **http://127.0.0.1:8000**. O servidor escuta somente em `127.0.0.1`. Para outra porta: `GEOVALE_PORT=8020 python executar.py`. O comando não abre o navegador automaticamente.

O arquivo de dependências Linux x86_64 é separado; execução nessa plataforma não foi verificada nesta entrega. Não use o lock de macOS em outro sistema.

Para desenvolvimento, execute a API e, em outro terminal, `cd frontend && npm run dev`. O Vite usa a porta 5173 e encaminha `/api` à porta 8000.

## Verificar

```bash
PYTHONPATH=backend PYTHONDONTWRITEBYTECODE=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest -q -p no:cacheprovider tests
cd frontend
npm test
npm run build
```

## Organização

As tecnologias utilizadas e suas justificativas estão em [Ferramentas](docs/FERRAMENTAS.md), com uma explicação curta para apresentação.

- `backend/geovale/api`: configuração do mapa, contorno e entrega da interface.
- `backend/geovale/camadas.py`: catálogo fixo: cinco temas estaduais/dez bases e uma camada municipal de trilhas.
- `backend/geovale/mapa.py`: consulta WFS, validação, simplificação visual e cache em memória.
- `backend/geovale/trilhas.py`: consulta municipal, validação e cache temporário.
- `backend/geovale/anm.py`: consulta do processo e polígono cadastral ANM.
- `backend/geovale/municipio.py`: consulta do município selecionado na API IBGE.
- `backend/geovale/area.py`: validação do polígono manual.
- `frontend/src`: navegação, pesquisa, camadas, desenho e identidade visual.
- `dados/minas.json`: cadastro da única mina e proveniência de sua localização.
- `tests` e `frontend/tests`: testes do escopo territorial.
- `docs`: documentação atual; consulte o [índice](docs/INDICE.md).

O acesso à página já abre o mapa. A pesquisa aceita nome atual, nome anterior, empresa e município da mesma mina. Os controles permitem alternar Mapa/Satélite, aproximar/afastar e retornar ao enquadramento estadual. O [manual de uso](docs/MANUAL_USO.md) descreve a operação.

## Escolhas e limites do MVP

Mantido o mapa atual para demonstrar integração de dados públicos, sem contratação Google ou visualizador 3D. Acesso público não significa consumo ilimitado. Os cinco temas são uma seleção documental para o MVP sem validação de especialista da Vale; não fazem diagnóstico, classificação ou recomendação. Datas e escalas variam por base. O relevo Topodata deriva de SRTM de 2000 e não descreve a cava atual. Consulte [justificativa e referências para apresentação](docs/ESCOLHAS_TERRITORIAIS.md) e [proveniência das camadas](docs/DADOS_GEOGRAFICOS.md).

Todas as áreas confirmadas ficam apenas na memória da página; atualizar ou fechar descarta as demarcações. Cada uma pode ser selecionada, ajustada ou removida sem apagar as demais. É um recorte de estudo escolhido pelo usuário, não o limite oficial da mina. Consulte [Área de estudo](docs/AREA_ESTUDO.md) e [Trilhas de Nova Lima](docs/TRILHAS_NOVA_LIMA.md).

O contorno municipal vem da [API oficial de malhas simplificadas do IBGE](docs/LIMITE_MUNICIPAL.md), somente para a mina selecionada. O [polígono ANM](docs/ANM.md) representa o processo minerário, não o perímetro físico da mina; fase cadastral não é situação operacional. A consulta não requer arquivos MG/KMZ nem Selenium.
