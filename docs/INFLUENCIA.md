# Área de influência — recorte comum do MVP

O GeoVale utiliza **um único recorte de caracterização por mina** para todos os temas. Na Horizontes, é o contorno externo da **AII de águas e solos** do [Parecer nº 64/FEAM/GST/2024](https://sistemas.meioambiente.mg.gov.br/consulta-intervencao/uploads/122024/24642_gvwxhTH__066nrKD6s2u.pdf), de 13/12/2024: Figura 2.3, PDF p. 18 / impressa 15, mapa de 02/11/2023. O estudo trata da ampliação conjunta das cavas Tamanduá e Horizontes.

A legenda da AII trata de qualidade das águas, dinâmica hídrica/erosiva e alteração dos solos. **Usar esse contorno como recorte comum de todos os temas é uma simplificação explícita do MVP**, para oferecer um território consistente e comparar informações na mesma extensão. Isso não converte a AII em influência oficial de vegetação/população, área degradada inteira ou limite de recuperação/fechamento. Não foi obtido plano de fechamento específico de Horizontes.

## Minas sem estudo público

A Mina Abóboras não tem estudo público com mapa de área de influência e fica dentro da AII da Horizontes. Seu recorte é uma **faixa declarada de 3 km** em volta do contorno OSM da cava (`origem: faixa_declarada`), gerada por `ferramentas/preparar_faixa.py` e medida em UTM 23S. A API exige distância e norma de referência no pacote. Porquês em [Catálogo de minas](MINAS.md).

## Mina sombreada

O sombreado conserva o snapshot vetorial da [Mina Capitão do Mato, OpenStreetMap way 315221699](https://www.openstreetmap.org/way/315221699), obtido pela [API OSM](https://api.openstreetmap.org/api/0.6/way/315221699/full.json). `landuse=quarry`, `resource=iron_ore`, fonte publicada Bing. São 66 posições incluindo fechamento, preservadas sem simplificar ou reparar. O nome atual Horizontes consta do catálogo baseado na comunicação oficial da Vale.

Way versão 5, timestamp de 31/01/2019; esse timestamp não é data do terreno/imagem e os nós podem ter suas próprias revisões. O sombreado é contexto colaborativo, sem certificação de perímetro atual, titularidade ou condição operacional. Créditos © OpenStreetMap contributors, [ODbL](https://www.openstreetmap.org/copyright), também sobre Satélite.

## Preparo e precisão

O contorno externo foi digitalizado visualmente de uma imagem raster, sem vetor oficial extraível. Não é levantamento de campo nem limite cadastral. Imagem nativa: 1377 × 1286 pixels. Grade SIRGAS 2000 / UTM 23S (EPSG:31983): eixos leste 610000/620000 nos pixels x=442/951; norte 7780000/7770000 nos pixels y=327/836. O preparo interpola a grade e aplica inversa UTM/GRS80 para longitude/latitude. Amostragem de aproximadamente 19,6 m por pixel **não significa acurácia do contorno**; leitura da grade, espessura da linha e generalização acrescentam incerteza.

- `dados/influencias/horizontes.geojson`: duas Features, `influencia` e `mina`, com evidências e origens separadas.
- `dados/influencias/digitalizacao.json`: somente o traço externo escolhido e seus controles.
- `dados/influencias/mineracao-osm.geojson`: snapshot vetorial e procedência OSM.
- `ferramentas/preparar_influencia.py`: reprodução, sem download externo. Execute com o Python do projeto.

O pacote registra URL, hash SHA-256 do PDF, figura/página, datas e método. Nenhum reparo topológico é aplicado no preparo atual. A API `GET /api/minas/{id}/influencia` confere identidade, procedência, tipos e validade das duas geometrias. Pacote ausente/incompatível retorna 503; mina desconhecida, 404. Falha cadastral ANM não impede o contorno local.

A seleção pelo cartão ou pela bolinha mostra automaticamente o contorno da mina OSM. O botão Influência acrescenta o vetor externo usado pelo processamento, com todas as camadas dentro dele. Os checkboxes ampliam cada tema além desse contorno. Desativar o botão retira o contorno maior/camadas recortadas e preserva a mina sombreada. Desmarcar a mina retira ambos; os dados permanecem guardados por mina e disponíveis no relatório PDF quando completos. [Caracterização](DADOS_TERRITORIAIS.md).
