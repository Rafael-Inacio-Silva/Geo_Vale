# Estado atual

Versão **4.5.0**, atualizada em 28/10/2026. Mapa mundial aberto em Minas Gerais, contorno estadual oficial, uma Mina Horizontes e Nova Lima sob seleção. Fundos OpenStreetMap/Esri, seis temas estaduais e trilhas municipais, com intensidade e legendas. ANM fornece atributos cadastrais; IBGE fornece o município.

A barra esquerda apresenta **Influência**, **Ver relatório** e **Sugerir uso**. Selecionar pelo cartão ou pela bolinha já mostra o contorno da mina. Influência acrescenta o contorno externo e as dezoito bases visualmente recortadas; os checkboxes da direita ampliam cada tema além dele. O PDF GeoVale reúne visão geral, sete fichas temáticas, dados técnicos simulados com mapa de pontos e a sugestão multicritério. O visualizador próprio permite navegar e baixar o PDF.

A preparação usa WFS para quinze bases vetoriais estaduais, WCS para dois rasters e ArcGIS REST para trilhas. Todos os atributos dos registros que intersectam a influência são conservados. A ZAS é lida um registro por vez, porque a resposta conjunta excede 32 MiB, e 13 das 19 geometrias publicadas são corrigidas com make_valid declarado e contado. SQLite guarda os resultados por mina/base em `.local`, fora do Git.

O relatório separa **área minerada** (classe Mineração do MapBiomas: 3.173,3 ha, 20,7% da AII) e **entorno**. Áreas matriciais somam células medidas em UTM 23S. UCs aparecem por grupo do SNUC. Barragens: 10 no recorte, 2 alteadas a montante; ZAS: 729 ha no recorte, 57,8 ha na área minerada.

**Sugerir uso** divide a área minerada em cinco setores contínuos (≥ 20 ha), exclui usos por proteção integral, APP, ZAS e superfície d’água, e ordena conservação, ecoturismo, silvicultura e solar por sete critérios com pesos AHP (consistência 0,012) ou do engenheiro. Com os pesos AHP: S1 e S3 ficam com ecoturismo, S2, S4 e S5 com conservação; S2 é sensível a ±20% nos pesos. O mapa entra num modo próprio: as camadas saem, os setores aparecem pelo 1º uso e a barra direita mostra setores, ranking, porquê e pesos; Voltar ao território devolve as camadas. O relatório usa os pesos escolhidos.

A IA (OpenAI Responses / GPT-5 nano) escreve a leitura contextual de cada ficha, guiada por um roteiro por tema, e explica a sugestão; números são conferidos e qualquer falha volta ao texto por regras. O cabeçalho da coluna mostra “(IA)” quando o texto veio do modelo. Não há diagnóstico real, decisão automática, ML, upload ou implantação pública. [Multicritério e IA](MULTICRITERIO.md), [evidência do recorte](INFLUENCIA.md), [método](DADOS_TERRITORIAIS.md), [verificações](VALIDACAO.md).
