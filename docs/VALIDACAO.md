# Validação das fichas, da sugestão e da prévia

Versão 4.7.0, 28/10/2026, macOS/Python 3.12/Node 24.

## Automatização

113 testes Python aprovados no conjunto completo. Dois testes Node aprovados. TypeScript (`tsc --noEmit`) e build aprovados. Avisos de depreciação Starlette/HTTPX e Rasterio/NumPy permanecem sem falhas.

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

## Leitura contextual por IA (4.5.0)

Testes: sem chave, nenhuma chamada e textos por regras; com chave, cada ficha recebe o guia do próprio tema, e a ficha cuja resposta traz número não fornecido, interrogação, nome de campo ou letra fora do alfabeto latino volta às regras sem afetar as outras; a ficha 09 mostra “Por que” sem “(IA)” quando não há chave.

Emissão real com a chave local, em 28/10/2026, pelo mesmo código do servidor. Primeira emissão: 7 de 8 fichas com IA, mas a leitura revelou rascunho (“fique objetivo”), uma palavra em hindi e, na sugestão, nomes de campo (“alto_pct”, “true”). Daí vieram a conferência de texto, a nova tentativa por ficha e a entrada da sugestão em frases. Emissão final: 8 de 8 fichas e a sugestão com “(IA)”, 14 páginas, 25,7 s; nenhum dos avisos removidos aparece no PDF. Textos lidos um a um: números iguais aos dos dados, leis citadas só as do guia. Pequenas imprecisões de redação continuam possíveis com o gpt-5-nano; por isso o texto por regras segue como reserva e a revisão técnica continua necessária.

## Explicação pelo terreno, modelo e tela (4.6.0)

Testes novos: a explicação por regras começa pelo uso sugerido e não fala em pontos nem pesos; o perfil do setor guarda declividade por faixa e distâncias (sem linha de transmissão, a distância é nula); a explicação da IA com “vantagem de 34 pontos” é recusada; a mesma explicação pedida duas vezes chama o modelo uma vez; a rota `/sugestao/explicacao` devolve 404, 422 e, sem chave, o texto por regras.

Comparação de modelos com a mesma entrada real (Horizontes, pesos AHP), em 28/10/2026:

| Modelo e ajuste | Resultado |
|---|---|
| gpt-5-nano, raciocínio baixo, todos os fatos | Recusado: passou de 420 caracteres e usou interrogação. |
| gpt-5-nano, raciocínio médio | 87 s e recusado: copiou rótulos (“Por que combina:”) e passou do tamanho. |
| gpt-5-nano, duas frases com fatos escolhidos | Aceito, mas a 2ª frase trocou número (S5: “10% acima de 20%”, quando 10% era APP). Daí a frase sobre os demais usos ficar por regras. |
| gpt-5-nano, só a 1ª frase | Aceito, mas só repetia os fatos, sem dizer o que significam. |
| gpt-4.1-mini, só a 1ª frase, `temperature` 0,2 | Aceito nos 5 setores e interpretando: “57% do setor com declividade acima de 20% dificulta o uso de máquinas, favorecendo o retorno natural da vegetação”. Uma resposta trouxe “visitação segura”; “seguro” passou a ser recusado. |

PDF padrão com gpt-4.1-mini: 14 páginas, 20 s; ficha 09 com “Por que (IA)”; 7 de 8 fichas com IA (Entorno caiu para regras naquela emissão, como previsto).

Tela, numa instância isolada (porta 8031, cópia do banco e da chave): o resultado aparece à esquerda abaixo de Sugerir uso e os pesos à direita; S2 mostrou “Por que (IA)” com a explicação do terreno; mudar o peso de trilhas para 40 fez aparecer Emitir relatório com estes pesos, que abriu “Relatório com pesos ajustados” (`?pesos=34,22,13,13,7,6,40`, 15 páginas); fechar e clicar Ver relatório pediu o PDF sem pesos (“Relatório da mina”).

