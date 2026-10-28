# Ferramentas e justificativas

Versão 4.6.3. As ferramentas abaixo correspondem ao mapa e à caracterização territorial automática implementados.

| Necessidade | Ferramenta | Motivo e resultado |
|---|---|---|
| Interface organizada e estado visual | React | Separa mina, mapa, camadas e exportação; checkboxes visuais não alteram os dados preparados. |
| Contratos da interface | TypeScript | Verifica tipos de configuração, influência e dados antes do build. |
| Identidade/responsividade/acessibilidade | HTML/CSS | Mantém verde/amarelo, textura, barras, máscara visual do recorte, detalhes expansíveis, teclado e adaptação ao celular. |
| Mapa e sobreposições | Leaflet | Reúne tiles, marcador, contornos, WMS e trilhas, com intensidade e legendas. |
| Integração e automação | Python | Implementa consultas, preparação, atualização e leitura no backend. |
| API local | FastAPI/Uvicorn | Serve interface e dados na mesma origem e inicia a preparação no ciclo do servidor. |
| Interseção vetorial | Shapely/GEOS | Recorta registros no polígono comum e preserva partes/atributos. Também confere contornos de navegação. |
| Células e georreferenciamento | Rasterio/GDAL e NumPy | Lê valores GeoTIFF, transforma o recorte para o CRS da grade, mascara células e resume classes sem reamostragem. |
| Análise multicritério | NumPy e Shapely (STRtree) | AHP por autovetor, vegetação no entorno por imagem integral e distâncias pelo vizinho mais próximo, sem nova dependência. Cálculo por célula guardado em cache; mudar pesos refaz só a soma. |
| Persistência por mina | SQLite | Biblioteca padrão Python, transações locais e armazenamento leve de atributos/GeoTIFF; evita refazer consultas a cada clique ou reinício. |
| Limitar concorrência/rede | urllib, threading e ThreadPoolExecutor | Consultas HTTP limitadas e até três bases em paralelo, com repetição automática e estados. |
| Relatório PDF | ReportLab | Marca, mapas em vetor, tabelas e paginação; geração local a partir dos dados guardados. |
| Visualização do documento | pypdfium2 / PDFium | Renderiza PNGs por página no servidor, sem depender de canvas ou worker do navegador. |
| Leitura contextual por dado | GPT-4.1 mini com guia por tema; regras de reserva | Mantém fatos imutáveis e marca “(IA)” quando o texto veio do modelo. Nenhum ML foi treinado. |
| Build e dependências | Node/npm/Vite e ambiente virtual/pip | Interface compilada e ambientes reproduzíveis com locks/hashes, preservando ambiente pessoal. |
| Verificação/versionamento | pytest/TestClient, Node tests, navegador, Git/GitHub | Conferem contratos, falhas, persistência e fluxo real; compartilham o código autorizado. |

## Fontes e formatos

| Fonte/padrão | Papel |
|---|---|
| OpenStreetMap e Esri World Imagery | Fundos de navegação/contexto; OSM também fornece snapshot do sombreado da mina. |
| FEAM / Vale / Amplo | Evidência do contorno externo do estudo conjunto, digitalizado aproximadamente. |
| IDE-Sisema / WMS | Imagens dos dezessete conjuntos estaduais, mascaradas no navegador dentro da influência ou ampliadas por checkbox. |
| IDE-Sisema / WFS | Contorno estadual e quinze bases vetoriais com atributos completos para o território. |
| IDE-Sisema / WCS | Coberturas numéricas de declividade e MapBiomas, em GeoTIFF nativo. |
| Prefeitura de Nova Lima / ArcGIS REST | Trilhas, atributos completos para caracterização e simbologia oficial para visualização. |
| ANM / SIGMINE | Processo, titular e fase cadastral; não fornece o recorte do MVP. |
| IBGE / API de malhas | Município sob seleção; contexto administrativo. |
| GeoJSON / JSON / GeoTIFF | Geometrias, atributos/metadados e todos os valores matriciais associados ao recorte. |

Não é necessário QGIS instalado, Selenium, credencial Google ou serviço de IA. Fontes públicas têm condições de uso e disponibilidade; não são classificadas como ilimitadas. O banco local é gerado no computador e não é enviado ao GitHub.

## Fala para apresentação

> “Usei React/TypeScript e Leaflet para a exploração do mapa. Python/FastAPI organiza a preparação automática. Shapely recorta os registros vetoriais; Rasterio conserva os valores das imagens temáticas; SQLite guarda os resultados por mina. Influência mostra todas as camadas no território e os seletores ampliam cada tema além dele. O relatório PDF organiza todas as bases e um cenário técnico simulado; as informações reais permanecem preservadas. A escolha demonstra integração de dados e automação, com fonte, data e limitações explícitas, antes de qualquer avaliação de alternativas de uso futuro.”

[Justificativas temáticas e do recorte](ESCOLHAS_TERRITORIAIS.md), [método](DADOS_TERRITORIAIS.md), [versões](DEPENDENCIAS.md), [verificações](VALIDACAO.md).
