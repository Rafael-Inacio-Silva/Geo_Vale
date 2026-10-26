# Cadastro e polígono da ANM

Na versão 3.3.0, selecionar a Mina Horizontes consulta o processo **003.964/1950** diretamente no SIGMINE da Agência Nacional de Mineração. O vínculo entre processo e empreendimento é curado no catálogo local e apoiado no [documento público da FEAM](https://sistemas.meioambiente.mg.gov.br/licenciamento/uploads/-r1U-OgCZO3dEqex9HShmdqbrC5mgstw.pdf). Não se procura uma mina apenas por nome ou por proximidade.

## Fonte e contrato

[Camada oficial ANM](https://geo.anm.gov.br/arcgis/rest/services/SIGMINE/dados_anm/MapServer/0?f=pjson), ArcGIS REST `query`, filtro `NUMERO = 3964 AND ANO = 1950`, campos PROCESSO, NUMERO, ANO, NOME, FASE, AREA_HA, SUBS, UF e DSProcesso, geometria com `outSR=4326`, `returnZ=false`, `f=geojson`, no máximo dois registros para detectar ambiguidade. A camada nativa informa SIRGAS 2000; a resposta solicitada é EPSG:4326.

`GET /api/minas/horizontes/processo-anm` entrega uma Feature Polygon com propriedades controladas, origem `processo_anm`, finalidade `area_de_estudo` e fonte/data da consulta. O número e ano vêm de `dados/minas.json`; o navegador não escolhe URL, titular ou processo arbitrário. Mina desconhecida retorna 404; fonte indisponível/incompatível, 503 com mensagem pública. Timeout externo de 15 segundos e resposta limitada a 2 MiB. Cache de dez minutos em memória, cópia defensiva e trava contra consultas simultâneas duplicadas. A renovação ocorre sob demanda, sem Selenium, tarefa agendada ou download dos processos de MG.

A validação confere uma única feição, número/ano/UF, titular e fase não vazios, área cadastral numérica finita, ausência de truncamento, posição em MG e polígono simples válido. O contrato desta mina aceita um anel sem buracos, de 3 a 500 vértices. Geometrias diferentes exigem revisar a integração; não são achatadas ou reparadas silenciosamente.

Consulta real em 26/10/2026 retornou **VALE S.A.**, **CONCESSÃO DE LAVRA**, **FERRO** e **471,39 ha**, com 12 vértices distintos. São atributos cadastrais da fonte nessa consulta. A área em hectares é fornecida pela ANM; o GeoVale não a calculou. A fase cadastral não informa se a operação está ativa ou encerrada.

## Interface

Os detalhes ficam dentro do cartão da mina, fechados por padrão e acessíveis pela seta. Empresa, município e complexo são do catálogo; titular, fase, processo e área cadastrada vêm da consulta ANM. Falha oferece Recarregar ANM e preserva o mapa e as outras fontes. A consulta é compartilhada entre cartão e botão de polígono.

**Polígono ANM** fica desabilitado até selecionar a mina. O botão carrega a geometria, mostra uma prévia e exige Confirmar área ou Cancelar. A confirmação preserva geometria e origem cadastral. Havendo outras áreas, acrescenta uma área independente. Ajustar e confirmar uma geometria importada produz uma área de origem **desenho_manual**, sem conservar a identificação de polígono oficial. Cancelar restaura a última área confirmada e mantém todas as outras demarcações.

O polígono do processo minerário **não equivale ao perímetro físico, operacional ou pós-mineração da mina**. Usá-lo como recorte não comprova propriedade, segurança, aptidão ou liberação da área. Não se versionaram os arquivos MG/KMZ baixados pelo usuário; a aplicação consulta a fonte oficial.