## Tabela de referência na ficha 09 (4.6.1)

Teste novo: a tabela e o cálculo usam a mesma régua (mesmos usos e critérios), o texto da régua confere com os parâmetros (solar no relevo: “1 · 0,8 · 0,3 · 0 · 0 · 0”) e a função continua igual (conservação a 350 m da drenagem: 0,65). O PDF com pesos ajustados contém “Como a nota é calculada” e a citação de Saaty. Na emissão real, a tabela ficou na página 14, depois das restrições, sem criar página nova (14 páginas).

Setor que abre e fecha (28/10/2026, instância isolada): clicar em S3 na lista abriu o detalhe dentro do item S3, antes do S4, com um único detalhe na tela; clicar de novo fechou (nenhum detalhe, botão com `aria-expanded=false`). No mapa, clicar no S5 aberto fechou o detalhe e clicar outra vez reabriu.

## Ficha 09 em tópicos e passo a passo (4.6.2)

Teste novo: os exemplos do passo a passo saem das mesmas réguas e pesos (quadrado plano: conservação 0,5, ecoturismo 0,8, silvicultura e solar 1; silvicultura a 100 m do rio: 70 ÷ 170; comparações do relevo 2, 3, 3, 4, 5, 5). O PDF contém os tópicos “• Por que”, o “Passo 5” e a “Régua do relevo”. Emissão real: 15 páginas; ficha 09 nas páginas 13 a 15; exemplo do passo 5 no S1 (3% plano ou suave × 1 + 34% ondulado × 0,7 + 58% forte × 0,3 + 5% montanhoso ou escarpado × 0 ≈ 0,44; com 9% proibido, 0,40). Páginas renderizadas e lidas.

## Ficha 09 enxuta (4.6.3)

O teste do PDF passou a exigir os três quadros (“Pesos dos critérios”, “Régua do relevo”), três “Fonte dos parâmetros”, o porquê em tópicos e a ausência do passo a passo e da lista de restrições; o teste e a função do passo a passo saíram com ele. Emissão real: 16 páginas; página 1 com um setor por linha; ficha 09 nas páginas 14 a 16, lida renderizada.

## Quadro único de réguas (4.6.4)

Teste novo: o quadro cobre os 7 critérios, com valores que saem das mesmas funções do cálculo (relevo plano: 0,5 · 0,8 · 1 · 1; drenagem “Perto”, 100 m: silvicultura 70 ÷ 170 e solar 0,2; “até 10%”, “3 km ou mais”; uso que não considera o critério fica sem nota). O PDF tem dois “Fonte dos parâmetros”. Emissão real: 17 páginas; o quadro das réguas ficou inteiro na página 17, sem cortar o relevo.

## Vídeo pós-mineração (4.7.0)

Teste novo: a rota do vídeo devolve 404 sem arquivo e para mina desconhecida, o arquivo inteiro com `video/mp4` e um trecho com 206 quando o navegador pede `Range`. No navegador (instância isolada, porta 8031): com a mina selecionada, Ver pós-mineração aparece abaixo de Sugerir uso, abre o diálogo e o vídeo carrega (9,2 s, 1072×1220, sem erro), com a legenda embaixo. Geração e conferência do vídeo em [Vídeo pós-mineração](VIDEO_POS_MINERACAO.md).

Correção: o botão do relatório e o do vídeo usavam a mesma chave React (o id da mina) no mesmo bloco, e cada atualização deixava cópias de “Preparando relatório…”. Com chaves distintas, selecionar e desmarcar a mina três vezes deixou um botão de cada (relatório, Sugerir uso, vídeo) e nenhum aviso de chave repetida no console.

## Publicação (29/10/2026)

