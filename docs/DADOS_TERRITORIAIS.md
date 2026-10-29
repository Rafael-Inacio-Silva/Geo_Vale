# Dados do território — preparação automática

Versão 4.7.0. O sistema associa os dados de **todas as bases do catálogo** a cada mina e ao seu único recorte de influência. O engenheiro consulta o resultado preparado. Seletores visuais, intensidade, fundo e enquadramento não são parâmetros de processamento.

## Catálogo único e abrangência

`backend/geovale/camadas.py` declara as mesmas dezoito bases usadas na visualização: dezessete estaduais da IDE-Sisema e a trilha municipal. Cada base informa seu adaptador de dados: WFS, WCS ou ArcGIS REST. O ciclo percorre o catálogo completo, sem uma lista paralela de bases para análise e sem totais preenchidos manualmente.

Adicionar uma base com adaptador compatível ao catálogo faz sua preparação entrar automaticamente na próxima execução do ciclo. Uma fonte de outro protocolo requer implementar seu adaptador. A aplicação não descobre sozinha novas camadas externas. Alteração do código do catálogo requer reiniciar o servidor para carregá-la. Novos registros publicados na fonte entram na próxima atualização automática.

Todos os temas utilizam o **mesmo recorte aproximado da AII de águas/solos**, por simplificação do MVP. O recorte é conferido em arquivo local e vinculado à evidência. Não representa limite de intervenção ou influência temática oficial para todos os assuntos. [Origem e precisão](INFLUENCIA.md).

## Vetores: registros e todos os atributos

O adaptador WFS consulta `DescribeFeatureType`, descobre campo geométrico e todos os atributos, depois solicita `GetFeature` com BBOX do recorte e EPSG:4326. Não restringe `propertyName` a nomes selecionados. Confere `numberMatched = numberReturned = número recebido`, identidades únicas, CRS, tipo/validade das geometrias e correspondência exata entre atributos e esquema. Limite de 2.000 registros por base, leitura até 32 MiB, timeout de 25 s por requisição. Excesso/truncamento é falha explícita, não primeira página apresentada como base completa. Exceções são declaradas no catálogo por base: barragens publicam no GeoJSON o campo `name`, ausente do esquema, e pontos com cota constante zero, removida antes da validação; outra cota ou campo não declarado continuam sendo falha. A ZAS declara `por_registro`: a resposta conjunta excede 32 MiB, então o adaptador lista os IDs no BBOX e lê cada registro completo, conferindo identidade e CRS. Também declara `reparar`: 13 das 19 geometrias publicadas são inválidas; make_valid é aplicado, mantém só a dimensão de polígono, e o aviso registra quantos registros foram corrigidos. Massas d’água também declara `reparar` (1 de 10 geometrias inválidas na faixa da Abóboras). Sem registros no recorte, o servidor publica `"crs": null`; só esse caso dispensa a conferência de CRS.

Shapely intersecta as geometrias com o vetor irregular da influência; o envelope serve apenas para reduzir transferência. Contato apenas pontual não vira trecho, e contato apenas linear não vira superfície. Todas as partes do mesmo registro são mantidas e contadas uma vez. Geometrias inválidas são recusadas sem reparo automático.

Os registros guardam **todos os atributos publicados**, incluindo valores nulos, campos adicionais e identificador original. Geometria entregue é somente a porção no recorte. Valores cadastrais de área, comprimento, vazão, uso ou data continuam com significado e unidade da fonte; **não são recalculados nem apresentados como medidas da porção recortada**. Trechos de um rio contam separadamente. Registros de conservação de esferas diferentes não são unidos.

Trilhas usam a API ArcGIS REST municipal com metadados de campos, contagem prévia, `outFields=*`, EPSG:4326 e verificação de truncamento/IDs antes do mesmo recorte. O processamento de dados conserva todos os atributos; a camada visual municipal continua com sua consulta leve e simbologia oficial.

## Rasters: células e classes, sem leitura de cores do mapa

Declividade Topodata e cobertura MapBiomas 2025 são obtidas por **WCS 2.0.1**, como GeoTIFF numérico, não por captura WMS. `DescribeCoverage` fornece CRS, eixos e resolução. Solicita-se somente o envelope da influência, com margem de dois pixels. Não há `scale`, redução de resolução ou download do estado inteiro. Limites de 4 milhões de células, uma banda categórica uint8, NoData 0 e 32 MiB; saída deve conservar CRS nativo SIRGAS 2000/EPSG:4674 e resolução descrita.

Rasterio transforma o contorno para o CRS da grade e seleciona todas as células cujo **centro** está no polígono (`all_touched=false`). Guarda os valores na posição original, mascarando fora do recorte/NoData. Conserva grade, transformação, resolução, tags, metadados e GeoTIFF; não interpola valores. O histórico de idade dos dados permanece sendo o das fontes.

Os códigos, nomes e cores vêm do **estilo padrão oficial** via GetStyles. Outra classificação alternativa no mesmo SLD não é misturada. Classe sem legenda oficial gera falha. O armazenamento conserva quantidades por classe e percentual de **células válidas**. O relatório apresenta áreas por classe somando a área de cada célula, obtida pelos quatro vértices projetados em UTM 23S; não usa medidas em graus nem trata contagem de células como área. Células sem dados são informadas separadamente. Todos os valores ficam no GeoTIFF guardado. O PDF apresenta classes, contagens e medidas geométricas por tema; não reproduz matrizes ou listas de coordenadas em texto. O armazenamento interno conserva os dados completos.

## Persistência e atualização

