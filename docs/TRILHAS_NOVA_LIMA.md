# Trilhas de Nova Lima — integração municipal

Opção de sobreposição municipal, disponível desde a versão 4.2.0. Os seis temas estaduais/dezessete bases da IDE-Sisema continuam disponíveis. Esta camada acrescenta uma **segunda infraestrutura pública**, com informação municipal específica para conhecer o entorno da Mina Horizontes.

## Fonte verificada em 25/10/2026

- [Aplicativo Público Territorial Municipal — Prefeitura de Nova Lima](https://pmnl.maps.arcgis.com/apps/webappviewer/index.html?id=ff761e397b904ad4b164eb8a71cb7d86).
- Aplicativo `ff761e397b904ad4b164eb8a71cb7d86`, proprietário `geoprocessamentoPNL`, acesso público; WebMap `f356b24170e9456f9546a514676aef5c`.
- Título no aplicativo: **Trilhas (Decreto 6773/2016)**.
- [Item público da camada](https://pmnl.maps.arcgis.com/home/item.html?id=2504a27b4e684bfdbe0210fa7af1971d).
- [ArcGIS REST — Trilhas/FeatureServer/0](https://services3.arcgis.com/8p5P2iPRkT0RXnI3/arcgis/rest/services/Trilhas/FeatureServer/0).
- Nome técnico `Trilhas_Decreto_6773_2016_fev_2024`, capacidade `Query`, respostas JSON, GeoJSON e PBF; até 2.000 registros por consulta.
- Referência nativa **EPSG:31983**, SIRGAS 2000 / UTM 23S; `outSR=4326` entrega longitude/latitude para o GeoJSON.
- Contagem observada: **67 registros**. Última edição informada pelo serviço: **22/04/2024 às 16:34:49 UTC**. Não equivale à data de levantamento de cada caminho.
- Extensão publicada aproximada: oeste −44,005238; sul −20,211133; leste −43,749501; norte −19,923718. Cobertura municipal em Nova Lima; não cobre MG inteiro ou o mundo.

A API pública respondeu sem login ou chave. Isso comprova viabilidade técnica de consulta, não uso ilimitado. O item não apresentou informação explícita de licença; não se presume autorização irrestrita de redistribuição. O GeoVale identifica e credita a fonte, sem copiar sua aplicação. O processamento territorial guarda apenas os registros/porções que intersectam a influência, com os atributos publicados.

## Consulta implementada

Ao marcar Trilhas de Nova Lima, o navegador pede `/api/mapa/trilhas?bbox=oeste,sul,leste,norte`. O backend recorta à extensão da fonte e consulta o endpoint `/query` com:

```text
f=geojson
where=1=1
geometry=oeste,sul,leste,norte
geometryType=esriGeometryEnvelope
inSR=4326
outSR=4326
spatialRel=esriSpatialRelIntersects
outFields=OBJECTID,Name
returnGeometry=true
resultRecordCount=2000
orderByFields=OBJECTID
```

Nome, identificador, geometria e símbolo sanitizado (cor, opacidade e largura) são encaminhados à interface, junto com a legenda filtrada. O servidor confere tipo, validade, extensão e truncamento; erro não vira lista vazia. Há timeout, limite de tamanho e cache temporário em memória (dez minutos, até 16 enquadramentos). Navegar renova a bbox; fora da cobertura não consulta a fonte. A consulta visual tem cache em memória. Separadamente, o processamento territorial guarda o recorte da influência em SQLite e o atualiza automaticamente.

Os traçados e a legenda usam as cores e os nomes publicados na configuração do item oficial. Não se aplica o amarelo simples do FeatureServer a todas as trilhas. A largura base de 1,5 ponto publicada é convertida para 2 pixels CSS, sem halo extra. As variações de espessura por escala do aplicativo municipal não são reproduzidas; cores e rótulos são preservados. A linha não mostra o nome ao passar o cursor: era a única camada temática com rótulo no mouse (as demais são imagens WMS), e os nomes sobre a mina poluíam o mapa; o único rótulo do mapa é o da mina. O nome continua na legenda e nos dados do relatório. Intensidade, legenda, remoção, falha e recarga seguem os controles já existentes. A camada visual pode ser combinada com os cinco temas estaduais; seu estado não altera os dados preparados da influência.

## Justificativa e limite

Caminhos cadastrados são contexto para observar conexões e levantar questões sobre acesso, circulação e uso recreativo no entorno. O objetivo desta adição é demonstrar integração de **fontes diferentes**, motivada pelo cadastro concreto encontrado no portal municipal. As referências acadêmicas dos temas estaduais não foram apresentadas como validação desta escolha.

No inventário WMS da IDE-Sisema consultado em 24/10/2026, não foram encontrados títulos contendo “trilh”. As bases estaduais integradas não incluem esse cadastro; isso não garante ausência em todo serviço estadual. A fonte municipal foi verificada diretamente.

Traçado cadastrado **não comprova acesso público, segurança, conservação, autorização de entrada ou aptidão para turismo**, nem corresponde ao limite da mina. O rótulo do decreto é o informado pela fonte, sem análise jurídica do ato. A falta de feição na região visível não comprova inexistência de caminhos. A etapa oferece exploração visual e caracterização cadastral, sem avaliação de uso futuro.

## Configuração oficial de cores e nomes

A [API de configuração do item](https://pmnl.maps.arcgis.com/sharing/rest/content/items/2504a27b4e684bfdbe0210fa7af1971d/data?f=json) publica o renderer em `layers[0].layerDefinition.drawingInfo.renderer`. Seu tipo é `uniqueValue`, com `field1=Name`. Em 25/10/2026, foram encontradas **59 categorias**, **12 cores distintas** e 67 registros geométricos. Quantidade de categorias não equivale a quantidade de feições; nomes diferentes podem compartilhar uma cor.

Essa configuração é distinta do renderer simples amarelo publicado no endpoint do FeatureServer. O GeoVale consulta geometria e configuração na API, sem extrair cores da captura de tela ou manter tabela manual de nomes/cores. A simbologia validada fica em memória por dez minutos e é compartilhada entre enquadramentos. Geometria e configuração são lidas em paralelo quando necessário, com timeout e limites de tamanho independentes.

A associação usa `Name` sem distinguir caixa, pois a fonte contém, por exemplo, “Trecho Substituído 08-2018” na geometria e “Trecho substituído 08-2018” na categoria. O texto exibido na legenda conserva o rótulo oficial. Se uma categoria não tiver símbolo válido, a integração informa falha em vez de inventar cor.

A legenda inclui apenas as categorias retornadas pela consulta de interseção com o enquadramento, sem duplicatas e na ordem publicada pela Prefeitura. Na versão ampliada por checkbox, feições são devolvidas inteiras pelo serviço e a legenda se refere à consulta. Com Influência ativa e checkbox desmarcado, a rota trilhas-influencia intersecta as linhas no polígono irregular e filtra a legenda pelas categorias presentes, preservando símbolos oficiais. A legenda não é contagem de linhas SVG. Ao navegar, a lista anterior é limpa e atualizada com os novos dados. Intensidade modifica opacidade sem mudar a associação nome/cor. Lista com rolagem e foco permite leitura sem alongar toda a lateral.

## Dados associados à influência

O pipeline territorial consulta o mesmo FeatureServer com contagem prévia, metadados de campos e `outFields=*`, conservando os 13 atributos publicados observados nesta revisão. Recorta as geometrias na influência comum; não usa bbox visível ou o checkbox da camada. Os registros completos ficam guardados por mina, com fonte/data, e entram na atualização automática de todas as bases. Essa consulta é independente do renderer e do cache leve de visualização. [Método](DADOS_TERRITORIAIS.md).
