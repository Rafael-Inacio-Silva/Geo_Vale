# Validação do território e relatório JSON

Revisão de 26/10/2026, versão **4.0.0**, macOS, Python 3.12 e Node 24. Servidor local em `127.0.0.1:8000`, sem implantação pública.

## Verificações automatizadas

**84 testes Python aprovados**, incluindo catálogo de mapa, ANM sem geometria, município, trilhas, influência, atributos completos, rasters, persistência e exportação. **2 testes Node aprovados**; TypeScript e build Vite aprovados. Instalação Python com hashes conferida por dry-run do lock macOS e `pip check`; Linux não foi executado.

Os casos territoriais verificam recorte irregular em vez de bbox, partes contadas uma vez, todos os campos/nulos/IDs, rejeição de truncamento/CRS/invalidade, classes do estilo padrão, grade/células/NoData, persistência entre instâncias, nova base automática, invalidação por recorte, isolamento por mina, retenção explícita de último dado/falha, repetição somente da base pendente e início pelo lifespan sem clique. Exportação verifica onze bases independentemente de seletores, attachment, matriz nativa/`null`, fonte/evidência, impedimento de base ausente/erro/vencida/recorte alterado e ausência de consultas externas no download. Trilhas visuais preservam nomes/cores ao intersectar o polígono e excluem contato apenas pontual.

Há avisos de depreciação Starlette/TestClient/HTTPX e Rasterio/Affine/NumPy, sem falhas. Não se alteraram outras dependências para silenciar esses avisos.

## Dados reais e exportação

As onze bases reais foram preparadas no contorno externo comum da AII de águas/solos e guardadas em SQLite local:

| Base | Resultado observado | Atributos por registro |
|---|---:|---:|
| Trechos hidrográficos | 68 registros | 13 |
| Massas d’água | 16 registros | 58 |
| Solos | 3 registros | 6 |
| UCs estaduais | 3 registros | 13 |
| UCs federais | 1 registro | 31 |
| UCs municipais | 1 registro | 13 |
| Áreas urbanizadas | 34 registros | 7 |
| Rodovias | 4 registros | 21 |
| Trilhas | 34 registros | 13 |
| Declividade | 171.428 células válidas; 6 classes | Raster nativo |
| Cobertura da terra | 182.154 células válidas; 10 classes | Raster nativo |

O JSON real retornou HTTP 200, attachment `geovale-horizontes.json`, **3.543.992 bytes** nesta verificação, todas as bases e matrizes. Conferiu-se número de registros, correspondência exata dos campos com o esquema publicado, preservação de nulos, dimensões/quantidade de células e presença de evidências/datas. As geometrias foram comparadas com o contorno com tolerância numérica de 1e-10 grau para diferenças de ponto flutuante, sem alterar as geometrias exportadas. Não se interpreta essa tolerância como precisão do recorte.

Os dois GeoTIFFs reais também retornaram HTTP 200, hashes iguais aos metadados, células válidas iguais às contagens e grade nativa conservada. Uma segunda instância do armazenamento recuperou as onze bases sem consulta externa; reinício do servidor conservou as datas de consulta. `.local/territorios.sqlite3` permanece ignorado pelo Git. Valores acima são observações documentadas desta coleta, sem constantes de demonstração no aplicativo.

## Interface e fluxo conferidos

- Sem seleção: botão Influência visível e desabilitado. Selecionar pelo nome/cartão ou pela bolinha mostra automaticamente um contorno da mina, sem ativar Influência. Desmarcar remove-o e retorna a MG; desligar Influência preserva o contorno da mina selecionada.
- Ativar Influência: contorno, mina sombreada, cinco grupos WMS e 34 geometrias visuais de trilhas; esquerda com somente Influência e Exportar JSON ao terminar carregamento.
- Cinco máscaras de polígono ativas no navegador, com quatro imagens carregadas por grupo no enquadramento observado. Os estilos oficiais se mantêm e as imagens ficam limitadas ao contorno irregular.
- Marcar Água remove sua versão mascarada e usa uma única versão ampliada: quatro máscaras permanecem para os outros grupos. Desmarcar restaura cinco máscaras e uma única versão de Água.
- Zoom atualiza coordenadas das máscaras; elas reaparecem visíveis ao terminar animação. Ocultar/reabrir a barra conserva a influência e as cinco máscaras.
- Clique em Exportar JSON acionou a rota de download sem erro na interface; conteúdo integral foi conferido por HTTP.
- Legenda e escala mantiveram espaçamento acima dos créditos completos, inclusive com Satélite e todos os temas. Em janela 1200 × 850, foram medidos cerca de 45 pixels da legenda até os créditos e 12 pixels da escala até os créditos. Desligar Influência removeu os créditos dos temas retirados e manteve os créditos do contorno da mina.
- Desktop 1440 × 900, janela 1200 × 850 e celular 390 × 844 inspecionados. No celular, largura de conteúdo igual a 390 pixels, sem rolagem horizontal; controles antes do mapa e consulta depois.

A representação WMS é mascarada no navegador; os valores do relatório vêm de WFS/WCS/ArcGIS persistidos, não de leitura das cores. Imagens atuais e dados guardados podem ter datas distintas. Créditos cartográficos permanecem na tela; fontes/datas/explicações detalhadas ficam no relatório e documentação.

## Alcance

A validação verifica integração e contratos computacionais. Não certifica atualidade do terreno, precisão de levantamento, adequação técnica das cinco escolhas ou limites de fechamento. Não foi feita validação por especialista da Vale. O contorno comum é aproximado, do estudo conjunto Tamanduá/Horizontes, e não define intervenção ou recuperação para todos os temas. Testes de falhas usam respostas controladas; não se provocou indisponibilidade física dos fornecedores. [Método](DADOS_TERRITORIAIS.md), [evidência](INFLUENCIA.md).
