# GeoVale

MVP de caracterização territorial para apoiar a exploração de informações relevantes à ressignificação de áreas pós-mineração. Abre um mapa mundial em **Minas Gerais**, com contorno oficial estadual e uma mina no catálogo: **Horizontes — Vale — Nova Lima/MG**.

Selecionar a mina pelo cartão ou pela bolinha mostra automaticamente seu contorno. O engenheiro ativa **Influência** para conhecer o território maior. O mapa mostra o contorno, a mina sombreada e os seis temas/onze bases somente dentro desse território. Marcar uma camada à direita amplia sua visualização para além da influência; desmarcar volta ao recorte. **Ver relatório**, disponível ao selecionar a mina mesmo sem ativar Influência, abre um PDF GeoVale com mapa, tabelas das onze bases, cenário técnico simulado e inventário. É possível navegar pelas páginas e baixar o mesmo documento. A tela permanece centrada no mapa, sem tabelas de atributos ou instruções de procedimento.

Os dados são consultados automaticamente e guardados por mina em SQLite local. A aplicação conserva todos os atributos dos registros vetoriais recortados e as células dos dois rasters, com fontes, datas e metadados. Novas bases integradas ao catálogo entram no mesmo processamento. Fundos OpenStreetMap/Esri, WMS e trilhas continuam oferecendo exploração visual independente.

## Executar

Python **3.12**, Node **24**. Na raiz:

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

Abra **http://127.0.0.1:8000**. O servidor escuta somente em loopback. Outra porta: `GEOVALE_PORT=8020 python executar.py`. O comando não abre o navegador. O lock Linux é separado; execução Linux não foi conferida. Em desenvolvimento, Vite na porta 5173 encaminha `/api` para a porta 8000.

Internet é necessária para preparar/atualizar dados, fundos e serviços visuais. Reiniciar o servidor conserva os dados já guardados, sem baixar novamente bases ainda válidas. Imagens do mapa continuam dependendo de seus fornecedores.

## Verificar

```bash
PYTHONPATH=backend PYTHONDONTWRITEBYTECODE=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest -q -p no:cacheprovider tests
cd frontend
npm test
npm run build
```

## Organização

- `backend/geovale/api/main.py`: API local, ciclo de preparação e interface compilada.
- `backend/geovale/camadas.py`: catálogo único de visualização e processamento, com onze bases.
- `backend/geovale/fontes_territorio.py`: adaptadores WFS/WCS/ArcGIS, atributos completos, interseção e células.
- `backend/geovale/territorio.py`: preparação automática e persistência por mina/base.
- `backend/geovale/relatorio.py`: PDF padronizado, mapas vetoriais, tabelas, cenário e inventário.
- `dados/cenarios/horizontes.json`: premissas fictícias e referência metodológica do cenário.
- `backend/geovale/influencia.py`: conferência do recorte local e evidências.
- `backend/geovale/mapa.py`, `municipio.py`, `anm.py`, `trilhas.py`: navegação, município, cadastro e trilhas visuais.
- `frontend/src/Influencia.tsx` e `CamadasNaInfluencia.tsx`: botão, camadas recortadas e relatório PDF da mina.
- `dados/minas.json`: catálogo da mina e identificação.
- `dados/influencias`: influência aproximada, snapshot OSM e receita de preparo.
- `ferramentas/preparar_influencia.py`: reprodução local do contorno e sombreado.
- `.local/territorios.sqlite3`: dados gerados localmente; ignorados pelo Git.
- `docs`: [índice da documentação atual](docs/INDICE.md).

## Decisões e limites

O único recorte de caracterização do MVP vem do **contorno externo AII de águas e solos**, Figura 2.3 do parecer FEAM sobre ampliação conjunta Tamanduá/Horizontes. Usá-lo para todos os temas é uma **simplificação declarada do protótipo**, não delimitação temática oficial ou área obrigatória de recuperação. A mina sombreada vem do OpenStreetMap e não certifica perímetro físico atual.

Dados geográficos guardados são resultados calculados das fontes. Um cenário técnico fictício de pós-fechamento, identificado em seção própria, complementa o relatório para demonstrar informações que as camadas não fornecem. As premissas não alteram os dados reais. A atualização automática ocorre a cada 24 horas enquanto o servidor está ligado; falhas têm novas tentativas, mantendo data/estado explícitos. Uma fonte indisponível não vira quantidade zero. Adicionar uma base requer sua configuração no catálogo e adaptador compatível; não existe descoberta automática de todo serviço da internet.

Não há classificação de aptidão, ranking, recomendação de uso, definição de beneficiários, diagnóstico de impactos ou qualidade ambiental. O relevo é regional e antigo; contagens são registros, não riscos ou rios distintos. Acesso público não significa uso ilimitado. O cenário não constitui laudo ou avaliação de segurança. O 3D Google não está integrado.

[Justificativa e roteiro para apresentação](docs/ESCOLHAS_TERRITORIAIS.md), [recorte e evidência](docs/INFLUENCIA.md), [dados automáticos](docs/DADOS_TERRITORIAIS.md), [uso](docs/MANUAL_USO.md), [relatório e cenário](docs/RELATORIO.md).
