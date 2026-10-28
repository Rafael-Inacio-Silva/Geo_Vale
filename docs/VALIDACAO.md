# Validação das fichas, da sugestão e da prévia

Versão 4.4.0, 27/10/2026, macOS/Python 3.12/Node 24.

## Automatização

101 testes Python aprovados no conjunto completo. Dois testes Node aprovados. TypeScript (`tsc --noEmit`) e build aprovados. Avisos de depreciação Starlette/HTTPX e Rasterio/NumPy permanecem sem falhas.

Testes da 4.3.0: campo extra e cota zero aceitos só quando declarados; área das células em UTM igual à extensão projetada; área minerada pela classe Mineração com divisão de linhas, polígonos e pontos; UCs por grupo publicado; pontos de água contra a classe do trecho e os limites da CONAMA 357/2005; cenário inválido recusado.

Testes da 4.4.0: pesos AHP somam 1 e têm consistência abaixo de 0,10; pesos do engenheiro são validados e normalizados; contribuições por critério somam a nota; restrição zera o uso; a sensibilidade aponta o critério que troca o 1º lugar; a API devolve 404, 422 e 503 nos casos certos e, com dados sintéticos em que APP, ZAS e água cobrem tudo, só conservação fica permitida; pesos do engenheiro mudam o PDF e aparecem como "ajustados pelo engenheiro". As fichas não chamam a IA mesmo com chave; a explicação por IA só é aceita com todos os setores e sem número fora dos dados enviados.

## Dados e documento reais

Coleta em 27/10/2026 numa cópia isolada do banco local, com o código 4.4.0. O servidor que estava em execução com a versão anterior não foi reiniciado; o banco do projeto recebe as bases novas quando ele for reiniciado.

ZAS: 19 registros listados no BBOX, 12 no recorte, 13 geometrias corrigidas e registradas no aviso; a coleta completa levou 160 s. Linhas de transmissão: 2 no recorte. Área minerada: 3.173,3 ha; 120,4 ha em fragmentos abaixo de 20 ha ficaram fora dos setores. O preparo da sugestão levou 11 s; o recálculo com novos pesos, 0,4 s.

A emissão com pesos AHP tem 14 páginas, 2.328.323 bytes. Foram renderizadas e inspecionadas a visão geral, barragens (com ZAS) e a sugestão multicritério: setores coloridos e rotulados, tabela de notas, robustez, condicionantes e explicação.

## Navegador

Numa instância isolada (porta 8031, cópia do banco): mina selecionada, Sugerir uso calculou e pintou os setores, os pesos AHP apareceram nos controles, o popup de um setor mostrou ranking e explicação, e mudar o peso da vegetação nativa recalculou a lista (S2 passou a ecoturismo, marcado como sensível). Ver relatório pediu o PDF com os mesmos pesos (`?pesos=34,90,13,13,7,6,5`) e a ficha impressa "Pesos ajustados pelo engenheiro". O download byte a byte e a falha provocada de imagem foram conferidos na 4.2.0; esse mecanismo não mudou e não foi repetido.

## Correção após o reinício

Ao reiniciar o servidor com a 4.4.0, o tema Entorno não carregou no mapa. O GetMap de cada base mostrou a causa: o estilo oficial das linhas de transmissão gera erro no banco do GeoServer ("sintaxe de entrada é inválida para tipo double precision"), e um erro derruba a imagem do tema inteiro. A base passou a declarar `mapa=False`: sai da imagem WMS e da legenda, mas continua nos dados, na sugestão e no PDF. As demais 17 bases tiveram GetMap conferido com imagem PNG válida. O aviso de falha no mapa agora diz qual tema não carregou.

Na prévia do relatório, o texto oculto para leitores de tela ficava posicionado em relação ao diálogo e criava rolagem extra abaixo da página. A folha passou a ser o contêiner desse texto e o diálogo não rola mais: conferido no navegador, diálogo com 734 px de altura e rolagem igual; a folha rola 1.388 px (página de 1.356 px mais margens) e termina no fim da página.

## Modo sugestão

No servidor da porta 8024, com Influência ativa e Barragens expandida (6 camadas WMS na tela), Sugerir uso deixou 0 camadas WMS, desabilitou Influência, trocou Camadas pelo painel Sugestão de uso e mostrou os 5 setores na lista e no mapa. Escolher S2 na lista abriu ranking, robustez (sensível) e porquê, com o setor contornado no mapa. Mudar o peso da vegetação nativa recalculou a lista e marcou os pesos como ajustados. Voltar ao território devolveu as 6 camadas, Influência ativa e Barragens marcada.

## IA e alcance

O arquivo de chave permanece vazio: não houve chamada real à OpenAI. O contrato foi testado com respostas controladas. Não houve ML treinado, chamada paga, validação de especialista, ensaio real ou decisão de pós-mineração. Os limites das funções e os julgamentos AHP são valores de partida documentados, não calibrados com especialistas. [Multicritério e IA](MULTICRITERIO.md), [método](RELATORIO.md), [dados](DADOS_TERRITORIAIS.md).
