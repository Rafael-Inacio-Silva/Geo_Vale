# Validação da entrega

Revisão de **26/10/2026**, versão **3.3.0**, em macOS, Python 3.12 e Node 24. Execução local em `127.0.0.1:8000`; código e documentos destinados ao GitHub por solicitação do usuário, sem implantação pública.

## Verificações automatizadas

- **81 testes Python aprovados**: 13 de mapa, 15 de validação de área, 24 de trilhas, 19 de ANM e 10 de limite municipal.
- **Dois testes de pesquisa aprovados**: nome atual/anterior, normalização e ausência de correspondência, com uma única mina no catálogo.
- **TypeScript e build Vite aprovados**, incluindo as barras recolhíveis, coleção de áreas, consulta cadastral e limite IBGE. Sem novas dependências nesta adição.

Os testes da ANM conferem identidade do processo, atributos, origem, geometria preservada, descarte de rótulos oficiais na validação manual, cache concorrente/expiração/cópia defensiva, truncamento e respostas incompatíveis, falha e recuperação sem expor detalhes internos. Os municipais conferem código fixado no catálogo, ausência de consulta inicial/para mina desconhecida, geometria/CRS/extensão, cache, falha e recuperação independente. Consulta de códigos/processos arbitrários não é oferecida ao cliente.

O desenho é validado individualmente: buracos, anel aberto, interseções, degeneração, coordenadas inválidas/excessivas, limite de 500 vértices e corpo HTTP de 128 KiB. A coleção contém várias Features Polygon; o contrato não foi ampliado para MultiPolygon. Os testes de trilhas verificam cobertura, respostas truncadas, renderer oficial, cor/rótulo, legenda do recorte e cache compartilhado.

O TestClient emite um aviso de depreciação do adaptador HTTPX da Starlette. O servidor não usa esse adaptador em operação. Leaflet.draw pode emitir aviso de uma função legada do Leaflet; os fluxos de desenho/edição foram concluídos.

## Fontes reais e interface

A consulta direta da ANM e a rota local retornaram o processo **003.964/1950**, VALE S.A., CONCESSÃO DE LAVRA, FERRO e 471,39 ha, em GeoJSON solicitado EPSG:4326. A prévia desenhou a poligonal cadastral real. O cartão mostrou os atributos e data de consulta dentro da seção expansível, sem cartão separado abaixo.

A API IBGE retornou uma única Feature Polygon para **Nova Lima, código 3144805**, qualidade máxima da API simplificada, com 355 posições no anel incluindo fechamento. A rota local entregou o contorno e a fonte/data; o frontend o enquadrou com o ponto da mina. Na abertura não havia município. Voltar para MG removeu os caminhos municipais e o crédito IBGE, fechou os detalhes e desabilitou Polígono ANM. A data de consulta não foi apresentada como ano da malha.

As onze bases temáticas continuam no catálogo. A verificação real de dez GetMap/dez legendas WMS e da fonte municipal de trilhas ocorreu em 25/10/2026, sem representar nova validação integral de cada fornecedor em 26/10. As trilhas têm cores e nomes oficiais; os testes de integração com sua fonte simulada passaram nesta revisão.

## Áreas independentes e barras

Verificado em navegador com a aplicação compilada:

- Polígono ANM desabilitado antes de selecionar a mina; seleção habilitou, consulta trouxe prévia e confirmação preservou origem cadastral.
- Adicionar duas demarcações manuais além da área ANM resultou em **três áreas simultâneas**. As três geometrias apareceram no SVG, com a ativa amarela e as demais verdes.
- Ocultar a barra de áreas com dois pontos já marcados, reabrir, adicionar o terceiro e confirmar manteve o mesmo desenho e a área anterior.
- Cancelar a adição de uma quarta área preservou as três confirmações e a seleção anterior. Remover a terceira deixou duas geometrias e selecionou a última restante.
- Selecionar a área ANM, arrastar um vértice e confirmar produziu área manual com 12 pontos, conservando a segunda área e retirando a atribuição de área cadastral. O cartão cadastral permaneceu independente.
- Ocultar/reabrir a consulta preservou a coleção e ampliou o mapa. Recarregar descartou as áreas, conforme o contrato de memória da página.
- Ferramentas à esquerda, mapa central, pesquisa/cartão/camadas à direita. Nenhum painel de áreas sobre o mapa. As setas são botões com rótulo, estado expandido e controle da barra correspondente.
- Faixa superior amarela contínua entre cada barra e sua seta: borda de 4 px e a mesma cor RGB (255, 195, 41) nos quatro elementos.

A coleção foi testada com recortes manuais de verificação, sem certificar que representem cava, barragem ou limite de intervenção real. Não se criou dado de exemplo no catálogo.

## Responsividade e limites

Conferidas larguras **375, 768 e 1280 px** nesta revisão, sem transbordamento horizontal. Em 375×812 e 768×1024, ferramentas antes do mapa e consulta depois, com atalhos de ocultação no topo. O mapa continua com altura utilizável. Em 1280×900, as barras rolam independentemente; recolher expande a área central sem desmontar o desenho. Não houve teste em aparelhos físicos ou execução Linux.

Falhas das fontes ANM/IBGE e sua recuperação têm cobertura automatizada. Não foi interrompida a conexão física nem aguardado manualmente cada timeout externo. Não houve nova simulação visual de todos os erros nesta versão. As fontes continuam externas e sujeitas à disponibilidade e condições de uso.

Não há persistência das áreas, análise espacial, medição, ranking ou recomendação de uso futuro. Fase cadastral não comprova operação; processo ANM não é perímetro físico; malha municipal simplificada não é certificação cadastral; trilha não comprova acesso ou segurança. Fontes regionais não descrevem necessariamente a condição atual da cava.

## Opções recolhíveis de camada

Conferência de 26/10/2026: ativar relevo e água manteve intensidade/legenda recolhidas; cada seta expandiu somente seu tema. A intensidade de relevo foi alterada por teclado de 50% para 55%; recolher e reabrir preservou 55% e as duas camadas ativas. A legenda oficial de declividade abriu pela seção interna; recolher água não afetou relevo. Botões têm `aria-expanded` e `aria-controls`. Mensagens de carregamento/falha ficam fora do trecho oculto. TypeScript e build aprovados; nenhuma alteração no backend ou nos contratos das fontes.
