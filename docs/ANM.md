# Cadastro da ANM

Selecionar a Mina Horizontes consulta somente os atributos do processo **003.964/1950** no SIGMINE da Agência Nacional de Mineração. O vínculo é curado em `dados/minas.json` e apoiado no [documento público da FEAM](https://sistemas.meioambiente.mg.gov.br/licenciamento/uploads/-r1U-OgCZO3dEqex9HShmdqbrC5mgstw.pdf). Não se procura a mina por nome ou proximidade.

## Consulta e contrato

[Camada oficial ANM](https://geo.anm.gov.br/arcgis/rest/services/SIGMINE/dados_anm/MapServer/0?f=pjson), ArcGIS REST `query`, filtro `NUMERO = 3964 AND ANO = 1950`, campos PROCESSO, NUMERO, ANO, NOME, FASE, AREA_HA, SUBS, UF e DSProcesso, **returnGeometry=false**, `f=json`. Até dois registros permitem detectar ambiguidade. Nenhuma geometria cadastral é solicitada, validada, importada ou exibida como área de estudo.

`GET /api/minas/horizontes/processo-anm` retorna `properties` com processo, número, ano, titular, fase, área cadastrada, substância e UF, além de `fonte` com nome, URL e data de consulta. Não é uma Feature GeoJSON. O navegador não escolhe URL ou processo. Mina desconhecida: 404; fonte incompatível/indisponível: 503, com mensagem pública e recarga no cartão. Timeout de 15 s, resposta até 2 MiB, cache em memória por dez minutos com trava e cópia defensiva. Sem download em lote, Selenium ou banco.

O cartão mantém os detalhes sob seta. Empresa, município e complexo são do catálogo; os atributos cadastrais vêm da ANM. Área em hectares é declarada pela fonte, não calculada pelo GeoVale. Fase cadastral não comprova operação ativa/encerrada nem segurança. O cadastro não estabelece perímetro físico, fundiário ou pós-mineração.

Os contornos utilizáveis na delimitação vêm exclusivamente do desenho pessoal ou das [referências do parecer](REFERENCIAS_TERRITORIAIS.md). Falha da ANM não impede essas funções.
