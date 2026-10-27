# Validação do território e relatório PDF

Revisão de 27/10/2026, versão **4.1.0**, macOS, Python 3.12 e Node 24. Fluxo local em `127.0.0.1:8024`, sem implantação pública.

## Verificações automatizadas

**85 testes Python aprovados**, **2 testes Node aprovados**, TypeScript/build Vite aprovados e `pip check` sem dependências quebradas. Instalação do lock macOS com hashes executada. Lock Linux foi atualizado; execução Linux não foi conferida.

Os testes territoriais verificam catálogo completo, recorte irregular, atributos/nulos/IDs, CRS, completude, geometrias inválidas, classes oficiais, grade/células/NoData, persistência, base nova, invalidação por recorte, isolamento por mina, repetição após falha e início automático sem clique. Os testes do PDF verificam conteúdo das onze bases, marca/autoria GeoVale, rótulo fictício, referências, marcadores, cenário inválido/alterado, invalidação de cache, inline/attachment, ausência de consulta externa e preservação dos atributos e matrizes internas. Dados pendentes/vencidos ou de outro recorte impedem relatório apresentado como completo.

Há avisos de depreciação Starlette/TestClient/HTTPX e Rasterio/Affine/NumPy, sem falhas. Nenhuma dependência foi alterada apenas para silenciar esses avisos.

## Dados reais conferidos

O documento utiliza as onze bases reais persistidas no recorte comum:

| Base | Quantidade observada |
|---|---:|
| Trechos hidrográficos | 68 registros |
| Massas d’água | 16 registros |
| Solos | 3 registros |
| UCs estaduais | 3 registros |
| UCs federais | 1 registro |
| UCs municipais | 1 registro |
| Áreas urbanizadas | 34 registros |
| Rodovias | 4 registros |
| Trilhas | 34 registros |
| Declividade | 171.428 células válidas; 6 classes |
| Cobertura da terra | 182.154 células válidas; 10 classes |

Os 164 registros vetoriais têm identificador curto conferido no texto do inventário. Foram conferidos os nomes das onze bases e a manutenção dos campos originais e GeoTIFFs no armazenamento. As contagens reais não são constantes de demonstração no aplicativo. A assinatura de coleta continua 4.0.0, sem invalidar os dados por uma mudança apenas de apresentação.

## PDF real e diagramação

A rota final retornou **HTTP 200, application/pdf**, inline na consulta e attachment com baixar=true. O documento conferido tem **18 páginas**, **nove marcadores de seção** e **187.905 bytes** nesta emissão. Metadados de autoria: GeoVale. Cenário técnico fictício separado de observações geográficas; sem marca corporativa, assinatura de especialista, laudo ou conclusão real de segurança.

Todas as páginas foram renderizadas para inspeção visual. Conferidos capa/logo, mapas vetoriais, tabelas/classes, conservação, cenário, fontes e inventário. Fontes Unicode incorporadas, cabeçalhos repetidos nas tabelas e número de página. As matrizes não são despejadas em texto; aparecem como classes/contagens. Identificadores e nomes dos vetores estão no anexo, com ausência de nome preservada.

O download realizado por **Baixar PDF** no navegador foi comparado byte a byte com o PDF da API e coincidiu. A cópia conferida é gerada do estado atual e não substitui a geração dinâmica por um arquivo fixo no repositório. SQLite e arquivos gerados não são publicados em lote no Git.

## Fluxo no navegador

- Antes da seleção: Influência desabilitada e Ver relatório ausente. Selecionar a mina mostra o contorno e Ver relatório, sem exigir Influência.
- Ver relatório abre diálogo; PDF.js/worker no build oficial legacy carregam sob demanda. Capa e página de contagens reais renderizadas, com texto também disponível para leitor de tela.
- Anterior/Próxima atualizam a página; download salva o documento visualizado. Fechar preserva seleção e retorna o foco ao botão.
- Falha de conexão provocada desligando somente o servidor de verificação apresentou Tentar novamente. Reinício e nova tentativa recuperaram o relatório de 18 páginas sem perder a seleção.
- Em celular 390 x 844, largura do documento HTML igual a 390, diálogo com 374 pixels e canvas com 340 pixels; sem rolagem horizontal. Os controles permaneceram disponíveis.

A compatibilidade foi verificada em sessão controlada do navegador com `Map.prototype.getOrInsertComputed`, `Uint8Array.prototype.toBase64` e `Uint8Array.fromBase64` removidos antes de carregar o leitor. O build moderno reproduziu TypeError ao renderizar; o legacy renderizou as 18 páginas do PDF real. Na interface compilada sob as mesmas ausências, uma falha transitória de canvas foi provocada: Tentar novamente recuperou a capa sem fechar o diálogo e Próxima exibiu a tabela das onze bases. Essa verificação simula APIs ausentes; não equivale a execução automatizada no Safari do usuário, cujo controle nativo não respondeu. Os arquivos temporários de reprodução foram removidos do build após a conferência.

A representação temática do mapa continua independente do documento. Os controles visuais não escolhem dados do relatório; o armazenamento real é separado do cenário local fictício. As verificações do novo fluxo não certificam condições ambientais, estabilidade ou precisão do contorno.

## Alcance

O documento é caracterização territorial com cenário técnico simulado. Não é plano de fechamento da Horizontes, laudo, avaliação de aptidão ou ranking. Não houve validação por especialista da mina. O recorte comum permanece uma aproximação do estudo conjunto Tamanduá/Horizontes e os dados conservam suas idades/escalas próprias. [Relatório e cenário](RELATORIO.md), [dados](DADOS_TERRITORIAIS.md), [recorte](INFLUENCIA.md).
