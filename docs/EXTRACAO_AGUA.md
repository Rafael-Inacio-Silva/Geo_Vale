# Caracterização preliminar da água

Versão 3.5.0. Esta etapa responde: **quais trechos hidrográficos e massas d’água cadastrados intersectam o recorte documental de influência de águas e solos?** O sistema consulta geometrias pela API, recorta e organiza os registros. Não lê pixels do mapa nem mede qualidade da água.

## Decisão territorial e fundamento

O recorte fixo é **Águas e solos · AID**, identificador `aid_agua_solos`, da Figura 2.3 do [Parecer nº 64/FEAM/GST/2024](https://sistemas.meioambiente.mg.gov.br/consulta-intervencao/uploads/122024/24642_gvwxhTH__066nrKD6s2u.pdf), PDF p. 18 / impressa 15, mapa de 02/11/2023. A legenda trata de qualidade das águas, dinâmica hídrica/erosiva e alteração dos solos. A escolha utiliza a influência direta documentada para iniciar a caracterização de água superficial; não troca essa área por município, raio genérico, processo ANM ou referência OSM.

A influência pertence ao **projeto conjunto de ampliação Tamanduá/Horizontes**. O vetor utilizado é uma digitalização aproximada do mapa raster, não arquivo cadastral oficial. Essa aproximação afeta quais registros próximos à borda entram no resultado. Não é uma área de fechamento certificada. Procedência, hash e precisão em [Referências territoriais](REFERENCIAS_TERRITORIAIS.md).

O [Plano de Fechamento de Mina do Complexo Minerário — Sistema Minas-Rio, Anglo American](https://brasil.angloamerican.com/~/media/Files/A/Anglo-American-Group-v5/Brazil/sustentabilidade/plano-de-fechamento-de-mina-do-minas-rio.pdf), revisão de junho de 2021, distingue abrangência e intervenção. Em **11.7, PDF p. 64 / impressa 58**, o PRAD abrange a ADA e considera a AID quando identificada interferência que requeira reabilitação. Em **11.8**, na mesma página, identifica público interno e população da AID do meio físico. Isso fundamenta investigar o contexto sem assumir que toda influência requer obras ou recuperação. O plano é de outro empreendimento: seus limites não são transferidos para Horizontes.

**A extração GIS é uma adaptação nossa para o MVP**, não uma rotina ou lista obrigatória prescrita pela Anglo ou pela Vale. Organizar dados públicos antes de avaliar alternativas demonstra as atividades da vaga de integrar dados e automatizar etapas de avaliação. Não foi obtido plano de fechamento específico de Horizontes.

## Uso na apresentação

> “Depois de conhecer o território no mapa, o engenheiro pode extrair os dados públicos de água no recorte de influência de águas e solos do estudo disponível. O backend consulta duas bases oficiais, recorta as geometrias e apresenta registros, fontes e datas. É uma caracterização territorial preliminar para organizar informações relevantes ao planejamento de fechamento e uso futuro. A distinção entre influência e intervenção tem apoio no plano de fechamento do Minas-Rio; a implementação automatizada é nossa adaptação para o MVP. O resultado não mede qualidade da água nem define o que recuperar.”

Demonstração: selecionar **Horizontes → Influência → Extrair dados de água**. Não é necessário desenhar ou usar a referência antes. Mostrar as contagens, ligar/desligar o resultado no mapa e abrir Registros e fontes. Explicar que **trechos não são rios distintos**, que o estudo é do projeto conjunto e que data de consulta não é data de levantamento.

## Bases efetivamente consultadas

As mesmas duas bases do tema visual Água e drenagem são acessadas por **WFS 2.0.0**, no [GeoServer oficial da IDE-Sisema](https://geoserver.meioambiente.mg.gov.br/ows). O WMS continua entregando somente imagens para exploração; a extração usa GeoJSON vetorial.

| Conjunto | Camada e identificação | Campos utilizados / referência publicada |
|---|---|---|
| [Principais trechos hidrográficos](https://idesisema.meioambiente.mg.gov.br/geonetwork/srv/por/catalog.search#/metadata/ebb215b7-10a5-481b-8cb2-823b4cf3d5e4) | `IDE:ide_0104_mg_hidrografia_principal_lin`, chave `id` | `noriocomp`, `dsversao`, `datverbase`. Consulta real: BHO de 2017, versão de 22/06/2018; revisão GEIRH de 07/11/2022. Não contém necessariamente toda drenagem local. |
| [Massas d’água](https://idesisema.meioambiente.mg.gov.br/geonetwork/srv/por/catalog.search#/metadata/537a07b7-4a29-422d-bdde-43ae8af87b61) | `IDE:ide_0103_mg_massa_dagua_bho_pol`, chave `id_0` | `nmoriginal`, `nmalternat`, `detipomass`, `deversao`. Registros encontrados publicam FBDS (2017) e `bho_massa_dagua_2019`; essas versões não datam igualmente cada geometria. Nome pode estar ausente; não é inventado. |

Não se deduz segurança, uso atual, titularidade ou condição da barragem do nome cadastral. “Artificial” é a classificação publicada de massa d’água, não avaliação do sistema.

## Método e contrato

`GET /api/minas/horizontes/agua-influencia` utiliza o pacote local conferido e **sempre o mesmo recorte AID**. Não aceita URL, camada ou recorte arbitrário. Mina desconhecida retorna 404; pacote indisponível ou qualquer base incompleta/inválida retorna 503, sem resumo parcial ou valores zero inventados.

1. O backend consulta as duas bases fixas em paralelo. Usa `GetFeature`, `srsName=EPSG:4326`, campos explícitos, ordenação pela chave e `CQL_FILTER=BBOX(geom,...,'EPSG:4326')` com o envelope do recorte.
2. Confere FeatureCollection, CRS, `numberMatched`, `numberReturned`, número recebido, identidade única e geometria válida. Limites por base: 2.000 registros aceitos, 12 MiB e timeout de 15 s. Solicita `count=2001` para detectar excesso; resposta truncada, CRS inesperado, geometria inválida ou campo obrigatório ausente não geram sucesso. Não repara geometrias externas silenciosamente.
3. Shapely faz a **interseção exata com o vetor aproximado**, não apenas com seu retângulo. Retém as partes lineares dos trechos e as superfícies das massas. Exclui contato apenas pontual de linha e apenas linear de polígono. Um registro recortado em várias partes continua contado uma vez. Trechos diferentes do mesmo rio permanecem separados.
4. Entrega FeatureCollection somente com as porções no recorte; inclui identificador original, nome se publicado, categoria, versão/revisão quando disponíveis, totais por base, consulta UTC, fonte/figura/data do recorte, hash do PDF e hash da Feature usada. Sem cálculo de área, distância, volume ou vazão.

O envelope é uma otimização de transferência. A comparação `numberMatched = numberReturned = quantidade recebida` evita tratar a primeira página como a base inteira. A referência técnica é a [documentação WFS GeoServer](https://docs.geoserver.org/main/en/user/services/wfs/reference/) e seus [filtros espaciais](https://docs.geoserver.org/main/en/user/filter/filter_reference/).

Cache em memória: **um resultado completo por 600 s**, chaveado pelo conteúdo do recorte e a evidência do parecer, com trava e cópia defensiva. Não existe atualização periódica, Selenium, download estadual em lote ou banco. Consultar novamente pode reutilizar o resultado dentro dos dez minutos, mantendo sua data original. Após expirar, falha não entrega resultado vencido como atual. Encerrar o servidor descarta o cache.

## Interface e limites

O comando fica no modo Influência, depois dos filtros. Estes controlam só a visualização: **não escolhem o recorte do cálculo**. A extração não depende de WMS, ANM, IBGE ou fundo de satélite estarem disponíveis. Somente o pacote local e as duas bases WFS são necessários para o resultado.

O resumo apresenta contagens, data da consulta e detalhe expansível com registros/fontes/versões. Sem nome cadastral aparece Sem nome publicado. O checkbox Mostrar água recortada no mapa controla somente o resultado azul, separado do tema WMS. Tooltip informa nome, categoria e ID. A camada não reenquadra a câmera e fica entre influência (pane 430) e desenhos (450), em pane 440.

Alternar modo oculta o resultado cartográfico e conserva a consulta para quando voltar a Influência. Ocultar a barra conserva também a camada. Desmarcar a mina cancela o pedido e limpa resultado/crédito; rascunhos e áreas pessoais permanecem independentes. Atualizar a página descarta o estado. Consultar novamente limpa o resultado anterior enquanto carrega; uma falha oferece nova tentativa. Resposta vazia completa significa apenas nenhum registro dessas bases no recorte.

Esta etapa **não extrai dados dentro de polígonos manuais, da referência OSM, do município ou de outras influências**. Também não extrai solos/vegetação/relevo nem avalia impactos, beneficiários, necessidade de intervenção, qualidade ou aptidão. Os demais cinco temas e a trilha continuam como exploração visual. AID, ADA e referência continuam com seus significados próprios.
