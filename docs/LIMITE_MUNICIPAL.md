# Contorno municipal sob seleção

Implementado em 26/10/2026, versão 3.3.0. O mapa abre com o contorno de Minas Gerais, sem carregar uma malha de todos os municípios. Selecionar a Mina Horizontes pela lista, seta de detalhes ou marcador acrescenta **somente Nova Lima**. Ver Minas Gerais remove esse limite e a seleção, preservando as áreas de estudo e temas ativos.

## Fonte oficial

[API de malhas geográficas do IBGE, versão 3](https://servicodados.ibge.gov.br/api/docs/malhas?versao=3). O [código de Nova Lima é 3144805](https://www.ibge.gov.br/cidades-e-estados/mg/nova-lima.html), associado à mina no catálogo local.

Consulta: `https://servicodados.ibge.gov.br/api/v3/malhas/municipios/3144805?formato=application%2Fvnd.geo%2Bjson&qualidade=maxima`.

É a maior qualidade da **API de malhas simplificadas**, indicada pelo IBGE para aplicações web. Não é a malha cadastral original. A consulta real retornou uma Feature Polygon, propriedade `codarea=3144805`, 355 posições no anel incluindo fechamento e cerca de 7,9 kB descompactados. A geometria é preservada pelo GeoVale. O resultado é consumido como GeoJSON em longitude/latitude, sem medição ou transformação local. A resposta consultada não declara CRS nem ano da malha; a aplicação registra a data da consulta e `ano_referencia=null`. Não atribuímos o ano da consulta ao levantamento nem presumimos que seja a malha 2025. A API também oferece metadados, mas seus valores se referem à malha original e não são usados para calcular área no MVP.

## Integração

`GET /api/minas/{mina_id}/limite-municipal` lê exclusivamente o código fixado no catálogo. Retorna FeatureCollection com código, fonte, qualidade, URL e data efetiva da consulta. Não aceita códigos ou URLs arbitrários do cliente. 404 para mina desconhecida; 503 para indisponibilidade ou resposta incompatível.

O backend verifica identidade, quantidade de feições, tipo Polygon/MultiPolygon, validade e extensão dentro de MG, com timeout de 15 segundos e limite de 2 MiB tanto no corpo recebido quanto após descompactação gzip. Não inventa ou corrige o limite. Cache com trava e cópia defensiva, válido por uma hora em memória. Uma leitura posterior à expiração renova sob demanda; falha de renovação informa indisponibilidade, sem resposta vencida silenciosa. Sem credenciais, lote estadual, Selenium ou armazenamento em banco.

O frontend cancela a requisição ao desfazer/trocar a seleção, remove a camada e seu crédito e ignora respostas antigas. O limite azul tracejado fica acima das imagens temáticas e abaixo das áreas de estudo, com atribuição IBGE. Na seleção, o mapa enquadra município e referência da mina. Se o usuário já começou a demarcar/carregar área ou navegou enquanto a resposta chegava, o limite é acrescentado sem desfazer esse enquadramento. Falha tem recarga própria e não interrompe ANM, desenho ou outras camadas.

O contorno municipal é contexto administrativo para navegação; não delimita a mina, a área degradada nem a área de estudo. Não é uma sétima camada temática selecionável: sua visibilidade acompanha a seleção da mina.
