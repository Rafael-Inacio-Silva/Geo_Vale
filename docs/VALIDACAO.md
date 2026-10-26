# Validação da etapa territorial

Revisão de 26/10/2026, versão **3.4.0**, em macOS, Python 3.12 e Node 24. Servidor em `127.0.0.1:8000`, sem implantação pública.

## Verificações automatizadas executadas

- **79 testes Python aprovados**: mapa, desenho manual, trilhas, atributos ANM, município e referências locais. Os testes específicos do antigo importador geométrico ANM foram retirados; permanecem os de identidade, atributos, cache, falha e recuperação cadastral.
- **2 testes Node aprovados**, cobrindo pesquisa do catálogo único e ausência de resultados inventados.
- **TypeScript e build Vite aprovados**.
- O pacote local foi reproduzido pelo script de preparo. A referência entregue conserva exatamente as coordenadas do snapshot OpenStreetMap. Todos os cinco recortes têm geometria válida; a referência é Polygon editável com 65 vértices.

Os testes de referência verificam fonte/CRS/hash, os cinco identificadores, página/figura dos quatro recortes de influência, identidade OSM, igualdade com snapshot, marcador dentro da referência, conversão para origem manual ao validar edição e 404/503/recuperação de pacote inválido. A rota não consulta fontes externas.

## Fontes reais conferidas

- PDF público do parecer: HTTP 200, `application/pdf`, SHA-256 igual ao arquivo fornecido pelo usuário. Figura 2.3/p. PDF 18 conferida visualmente com o traçado digitalizado.
- OpenStreetMap: API oficial `/api/0.6/way/315221699/full.json` retornou Mina Capitão do Mato, `landuse=quarry`, 66 posições incluindo fechamento, way versão 5, timestamp 31/01/2019. Snapshot salvo sem simplificar/reparar sua geometria. A data do way não foi apresentada como data do terreno ou imagem.
- API local de referências: HTTP 200, uma referência OSM e quatro recortes do parecer, sem chamada externa na entrega.
- ANM: consulta real retornou processo 003.964/1950, VALE S.A., CONCESSÃO DE LAVRA, FERRO e 471,39 ha. Resposta local contém apenas propriedades e fonte, sem geometria. Teste confere `returnGeometry=false` e `f=json`.
- IBGE e limite estadual: retornos HTTP 200 observados no navegador/servidor. Houve uma falha inicial 503 do limite estadual; os controles locais e o restante do mapa permaneceram utilizáveis e a consulta seguinte recuperou o contorno. Não houve interrupção física de rede nem simulação visual de todos os timeouts.

## Jornada conferida no navegador

- Abertura com botões documentais desabilitados; selecionar Horizontes habilitou os dois controles locais e acrescentou Nova Lima.
- Modo Referência mostrou a área cinza com símbolos de mineração, contorno vetorial OSM e atribuição. Usar como área acrescentou uma entrada independente; visitar Referência novamente ofereceu Selecionar esta área e manteve apenas uma referência.
- Desenho manual de segunda área com três vértices, fechamento, ajuste e confirmação pela API manteve a referência anterior.
- Ajustar a referência apresentou os pontos editáveis; Cancelar restaurou a confirmação sem perder a segunda área. Outro ajuste confirmado resultou em recorte manual com 66 pontos e retirou a atribuição de referência daquela área.
- Renomear por Enter atualizou a identificação e a lista para “Referência ajustada”, mantendo a outra área.
- Área de influência mostrou cinco feições: quatro filtros e referência OSM sombreada. Desmarcar os quatro filtros deixou uma feição de contexto (a mina sombreada), preservando duas áreas de estudo. Os créditos acompanharam as fontes visíveis.
- Ocultar/reabrir a barra preservou filtros e áreas. Desmarcar a mina retornou a MG, retirou influência e município e manteve as duas áreas confirmadas.
- Layout desktop 1440 × 900 e celular 390 × 844 conferidos; largura de conteúdo igual à largura do viewport, sem rolagem horizontal. Os controles continuam fora do mapa. Redimensionar conservou as áreas.

## Alcance

Não houve nova conferência visual individual das dez bases WMS e todas as legendas nesta mudança; os testes de seus contratos e trilhas continuam aprovados. Não foram adicionados cálculos de comparação, área, distância, interseção, ranking, diagnóstico ou persistência.

A referência OSM não é perímetro certificado ou levantamento atual. As influências são digitalizações aproximadas do meio físico de Tamanduá/Horizontes, sem acurácia cadastral e sem representar fechamento. A validade geométrica não certifica a precisão territorial. ANM informa cadastro; IBGE, contexto administrativo; trilhas, cadastro municipal. Ausência de feição não comprova ausência de risco.

## Alternância de modos conferida

Referência → Influência → Referência conservou zero áreas até a ação explícita Usar como área. Repetir a consulta e selecionar a referência manteve uma única entrada. Um desenho aberto de três pontos foi pausado pelos modos Referência/Influência e retomado em Manual: contagem e estilos/posições dos três marcadores no DOM foram exatamente iguais, com retorno ao enquadramento anterior. O ajuste fechado também foi suspenso e retomado com seus seis marcadores; confirmou como segunda área manual de três pontos. O contexto de influência permaneceu como apoio sob o desenho.

Na versão final, a alternância rápida Referência → Influência → Referência terminou imediatamente na referência, com uma feição de contexto e zero áreas criadas, escala de 500 m no desktop testado. Depois de usar a referência e consultar influência, desmarcar a mina retornou a escala estadual (200 km), modo Manual, zero feições de contexto e uma área conservada. No celular 390 px, os três seletores ocuparam cerca de 109 px cada, sem rolagem horizontal. Desmarcar AII, visitar Referência e voltar a Influência manteve os estados `[false, true, true, true]`; o filtro foi restaurado ao terminar. O tamanho normal do navegador foi restaurado.
