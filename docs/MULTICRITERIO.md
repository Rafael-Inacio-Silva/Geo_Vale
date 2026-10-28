# Sugestão multicritério e explicação por IA

Versão 4.6.0, 28/10/2026. Esta etapa vem depois da caracterização: o relatório organiza o território e a sugestão ordena usos pós-mineração para cada setor da área minerada. Na referência da Vale, corresponde a apoiar a etapa **Conceber** depois de **Conhecer** ([Fechamento de mina e uso futuro](https://www.vale.com/pt/esg/fechamento-de-mina-e-uso-futuro)). O sistema não decide: o engenheiro ajusta os pesos e leva a sugestão para discussão.

## Fluxo

1. O engenheiro seleciona a mina e clica em **Sugerir uso**.
2. O sistema divide a área minerada em setores contínuos de pelo menos 20 ha.
3. Exclui de cada célula de 30 m os usos que a lei não admite ali: UC de proteção integral, APP, ZAS e superfície d’água.
4. Converte sete critérios em notas de 0 a 1 para cada uso e soma com os pesos. O padrão vem do AHP.
5. O mapa entra no modo sugestão: camadas temáticas saem e os setores aparecem coloridos pelo 1º uso. A barra esquerda, abaixo de Sugerir uso, mostra setores, ranking e explicação; a direita, só os pesos. Escolher um setor (no mapa ou na lista) abre o ranking e o porquê.
6. Testa se o 1º lugar muda com ±20% em cada peso e marca os setores sensíveis.
7. O engenheiro move os pesos; o mapa recalcula. **Ver relatório** é sempre o padrão (pesos AHP); com pesos mudados aparece **Emitir relatório com estes pesos**, que gera o PDF com eles.
8. A IA explica cada setor pelo terreno, no PDF e na tela, e escreve a leitura contextual de cada ficha. Quando o texto veio do modelo, o cabeçalho da coluna mostra “(IA)”; sem chave ou com resposta recusada na conferência, entra o texto por regras, sem “(IA)”.

## Decisões e porquês — fase 3

| Decisão | Por quê | Evidência |
|---|---|---|
| Unidade de decisão: setores contínuos da área minerada (≥ 20 ha) | O uso futuro é decidido no terreno minerado, não nos 15 mil ha da AII. Cava, pilha e barragem não têm cadastro público separado; setores contínuos são a menor unidade honesta com dados públicos. 20 ha evita decidir sobre fragmentos de poucos pixels; o fechamento de 30 m (uma célula) une vizinhos na diagonal. | Plano Minas-Rio 11.7–11.8 (ações na ADA); MapBiomas 30 m, classe Mineração. Na Horizontes, 120,4 ha em fragmentos ficaram fora. |
| Quatro usos | São os quatro grupos do estudo de Ptolemais, adaptados: agricultura vira silvicultura, porque os solos do recorte (Cambissolo e Neossolo litólico) são rasos; parques recreativos viram ecoturismo, que usa as trilhas existentes; uso industrial, que no estudo inclui fotovoltaica, vira energia solar e infraestrutura. | Servou et al. (2023); ficha de solos; Vale, uso futuro. |
| Restrições excluem, não pontuam | Um fator compensa outro numa soma; uma proibição legal não pode ser compensada por boa declividade. Por isso a restrição zera o uso na célula e o setor informa a porcentagem permitida. | Eastman (1999) e Malczewski (2006): restrições booleanas separadas de fatores. |
| Proteção integral só admite conservação; parque e monumento natural também admitem ecoturismo | O SNUC admite apenas uso indireto na proteção integral; parque e monumento natural admitem visitação, estação ecológica não. | Lei 9.985/2000, arts. 7º, 9º, 11 e 12; campos `grupo` e `categoria` de cada UC. |
| APP admite conservação e ecoturismo | Trilha para ecoturismo é atividade de baixo impacto admitida em APP; plantio comercial e estruturas não. | Lei 12.651/2012, arts. 3º (X, c), 4º e 8º. |
| ZAS admite conservação e silvicultura | Na ZAS não há tempo para socorro externo em caso de ruptura; usos com permanência de pessoas (visitação, instalações) ficam inadequados enquanto a barragem existir. | Lei 12.334/2010, alterada pela Lei 14.066/2020; ZAS dos PAEBM publicadas pela FEAM. |
| Superfície d’água admite conservação e ecoturismo | Não se planta nem se instala placa solar sobre reservatório ou lago. | Massas d’água ANA/Igam. |
| Cavidades como condicionante, não restrição | O mapa nacional (1:2.500.000) indica potencial, não cavernas localizadas; excluir 96% da área minerada por ele seria falsa precisão. O setor mostra a porcentagem com potencial alto e pede prospecção. | Decreto 99.556/1990; Jansen, Cavalcanti e Lamblém (2012). |
| Sete critérios | Seguem os critérios físicos do estudo de Ptolemais (declividade e distâncias a povoados, rios, estradas e linhas de transmissão) e acrescentam dois dados locais já integrados: vegetação nativa no entorno e trilhas. | Servou et al. (2023); Pagouni et al. (2024). |
| Notas de 0 a 1 por funções lineares | Cada critério tem unidade própria (classe, metros, fração); a padronização permite somar. Os limites (por exemplo, acesso ideal até 1 km e nulo a 8 km) são valores de partida documentados em `multicriterio.py`, para calibrar com especialistas. | Servou et al. (2023) usam fuzzificação em SIG; Malczewski (2006). |
| Relevo pelas classes da Embrapa | É a classificação da própria Topodata; usos mecanizados e com estruturas preferem plano e suave ondulado, enquanto conservação ganha em relevo forte, onde os outros usos perdem. | Classes de relevo da Embrapa (1979) adotadas pela Topodata. |
| Soma ponderada e média por área do setor | Método compensatório mais usado e fácil de explicar: cada critério contribui com pontos visíveis. Células excluídas valem zero, então a restrição reduz a nota na proporção da área afetada. | Malczewski (2006); Eastman (1999). |
| Pesos padrão por AHP | Os pesos vêm de comparações par a par documentadas, com consistência medida. Relevo pesa mais porque define que usos são fisicamente possíveis; vegetação nativa em seguida porque a matriz natural do recorte (71%) favorece restauração; acesso, cidade, rede e trilhas pesam menos porque afetam um ou dois usos. | Saaty (1980): razão de consistência até 0,10. Matriz atual: 0,012. Soltanmohammadi et al. (2010) aplicam AHP ao uso pós-mineração. |
| Engenheiro ajusta os pesos | O estudo de Ptolemais conclui que o modelo matemático sozinho não basta e precisa de informação qualitativa da mineração. O controle deixa essa informação entrar. Simplificação: um peso por critério, aplicado aos usos em que ele participa; pesos por uso ficam como evolução. | Servou et al. (2023). |
| Sensibilidade ±20% em cada peso | Mostra se a ordem depende de um julgamento frágil. Setor sensível pede discussão antes de qualquer conclusão. | Chen, Yu e Khan (2013); Ligmann-Zielinska e Jankowski (2014): variação de um peso por vez. |
| Modo sugestão separado no mesmo mapa | Os setores coloridos competiam com as cores das camadas temáticas, os pesos ficavam espremidos e o porquê aparecia num balão sobre o mapa. O modo esconde as camadas (e as devolve ao sair), usa a barra mais larga e marca a passagem de Conhecer para Conceber. | Vale, etapas Conhecer e Conceber do uso futuro; teste da primeira versão. |
| Relevo de 2000 mantido, com aviso | É o único relevo público integrado; dentro da área minerada não representa a cava atual. O PDF diz isso e a função aceita trocar a fonte por levantamento atual. | Topodata (SRTM, 2000). |

### Pesos AHP e respostas por uso

| Critério | Peso AHP | Conservação | Ecoturismo | Silvicultura | Solar e infraestrutura |
|---|---|---|---|---|---|
| Relevo (classe Embrapa) | 33,8% | melhor em forte ondulado a escarpado | melhor em suave a ondulado | melhor em plano a suave | melhor em plano |
| Vegetação nativa em ~1 km | 22,0% | sobe de 10% a 60% de nativa | idem, com piso 0,3 | — | — |
| Distância da drenagem | 13,5% | melhor até 100 m | melhor até 200 m | melhor após 200 m | melhor após 300 m |
| Acesso por rodovia | 12,6% | — | melhor até 1 km | melhor até 1 km | melhor até 1 km |
| Proximidade urbana | 7,3% | melhor longe (pressão menor) | melhor perto (demanda) | — | melhor perto (carga) |
| Rede elétrica | 5,8% | — | — | — | melhor até 1 km |
| Trilhas existentes | 5,0% | — | melhor até 300 m | — | — |

Distâncias são medidas em UTM 23S do centro de cada célula até o registro mais próximo dentro do recorte; vias e linhas fora do recorte não foram consultadas.

## Resultado atual da Horizontes (pesos AHP)

| Setor | Área | Estruturas | 1º uso | Nota | Robustez |
|---|---|---|---|---|---|
| S1 | 1.431,9 ha | cava OSM; barragens 405 e 407 | Ecoturismo e lazer | 74 | estável |
| S2 | 925,8 ha | barragens 363 e 365 (Vargem Grande, a montante) | Conservação e restauração | 67 | sensível (Ecoturismo a 0,1 ponto) |
| S3 | 434,6 ha | barragens 331 (B3/B4, a montante), 473 e 476 | Ecoturismo e lazer | 80 | estável |
| S4 | 202,2 ha | — | Conservação e restauração | 84 | estável |
| S5 | 58,3 ha | — | Conservação e restauração | 88 | estável |

Solar e silvicultura ficam atrás em todos os setores principalmente pelo relevo forte. S1 a S3 têm mais de 95% de potencial alto de cavidades, o que exige prospecção antes de qualquer intervenção. Os números vêm da coleta de 27/10/2026 e mudam com novas coletas.

## Decisões e porquês — fase 4 (IA)

| Decisão | Por quê | Evidência |
|---|---|---|
| IA explica a sugestão pelo terreno (4.6.0) | Na 4.5.0 a explicação dizia “lidera com 74; pesaram relevo (27 pontos)”: repetia a conta e não dizia nada que a tabela não mostrasse. Agora a regra escolhe os fatos do terreno que separam o 1º uso do 2º (declividade, vegetação nativa, distâncias, APP) e anota o que cada fato significa para aquele uso (tabela `SENTIDO`: “encosta acima de 20% dificulta máquinas e favorece deixar a vegetação voltar”). O modelo escreve a frase que interpreta por que o uso combina; a frase sobre os demais usos fica por regras, porque nos testes era onde o modelo trocava números (S5: “10% acima de 20%”, quando 10% era APP). Pontos, pesos, nota, vantagem e “seguro” são recusados no texto. | Pedido do engenheiro em 28/10/2026; [Validação](VALIDACAO.md). |
| Perfil físico por setor | Para falar do terreno, cada setor guarda, ponderado pela área das células: parcela abaixo de 8%, de 8% a 20%, acima de 20% e acima de 45% de declividade; vegetação nativa no entorno de 1 km; e a distância mediana até curso d’água, rodovia, área urbana, linha de transmissão e trilha. | Mesmas variáveis do cálculo, sem dado novo. |
| Nota explicada na tela e no PDF | “67” era lido como área ou porcentagem. A nota é o quanto as condições do setor combinam com o uso (100 seria todas ideais), não área nem probabilidade; “Permitido em 95%” virou “Lei permite em 95% da área”. | Pedido do engenheiro em 28/10/2026. |
| Relatório padrão e emissão com pesos | O relatório é o documento de referência: sai sempre com os pesos AHP. Mudar os pesos é exploração; quando o engenheiro quer registrar, usa **Emitir relatório com estes pesos**, e o título do diálogo e a ficha 09 dizem que os pesos são do engenheiro. | Pedido do engenheiro em 28/10/2026. |
| Resultado à esquerda, pesos à direita | O resultado fica abaixo do botão que o gerou (Sugerir uso); a barra direita só com os pesos deixa os controles sem rolagem. | Pedido do engenheiro em 28/10/2026. |
| IA escreve a leitura contextual das fichas (4.5.0) | Na 4.4.0 as fichas ficavam por regras: uma frase fixa por dado. A regra continua calculando (por exemplo, 76,2% do entorno acima de 20%), mas o texto passou ao modelo, que recebe um **guia por tema** com o que interpretar: classes de declividade, Q7,10 e outorga, classes de enquadramento, grupos de UC, APP, ZAS, montante, valores simulados. Assim a leitura cita o que domina em cada dado, sem perder o conhecimento das regras. | Decisão do engenheiro em 28/10/2026; `GUIA` em `comentarios.py`; Ji et al. (2023) justificam a conferência abaixo. |
| Regras continuam calculando | O modelo não faz conta: recebe o valor, a origem e o texto por regras como “apoio” com os indicadores já calculados. Só pode usar números do dado, do apoio ou do guia. | Mesma conferência numérica da sugestão. |
| Uma chamada por ficha, em paralelo, com nova tentativa | Uma ficha recusada volta às regras sozinha, sem derrubar as outras; as oito fichas e a sugestão saem ao mesmo tempo. | Emissão real: 26 a 31 s, 14 páginas ([Validação](VALIDACAO.md)). |
| A IA não escolhe uso nem pesos | A decisão é do engenheiro e das partes interessadas; o modelo não tem informação além dos números enviados. | Servou et al. (2023); Vale, participação social no uso futuro. |
| Saída estruturada e conferida | JSON Schema estrito com a lista exata de setores (ou de dados da ficha); todos presentes; até 420 caracteres; qualquer número fora dos dados enviados derruba a resposta e volta às regras. Também derrubam: interrogação, nome de campo (`_`, true/false) e letras fora do alfabeto latino, porque apareceram na primeira emissão real (rascunho “fique objetivo”, uma palavra em hindi, “alto_pct”). A entrada da sugestão passou a ir em frases, não em campos técnicos. | [OpenAI Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs). |
| Envio mínimo | Só números já calculados e formatados como devem aparecer (nas fichas, os fatos do tema e o guia), sem geometria, `store=false`, chave apenas em `.local/ia.env`. | Configuração da integração em [Relatório](RELATORIO.md). |
| Regras sempre disponíveis; procedência no cabeçalho | A tela mostra a explicação por regras na hora e troca pela da IA quando ela chega (“Por que (IA)”); a resposta conferida fica em cache e é reaproveitada pelo PDF com os mesmos pesos. No PDF, os avisos longos (“Comentários automáticos por regras… não constituem laudo”, “IA não configurada… a decisão é do engenheiro”) saíram: repetidos em toda ficha, poluíam a leitura. A procedência ficou no cabeçalho da coluna, “Leitura contextual (IA)” e “Por que (IA)”, e o aviso de que a sugestão não decide continua no parágrafo da ficha 09. | Pedido do engenheiro em 28/10/2026. |
| Sem ML treinado | Não há histórico rotulado de usos pós-mineração bem-sucedidos para treinar ou validar um modelo. | — |
| Modelo gpt-4.1-mini (4.6.0) | O gpt-5-nano, escolha inicial, produziu rascunho, troca de idioma, nomes de campo e textos que só listavam fatos; com raciocínio médio levava 87 s e ainda era recusado. Com o mesmo prompt, o gpt-4.1-mini interpretou cada fato e passou na conferência numérica em todos os setores. Sem raciocínio interno, aceita `temperature` 0,2, que deixa o texto mais estável. | Troca pedida pelo engenheiro em 28/10/2026; comparação em [Validação](VALIDACAO.md); [documentação do modelo](https://platform.openai.com/docs/models/gpt-4.1-mini). |

## Limites e evolução

- Cava, pilha e barragem não são separadas: exige o cadastro interno de estruturas da Vale.
- Topografia atual (LiDAR ou drone) deve substituir a Topodata dentro da área minerada.
- 13 das 19 ZAS publicadas têm geometria inválida e foram corrigidas com make_valid, declarado e contado na coleta.
- Os limites das funções e os julgamentos AHP são de partida; devem ser calibrados com especialistas e comunidade.
- Pesos por uso, custo de implantação e demanda social medida ficam para a evolução.
- Ver também [Escolhas territoriais](ESCOLHAS_TERRITORIAIS.md) e [Relatório](RELATORIO.md).

## Referências

- Chen, Y.; Yu, J.; Khan, S. (2013). The spatial framework for weight sensitivity analysis in AHP-based multi-criteria decision making. *Environmental Modelling & Software* 48, 129–140.
- Eastman, J. R. (1999). Multi-criteria evaluation and GIS. In: Longley et al. (eds.), *Geographical Information Systems*. Wiley, 493–502.
- Embrapa (1979). Classes de relevo adotadas pela [Topodata](http://www.dsr.inpe.br/topodata/).
- Jansen, D. C.; Cavalcanti, L. F.; Lamblém, H. S. (2012). Mapa de potencialidade de ocorrência de cavernas no Brasil, 1:2.500.000. *Revista Brasileira de Espeleologia* 2(1).
- Ji, Z. et al. (2023). Survey of hallucination in natural language generation. *ACM Computing Surveys* 55(12).
- Ligmann-Zielinska, A.; Jankowski, P. (2014). Spatially-explicit integrated uncertainty and sensitivity analysis of criteria weights in multicriteria land suitability evaluation. *Environmental Modelling & Software* 57.
- Malczewski, J. (2006). GIS-based multicriteria decision analysis: a survey of the literature. *International Journal of Geographical Information Science* 20(7), 703–726.
- Pagouni, C. et al. (2024). Transitional and post-mining land uses: a global review. *Land* 13(7), 1051. [DOI](https://doi.org/10.3390/land13071051).
- Saaty, T. L. (1980). *The Analytic Hierarchy Process*. McGraw-Hill.
- Servou, A.; Paraskevis, N.; Roumpos, C.; Pavloudakis, F. (2023). A geospatial analysis model for the selection of post-mining land uses in surface lignite mines: application in the Ptolemais mines, Greece. *Sustainability* 15(19), 14388. [DOI](https://doi.org/10.3390/su151914388).
- Soltanmohammadi, H.; Osanloo, M.; Aghajani Bazzazi, A. (2010). An analytical approach with a reliable logic and a ranking policy for post-mining land-use determination. *Land Use Policy* 27(2), 364–372.
- Leis: 9.985/2000 (SNUC), 12.651/2012 (Código Florestal), 12.334/2010 e 14.066/2020 (segurança de barragens); Decreto 99.556/1990 (cavidades).
