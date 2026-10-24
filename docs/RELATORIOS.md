# Dois relatórios, uma revisão

Antes de exportar, é obrigatório salvar uma comparação válida. Os links usam área + revisão + tipo. A versão do estado, os pesos e os resultados ficam congelados no SQLite; exportar não executa outra decisão.

**Simples:** nome e localização, área, mapa com fotografia, características principais e ano, opções ordenadas, pesos e origem, índice relativo e explicação de alcance, pendências e limitações. Reflete o que o usuário vê na tela.

**Técnico:** inclui todo o conteúdo simples e acrescenta matriz de indicadores, regras/expoentes exploratórios, cobertura amostrada, classes, CRS, qualidade do relevo/cobertura, fontes/datas/hashes, geometria e entrada aceita, AHP e consistência, matrizes normalizadas/ponderadas, ideais, distâncias, TOPSIS, empates e cenários de sensibilidade. Serve à revisão/auditoria do cálculo; não é parecer técnico ambiental ou certificação.

Formato HTML independente, com imagem PNG embutida e sem scripts ou recursos remotos. Nomes recebidos passam por escape HTML. Pode abrir no navegador e imprimir/salvar PDF usando o próprio navegador. Não existe exportação PDF nativa implementada.

Uma alteração posterior de pesos produz outra revisão. Os dois formatos da revisão anterior continuam correspondendo àquele estado, enquanto o cookie da sessão permitir acesso. Guarde os arquivos baixados para consulta independente da sessão.
