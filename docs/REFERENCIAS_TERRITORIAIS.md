# Área de referência e áreas de influência

Versão 3.4.0, preparada em 26/10/2026. Os modos são **Manual**, **Referência** e **Influência**. Os dois últimos exigem mina selecionada e pacote local disponível. As duas fontes têm significados separados.

## Área de referência: marca de mineração do OpenStreetMap

Por decisão do usuário, o botão utiliza o contorno da **área cinza com símbolos de mineração**, visto no fundo Mapa. É a feição [Mina Capitão do Mato — way 315221699](https://www.openstreetmap.org/way/315221699), com `landuse=quarry`, `resource=iron_ore` e fonte publicada `Bing`. O nome anterior identifica a mesma unidade exibida como Horizontes no catálogo.

A geometria veio da [API oficial OpenStreetMap](https://api.openstreetmap.org/api/0.6/way/315221699/full.json): **66 posições, incluindo fechamento, 65 vértices**. É um Polygon simples válido, guardado sem simplificação, reparo, deslocamento ou digitalização da imagem. `dados/referencias/mineracao-osm.geojson` conserva o snapshot vetorial, ID, versão, timestamp, tags, URL, data de consulta, licença e hash da resposta. Não armazena perfil/identidade dos colaboradores.

Consulta em 26/10/2026: way versão 5, timestamp **31/01/2019, 13:56:08 UTC**. Esse timestamp é da edição do objeto way, não data da imagem Bing nem de levantamento de campo; os nós podem ter revisões próprias. A consulta atual não comprova atualização do terreno. A referência corresponde ao cadastro colaborativo mostrado pelos símbolos, **não certifica perímetro físico atual, propriedade, licença, atividade operacional ou área pós-mineração**. O símbolo do mapa não substitui diagnóstico.

Atribuição: **© OpenStreetMap contributors**, [ODbL 1.0](https://www.openstreetmap.org/copyright). O crédito acompanha a referência confirmada ou sombreada, inclusive sobre o fundo Satélite. A referência é local e pode ser carregada sem consultar OSM naquele momento. O catálogo usa seu centro visual aproximado como marcador de navegação.

## Área de influência: mapa do parecer FEAM

Fonte: [Parecer nº 64/FEAM/GST/2024](https://sistemas.meioambiente.mg.gov.br/consulta-intervencao/uploads/122024/24642_gvwxhTH__066nrKD6s2u.pdf), de 13/12/2024, processo SLA 4159/2020, SEI 1370.01.0024378/2020-18. O parecer analisa o **Projeto de Ampliação das Cavas Tamanduá e Horizontes**. Usa-se a **Figura 2.3, PDF p. 18 / impressa 15**, mapa de 02/11/2023. A legenda distingue:

| Filtro | Interpretação da legenda original |
|---|---|
| Área do projeto · ADA unificada | Área Diretamente Afetada unificada do projeto conjunto; não é a mina isolada. |
| Água subterrânea · AID | Área de Influência Direta da Hidrogeologia. |
| Águas e solos · AID | Influência direta para qualidade das águas, dinâmica hídrica e erosiva e alteração dos solos. |
| Águas e solos · AII | Influência indireta para esses mesmos atributos. |

Os nomes curtos agrupam os atributos expressos na legenda. A influência é do meio físico e do projeto conjunto, **não de fechamento, recuperação ou pós-mineração**. Não foi obtido o conteúdo do plano de fechamento para esta entrega. A menção à apresentação do plano no parecer não permite reconstruí-lo. Os recortes não devem ser aplicados automaticamente a vegetação, biodiversidade, população ou definição de beneficiários.

Na primeira seleção da mina, os quatro filtros de influência iniciam marcados e a **referência OSM da mina fica sombreada**, mesmo com todos os filtros desmarcados. O sombreamento não é uma quinta delimitação do parecer. As fontes/datas são diferentes e não se força coincidência entre seus perímetros. Alternar modos não cria áreas de estudo nem altera desenhos. Usar como área adiciona a referência OSM explicitamente; se já existir intacta, seleciona a mesma área. Fonte e significado explica as siglas e abre o PDF.

## Preparo das influências e precisão

O mapa do PDF é **raster**, sem vetor georreferenciado extraível. Os quatro recortes são uma **digitalização aproximada para o MVP**, não arquivos oficiais da Vale/FEAM. Não há levantamento de campo, precisão cadastral ou validação de especialista.

- `dados/referencias/horizontes.geojson`: pacote de cinco Features, com referência OSM e quatro influências. Cada fonte fica identificada; o bloco `fonte` do pacote descreve o parecer das influências.
- `dados/referencias/digitalizacao.json`: pontos em pixels da Figura 2.3 e controles da grade.
- `ferramentas/preparar_referencias.py`: junta o snapshot OSM intacto aos recortes preparados, usando biblioteca padrão e Shapely já instalados.

Imagem nativa da Figura 2.3: 1377 × 1286 pixels; leste 610000/620000 nos pixels x=442/951; norte 7780000/7770000 nos pixels y=327/836. A grade é SIRGAS 2000 / UTM 23S (EPSG:31983). O preparo transforma pixels por eixo para UTM e aplica inversa Transversa de Mercator em GRS80 para longitude/latitude, serializada como EPSG:4326. Não há ajuste geodésico de alta precisão. A amostragem é cerca de 19,6 m por pixel: **não é acurácia do polígono**. Bordas grossas, leitura da grade e generalização acrescentam erro; não existe tolerância cadastral certificada.

Os contornos foram traçados visualmente e generalizados. A digitalização da ADA contém cruzamentos em conexões estreitas: `make_valid` organiza esses componentes em MultiPolygon durante o preparo, preservados no pacote. Esse acerto é explícito e exclusivo da digitalização aproximada; **desenhos do usuário continuam rejeitados, nunca reparados silenciosamente**. A representação pode omitir detalhes/vazios menores da imagem. Nenhuma correção é aplicada ao snapshot OSM.

Para reproduzir, na raiz: `.venv-geovale/bin/python ferramentas/preparar_referencias.py`. O pacote guarda o SHA-256 do PDF e o snapshot guarda o hash da resposta OSM. Receita e fontes precisam ser revisadas juntas se houver atualização. Não existe download/redigitalização automática em execução.

## Entrega e limite do escopo

`GET /api/minas/horizontes/referencias` lê o pacote local e confere identidades, procedência, geometria e extensão. Mina desconhecida retorna 404; pacote ausente/incompatível retorna 503. Não consulta serviços externos. ANM solicita somente atributos cadastrais com `returnGeometry=false`; não fornece área de estudo.

Os contornos locais funcionam independentemente de ANM, WMS ou IBGE. Fundo e outras fontes continuam dependendo de internet. Os filtros são visuais e não capturam cliques de desenho. Ocultar a barra conserva estados; desmarcar a mina retira a influência e desabilita os modos documentais, preservando as áreas confirmadas. Usar a referência preserva `origem=referencia_osm`; ajustá-la e confirmar produz recorte manual, sem alterar o snapshot.

O engenheiro pode sobrepor uma ou várias áreas pessoais ao contexto. **Não há cálculo de área, interseção, comparação automática, beneficiários, aptidão ou recomendação de uso futuro.** Esta etapa não define um buffer genérico ou a cidade toda como limite de recuperação.
