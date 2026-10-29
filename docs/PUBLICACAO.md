# Publicação (Vercel + Render)

Versão 4.7.0, 29/10/2026. A interface fica na Vercel e o backend no Render, os dois em planos gratuitos. A Vercel repassa `/api/*` ao Render, então a interface continua chamando a API no mesmo endereço, como no computador local. O Render também serve a interface, o que dá um segundo endereço completo se a Vercel falhar.

- Site: https://geo-vale.vercel.app
- Backend (e endereço reserva): https://geovale.onrender.com

## Passos

1. **Render (uma vez):** conta com "Sign in with GitHub" → New → Blueprint → repositório Geo_Vale. O `render.yaml` cria o serviço `geovale` (Docker, plano Free) e pede o valor de `OPENAI_API_KEY`, que fica só no Render.
2. **Atualizações:** cada push na `main` gera nova imagem no Render (`autoDeploy`).
3. **Vercel (uma vez):** Add New → Project → repositório Geo_Vale → Root Directory `frontend`. O `frontend/vercel.json` repassa `/api/*` ao Render e devolve `index.html` nas demais rotas.
4. **Resultado padrão pronto:** ao trocar o banco, as réguas, os pesos AHP ou o relatório, rodar `PYTHONPATH=backend .venv-geovale/bin/python ferramentas/gerar_prontos.py [mina ...]` (sem argumento, todas as minas) e versionar `dados/prontos/`.
5. **Antes de apresentar:** abrir o endereço do Render um ou dois minutos antes; no plano Free ele dorme após 15 minutos sem uso e leva cerca de um minuto para acordar.

## Decisões e porquês

| Decisão | Por quê | Evidência |
|---|---|---|
| Render Free para o backend | Gratuito, 512 MB de memória, deploy por Dockerfile a partir do GitHub. O backend usa cerca de 220 MB no pico (PDF com IA e sugestão). | Medição local em 29/10/2026: pico de 220,8 MB de memória residente. |
| Não Railway | Sem plano gratuito permanente para este backend: crédito de teste único, plano Free com US$ 1 de recursos por mês e Hobby com mínimo de US$ 5 mesmo parado. | [Railway Pricing](https://docs.railway.com/pricing), consultado em 29/10/2026. |
| Não Hugging Face Spaces | Contas novas têm cota zero de CPU gratuita para Spaces Docker: o Space foi criado e convertido para Docker, mas não pôde ser ligado (403, "cpu-basic quota limit"). | Tentativa de 29/10/2026; [relatos no fórum](https://discuss.huggingface.co/t/free-cpu-basic-quota-is-0-on-new-account/180764). |
| Vercel Hobby para a interface | Gratuita para uso pessoal; a interface é estática (Vite). | Plano Hobby. |
| Repasse `/api/*` em vez de CORS | A interface chama a API por caminho relativo em vários pontos (dados, PDF, páginas da prévia, vídeo); o repasse evita mudar o código e expor outra origem. A Vercel espera até 120 s pelo backend; no Render o primeiro PDF com IA leva cerca de 70 s (CPU do plano Free), e os seguintes saem do cache. | [CDN origin timeout increased to two minutes](https://vercel.com/changelog/cdn-origin-timeout-increased-to-two-minutes); teste local: 30,4 s; pela Vercel em 29/10/2026: 69,2 s. |
| Dados fixos (`GEOVALE_DADOS_FIXOS=1`) | Na demonstração, uma nova coleta dependeria dos servidores do Estado, que ficaram fora do ar em 28/10. O banco coletado (`deploy/territorios.sqlite3`, 3,9 MB, 18 de 18 bases) vai na imagem como retrato datado: nada vence nem é recoletado, e o relatório mantém as datas de consulta. | Teste com o banco de 27/10: 18 de 18 bases prontas, nenhuma coleta, PDF e vídeo servidos. |
| Contorno de Nova Lima salvo (`dados/municipios/3144805.geojson`) | O serviço de malhas do IBGE não responde ao servidor nos EUA (503 após 15 s), embora responda do Brasil em 0,2 s; no ar, o mapa mostrava “Contorno de Nova Lima indisponível”. Com dados fixos, a malha salva é lida e conferida pelas mesmas regras; a data de consulta é a do arquivo. As demais fontes ao vivo (limite de MG, trilhas, ANM) respondem do Render. | Teste no Render em 29/10/2026. |
| Sugestão, explicação e relatório padrão prontos (`dados/prontos/`) | Com dados fixos e pesos AHP, o resultado padrão é sempre o mesmo; no Render ele levava 45 s (sugestão) e 70 s (PDF) a cada vez que o servidor acordava. Gerados antes com o mesmo banco da imagem e a IA, saem na hora. Pesos ajustados continuam calculados ao vivo. O texto da IA do padrão fica fixo, com a data em que foi gerado, como os dados. | `ferramentas/gerar_prontos.py` confere que o banco local é o da imagem e que a explicação veio da IA; teste da API sem cálculo. |
| Interface compilada dentro da imagem | O Render monta a imagem a partir do GitHub, onde `dist/` não é versionado. | `Dockerfile`, etapa `interface`. |
| Chave da OpenAI como variável secreta do Render | O backend lê `OPENAI_API_KEY` do ambiente quando não há `.local/ia.env`; a chave não entra em arquivos, imagem nem Git. Nunca como variável pública: no Hugging Face ela chegou a ser salva como variável pública, foi apagada e revogada. | `comentarios.py`; `render.yaml` com `sync: false`. |
| `libexpat1` e `libstdc++6` na imagem | O rasterio traz o GDAL embutido, mas ele usa essas bibliotecas do sistema; a imagem Python slim não traz a libexpat, e o primeiro deploy caiu com `ImportError: libexpat.so.1`. | Log do Render, 29/10/2026; varredura das bibliotecas exigidas pela wheel do rasterio. |
| Dependências travadas para Linux | O servidor é Linux; o lock do macOS não serve. | `requirements/compatibilidade-linux-x86_64.txt`, com hashes. |

## Limites

- O plano Free do Render dorme após 15 minutos sem acesso e leva cerca de um minuto para acordar.
- Com pesos ajustados, a sugestão e o relatório são calculados ao vivo: logo depois de acordar, cerca de 45 s e 70 s.
- Os mapas de fundo e as camadas temáticas continuam vindo ao vivo dos seus fornecedores (OpenStreetMap, Esri, IDE-Sisema).
- O endereço é público; não há login.
- O retrato do banco é de 27/10/2026; para atualizar, coletar localmente e trocar `deploy/territorios.sqlite3`.