Teste novo: com dados fixos, nada é coletado (a coleta falharia o teste), o território continua completo dois dias depois e o relatório é gerado. Com o banco real de 27/10, servidor em modo de publicação (`GEOVALE_DADOS_FIXOS=1`, `GEOVALE_HOST=0.0.0.0`): 18 de 18 bases prontas, nenhuma coleta no registro, PDF com IA em 30,4 s, vídeo servido e pico de 220,8 MB de memória. O Hugging Face recusou ligar o Space de conta nova (403, cota zero de CPU gratuita); a publicação passou ao Render. O build Docker não foi feito localmente (não há Docker neste computador); ele acontece no Render.

No ar em 29/10/2026, pela Vercel (https://geo-vale.vercel.app, repasse ao Render): página e rotas da interface 200; `/api/saude` 4.7.0; sugestão 200 em 45,5 s com o Render acordando; explicação 200 com método `ia`; relatório PDF 200 em 69,2 s (2.334.174 bytes, abaixo do limite de 120 s da Vercel); página 1 da prévia 200 em 1,9 s; vídeo 206 com leitura por trechos. Direto no Render: 18 de 18 bases prontas.

No ar, o contorno de Nova Lima falhava: o IBGE não responde ao Render (EUA). Teste novo: com dados fixos, o contorno vem de `dados/municipios/3144805.geojson` sem consultar o IBGE. 109 testes passando.

Resultado padrão pronto: `ferramentas/gerar_prontos.py` gerou `dados/prontos/` (sugestão, explicação com método `ia`, relatório de 16 páginas, 2.333.924 bytes) em 39 s. Teste novo: com dados fixos, a API entrega os três sem tocar no território e a prévia da página 1 abre; com pesos, recalcula. 110 testes passando.

## Mina Abóboras (29/10/2026, 4.8.0)

Faixa de 3 km em volta da cava OSM (way 315221702): 4.266 ha. Coleta local só da Abóboras, numa cópia do banco: 18 de 18 bases, depois de aceitar coleção WFS vazia com `crs` nulo (UCs federais e municipais) e declarar `reparar` em massas d’água (1 de 10 geometrias). Na Horizontes, massas d’água recoletada com reparo teve os mesmos 16 registros e geometrias; só a assinatura foi atualizada, e a sugestão da Horizontes calculada ao vivo continuou igual à salva em `dados/prontos`. Relatório da Abóboras: 14 páginas, área minerada de 1.001,9 ha em 3 setores, conservação e restauração em primeiro nos três; página 1 renderizada e lida. No site local em modo publicado: lista com as duas minas, contorno de Nova Lima, influência, sugestão e relatório imediatos, vídeo 404 com aviso. Testes novos: faixa declarada sem distância ou referência é recusada; coleção vazia aceita `crs` nulo e, com registros, continua exigindo o CRS. 112 testes passando.

## Mina Trindade (29/10/2026, 4.9.0)

Cava OSM way 391438666 dentro de Sabará pela malha do IBGE (Barão de Cocais a 21 km). Faixa de 3 km: 4.530 ha. Coleta só da Trindade numa cópia do banco: 14 de 18 na primeira rodada (declividade, cavidades, massas d’água e enquadramento falharam por instabilidade da fonte e responderam na consulta seguinte), 18 de 18 na segunda; as três minas com 18 de 18 no banco final. Trilhas detectadas fora da cobertura. Sugestão: S1 (143,3 ha) ecoturismo 86 e conservação 85; S2 (28,1 ha) conservação 70. Com peso 50 em trilhas o resultado não muda. Sugestões da Horizontes e da Abóboras calculadas ao vivo iguais às salvas. Relatório da Trindade: 13 páginas; página 1 renderizada e lida, com “Sem dado: a camada cobre só Nova Lima” e “1 barragem” (concordância corrigida); a linha de trilhas fica com o texto por regras, depois de a IA ter escrito “rede de trilhas existente no entorno” numa primeira geração. Na tela local: Trindade na lista com Sabará, peso de trilhas cinza com “sem dado nesta mina”. Teste novo: fora da cobertura o critério sai da conta e o peso dele não muda a nota. 113 testes passando.