SQLite, biblioteca padrão Python, guarda cada combinação mina/base em `.local/territorios.sqlite3`, com WAL, transações, resultado JSON comprimido e GeoTIFF quando aplicável. Essa pasta é ignorada pelo Git. Reiniciar aplicação ou navegador não apaga os dados preparados.

O ciclo começa automaticamente na abertura do servidor, confere pendências a cada minuto e usa no máximo três consultas de bases em paralelo. Dados válidos são renovados a cada **24 horas** enquanto o servidor está ligado. Falha tenta novamente após **cinco minutos**, respeitando a passagem do ciclo. Um servidor desligado não atualiza; ao religar, verifica o que venceu.

A assinatura por base inclui sua definição, pacote de influência/evidência e versão do método. Uma base nova não obriga refazer as existentes; mudança do recorte invalida todos os resultados incompatíveis. Cada base grava sua resposta completa atomicamente. Falha não produz zero artificial: sem consulta válida, fica indisponível; com consulta anterior da mesma assinatura, esta permanece identificada por data e aviso de falha/atualização. Resultado de outro recorte não é reaproveitado.

Estados: pendente, processando, pronto e erro. Somente o catálogo inteiro válido e atual recebe `completo=true`; a interface usa esse estado para habilitar a exportação. Uma base vazia completa recebe zero no relatório; isso não prova ausência no terreno. Data de consulta/processamento não é data de levantamento. As respostas guardam serviço, hashes, esquema/atributos ou metadados matriciais e fonte do recorte.

## Visualização e exportação

Selecionar a mina lê contorno e estado guardado. A seleção pelo cartão ou pela bolinha mostra o contorno da mina automaticamente. **Influência** acrescenta/retira contorno externo e todas as camadas recortadas, preservando o contorno da mina enquanto selecionada. Os checkboxes da direita ampliam apenas a representação de um tema além da influência. Desmarcar restaura sua representação recortada; não oculta dados do relatório.

Base declarada com `mapa=False` (linhas de transmissão, cujo estilo WMS oficial falha no GeoServer) fica fora da imagem e da legenda, sem sair dos dados. As imagens WMS oficiais mantêm estilo/ordem e são mascaradas no navegador por um `clip-path` derivado do mesmo polígono irregular. O envelope limita tiles solicitados; a máscara efetua o recorte visual. A máscara usa coordenadas Leaflet da camada e acompanha enquadramento, zoom, redimensionamento e barras. As imagens recortadas ficam ocultas durante a animação de zoom para evitar recorte deslocado. Não há interpretação de valores a partir dessas cores. Trilhas visuais são intersectadas em Shapely no backend, com nomes/cores municipais preservados; sua expansão usa a consulta normal por bbox.

A representação visual consulta os serviços atuais; o relatório é uma fotografia dos dados persistidos na data indicada por base. Não se promete igualdade temporal entre uma imagem WMS atual e uma coleta anterior. Erros visuais não apagam o banco nem viram ausência de registros.

**Ver relatório**, disponível ao selecionar a mina, lê `GET /api/minas/{id}/relatorio`. A API gera PDF a partir dos dados persistidos e do cenário local de `dados/cenarios/horizontes.json`. Todas as bases entram no documento, independentemente de Influência ou seletores. O PDF apresenta visão geral de todos os temas, um mapa por tema, contagens, classes, medidas calculadas e comentários separados; fontes e datas acompanham cada ficha. Atributos/GeoTIFF completos continuam internos. A API de registros por base permanece sendo um contrato técnico, sem exportação JSON na interface.

A geração exige bases completas e atuais na assinatura vigente. Preparação, erro, vencimento ou mudança de recorte impedem apresentar um relatório como completo (503). O cenário precisa estar explicitamente identificado como simulado e vinculado à mina. ReportLab gera o PDF e a marca; PDFium renderiza as páginas em PNG no servidor, entregues por versão ao navegador com texto acessível. Download usa os mesmos bytes visualizados. [Formato, cenário e limites](RELATORIO.md).

## Justificativa e limites para apresentação

> “Cada mina tem um território e um conjunto de dados preparados automaticamente. O botão Influência mostra todas as camadas dentro do território; marcar um tema permite ver sua continuidade fora dele. O sistema guarda todas as bases integradas e apresenta as informações em um PDF padronizado, complementado por um cenário técnico simulado identificado. Consultamos os serviços oficiais, preservamos atributos e valores, recortamos pela mesma influência e guardamos fonte, data e estado. Isso demonstra integração de dados e automação para caracterização territorial preliminar, antes de avaliar alternativas de uso futuro.”

O [plano de fechamento Minas-Rio da Anglo American](https://brasil.angloamerican.com/~/media/Files/A/Anglo-American-Group-v5/Brazil/sustentabilidade/plano-de-fechamento-de-mina-do-minas-rio.pdf), revisão de junho/2021, **11.7–11.8, PDF p. 64 / impressa 58**, distingue ações na ADA e consideração da AID quando há interferência a reabilitar, e identifica público interno/população da AID física. Fundamenta separar investigação e intervenção. Não prescreve nosso pipeline ou recorte comum; ambos são adaptações explícitas do MVP. Seus limites não foram transferidos para Horizontes.

O protótipo organiza dados, indica implicações por dado e ordena usos por setor para discussão ([multicritério](MULTICRITERIO.md)); não mede qualidade da água, contaminação, impacto causal, estabilidade, beneficiários ou aptidão. Não classifica alternativas nem recomenda uso futuro. A abrangência dos dados vai além dos temas visuais por conter seus registros/atributos; ainda não é diagnóstico completo de um especialista. [Justificativa temática](ESCOLHAS_TERRITORIAIS.md).
