# Requisitos vigentes — versão 2.0

Revisão autorizada: substituir a referência preditiva por GIS + AHP + TOPSIS, concluir o MVP local com dois mapas reais, simplificar a tela e manter dois relatórios.

| ID | Requisito e aceitação |
|---|---|
| RF-01 | Receber um GeoJSON Polygon/MultiPolygon válido; recusar arquivo inválido com causa compreensível. |
| RF-02 | Mostrar mapa, nome e extensão da área antes da análise. |
| RF-03 | Abrir diretamente a jornada de envio do arquivo GeoJSON do usuário, pelo seletor ou por arraste. Os dois mapas reais de apresentação ficam em arquivos no computador. |
| RF-04 | Ler relevo e cobertura reais dos dois pacotes; dados ausentes ou corrompidos bloqueiam cálculo, sem substituição inventada. |
| RF-05 | Exibir apenas características principais; a matriz completa e metadados permanecem no backend/relatório técnico. |
| RF-06 | Comparar Agricultura, Uso florestal e Recreação em áreas abertas com perfil exploratório explicitado. |
| RF-07 | Permitir pesos percentuais somando 100%, origem manual ou AHP com verificação de consistência. |
| RF-08 | Executar TOPSIS, empates e sensibilidade local aos pesos; não apresentar probabilidade de sucesso. |
| RF-09 | Alterar mapa/prioridades invalida o resultado dependente e impede exportar comparação desatualizada. |
| RF-10 | Salvar revisão imutável com dados, pesos, hipóteses, fontes e cálculo aceitos. |
| RF-11 | Gerar HTML simples e técnico da mesma revisão, sem recalcular o ranking. |
| RF-12 | Não exibir login; isolar análises por sessão anônima na execução local. |
| RF-13 | Informar que viabilidade, autorização, custos, segurança e aceitação social não foram avaliados. |

RN-01: dados reais não validam automaticamente as transformações exploratórias. RN-02: soma de pesos não pode ser corrigida silenciosamente. RN-03: não transformar ausência de estudo em aprovação ou restrição comprovada. RN-04: índice relativo não equivale a aptidão ou probabilidade. RN-05: mapa fora dos recortes pode ser exibido, mas não recebe ranking sem fontes preparadas.

RNF: operação local sem dependência de consultas remotas durante a apresentação; mensagens de erro; sessão HttpOnly/SameSite; validação de origem e tamanho de entrada; persistência SQLite; interface responsiva e controles rotulados; fontes rastreáveis; testes de métodos e de jornada.

Fora desta entrega: treinamento ML, processamento de qualquer mina global, ingestão de SHP/KML/PDF, fotografia como classificador, globo 3D, análise financeira/geotécnica/jurídica, gestão multiusuário, implantação pública. A operação pública exige projeto próprio de autenticação e armazenamento; retirar o formulário de login da demonstração não autoriza exposição pública sem controle.
