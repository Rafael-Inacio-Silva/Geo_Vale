# Consulta sobre visualização 3D Google

Pesquisa solicitada pelo usuário em **26/10/2026**, para apresentação do MVP. **Adiada pelo usuário; não implementada ou contratada.** A aplicação continua usando Leaflet, OpenStreetMap/Esri e as fontes territoriais existentes. Nenhuma chave Google, conta Cloud ou serviço com faturamento foi ativado nesta pesquisa.

## Possibilidade técnica

A [3D Maps in Maps JavaScript API](https://developers.google.com/maps/documentation/javascript/3d/overview) fornece um visualizador 3D próprio, com imagens, câmera inclinada, rotação e elementos personalizados. Pode ser incorporado como uma visualização adicional sob ação do usuário. Não é uma camada WMS que se liga diretamente no Leaflet. Para apresentação, a recomendação é manter o mapa 2D para explorar os temas e editar áreas, carregando um visualizador 3D somente ao clicar em uma ação específica. É uma proposta, não um botão ou fluxo já disponibilizado.

A [documentação de cobertura](https://developers.google.com/maps/documentation/javascript/3d/coverage) distingue terreno 3D mundial e superfícies detalhadas (construções/árvores) em cobertura específica. A imagem mostrada pelo usuário no Earth não comprova mesma data, precisão ou detalhamento da cava na API. A mina ainda precisa ser verificada no serviço escolhido. A visualização não substituiria topografia técnica atual ou análise geotécnica.

## Preço e unidade de consumo

[Lista global oficial de preços](https://developers.google.com/maps/billing-and-pricing/pricing), consultada nesta data, em dólares americanos:

| Opção | Franquia/preço consultado | O que representa |
|---|---|---|
| Google Maps JavaScript 3D — SKU Immersive Maps | 5.000 carregamentos sem custo por mês; primeira faixa excedente US$7 por 1.000 carregamentos | [Evento cobrado: carregamento bem-sucedido de mapa 3D](https://developers.google.com/maps/billing-and-pricing/sku-details). Não é contagem de cada clique do usuário. |
| Google Earth Standard no site próprio | US$0 por usuário/mês | [Plano do aplicativo Earth](https://developers.google.com/maps/documentation/earth/earth-plans?hl=en), distinto da API incorporada. Abrir esse site não é uma integração 3D interna do GeoVale. |

A tabela de preços também oferece Photorealistic 3D Tiles com outra franquia (1.000 eventos mensais sem custo) e outro modelo de integração, usando um renderizador compatível. Não se deve misturar essa franquia com os 5.000 carregamentos do visualizador JavaScript nem com os 100.000 tiles de mapas 2D. A opção sugerida nesta pesquisa é o visualizador JavaScript para uma tela de apresentação simples, sem implementar outro motor completo.

A franquia é mensal, não um saldo permanente que precisa durar até a apresentação. O consumo de projetos associados à mesma conta de faturamento é agregado para o SKU correspondente. Os valores podem mudar; conferir novamente no momento da ativação. Esta pesquisa não consultou saldo ou uso de uma conta pessoal.

## Configuração e controle de consumo

[Uso e faturamento da API JavaScript](https://developers.google.com/maps/documentation/javascript/usage-and-billing) exigem conta de faturamento ativa e chave válida, mesmo que o uso permaneça na franquia. Isso não foi configurado. Evitar consumir inclui carregar o código/mapa 3D somente quando solicitado e conservar a instância durante a visualização, em vez de recriá-la a cada movimento. Recarregar ou recriar o mapa pode gerar novo carregamento; não se deve equiparar cada zoom a uma nova abertura.

O Google permite monitoramento e limites de quota. [Alertas de orçamento não interrompem o consumo](https://developers.google.com/maps/faq): é necessário conferir as quotas realmente disponíveis para o serviço/projeto e configurar limites apropriados. Nenhuma quota ou orçamento foi alterado nesta etapa.

Os testes atuais do GeoVale não fazem chamadas à API Google; usam as fontes documentadas do mapa 2D. Testar o Earth no site próprio e usar a API do GeoVale seriam consumos de produtos distintos. Uma integração futura exige validar cobertura, chave, restrições de origem/API, faturamento e limites com a conta autorizada pelo usuário.
