# Relatório GeoVale: dado e contexto

Versão 4.5.0, 28/10/2026. Selecionar a mina oferece **Ver relatório**, sem exigir Influência. A marca e autoria são GeoVale.

## Estrutura

A primeira página apresenta influência, área minerada e mina com todos os temas sobrepostos, a área minerada em hectares e um resumo por tema. Seguem sete fichas: relevo e cavidades, água, solos, vegetação/conservação, entorno/infraestrutura, barragens e trilhas. Cada ficha mostra somente seu tema sobre o mesmo recorte, com área minerada e mina, dados objetivos e comentário separado para cada dado. Depois vem a ficha de dados técnicos simulados, com mapa dos pontos e asterisco em cada valor fictício. A última ficha é a **sugestão multicritério**: mapa dos setores pelo 1º uso, pesos usados (AHP ou do engenheiro), notas de 0 a 100 por uso, porcentagem permitida, robustez, condicionantes e explicação por setor, além das restrições com base legal. Não há anexo de atributos.

Os valores observados/calculados ficam na coluna Dado / valor / origem; a leitura contextual fica em outra coluna. Os comentários não substituem ou alteram fatos. Os atributos completos e GeoTIFFs continuam no armazenamento interno.

## Área minerada e entorno

A AII é contexto; o objeto do pós-mineração é a área minerada. Ela é delimitada pelas células da classe Mineração da cobertura MapBiomas guardada, transformadas em polígono sem reamostragem. Na Horizontes: 3.173,3 ha, 20,7% do recorte. A mina OSM tem 512,2 ha e representa só a cava. Cada base vetorial é medida no total, na área minerada e no entorno: linhas pela soma dos trechos, polígonos pela união e pontos por contagem. Outras grades selecionam pelo centro as células que caem na área minerada.

Relevo e solos dentro da área minerada são identificados como anteriores à mineração: Topodata deriva do SRTM de 2000 e o mapa pedológico é de 2010. O PDF informa que avaliar essa área exige levantamento topográfico atual e que o substrato atual é material minerado.

## O que é calculável

Comprimentos e áreas vetoriais são calculados em SIRGAS 2000 / UTM 23S; registros sobrepostos não são dissolvidos no comprimento. Áreas matriciais somam a área de cada célula, obtida pelos quatro vértices projetados em UTM 23S; a soma da grade coincide com a área do recorte. Percentuais de classe são percentuais dessa área.

UCs de todas as esferas são agrupadas pelo campo `grupo` publicado em cada registro: proteção integral ou uso sustentável, com área da união, parte na área minerada e área de cada unidade. Barragens listam finalidade, método construtivo, PDA e classe publicados; alteamento a montante é destacado. Enquadramento soma o comprimento por classe; vazões apresentam o maior Q7,10 no recorte e na área minerada. Cavidades somam a área por grau de potencial. Áreas urbanas e rodovias informam a distância à área minerada.

## Dados técnicos simulados

`dados/cenarios/horizontes.json` contém três pontos de água e seis dados técnicos. Os pontos foram posicionados sobre dados reais: A1 em trecho classe 1 sem mineração a montante, A2 logo a jusante da área minerada e A3 após a confluência. pH, turbidez, ferro dissolvido e manganês total são fictícios. A classe do trecho mais próximo (até 300 m) vem do enquadramento do Igam; sem trecho próximo, vale a classe 2 (CONAMA 357/2005, art. 42). Os limites são os da Resolução CONAMA 357/2005 para a classe; a classe especial não tem padrão numérico.

Os dados técnicos são fator de segurança de talude de pilha (mínimo 1,5 no talude geral com superfície freática normal, ABNT NBR 13029:2017), resistência do solo à penetração (2 MPa, limite crítico usual atribuído a Taylor et al., 1966), sobrevivência de mudas, área de edificação, acessos liberados e participantes de consulta. Os quatro primeiros têm ponto na área minerada; acesso e participação não têm localização. Todos têm **\*** e nota explícita de que não foram medidos na Horizontes.

O Plano Minas-Rio, Anglo American, revisão junho/2021, fundamenta a estrutura de planejamento, vistoria, reabilitação e participação (8.2.1.3-8.2.1.5, 11.11.3 e 11.11.7.6). Não fornece os números simulados e não comprova resultados na mina do MVP.

## Comentários e IA

Cada leitura contextual das fichas indica a implicação do dado para o planejamento pós-mineração (o que favorece, limita ou exige estudo) e um limite do dado. As regras calculam os indicadores, por exemplo a parcela do entorno acima de 20% de declividade ou os quilômetros de drenagem que cruzam a área minerada, e escrevem um texto de reserva.

A IA escreve a leitura de cada ficha e explica a sugestão multicritério, setor por setor. Para as fichas, recebe um guia por tema que ensina a interpretar cada subtema (classes de declividade, Q7,10, enquadramento, grupos de UC, APP, barragens a montante, ZAS, valores simulados). O porquê está em [Multicritério e IA](MULTICRITERIO.md). `comentarios.py` separa leituras e explicações dos fatos por ID. A integração usa a **OpenAI Responses API** e o modelo **gpt-5-nano**, exatamente o solicitado. O modelo está confirmado na [documentação oficial](https://developers.openai.com/api/docs/models/gpt-5-nano), com [Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs).

A chave é colocada somente em `.local/ia.env`, na linha `OPENAI_API_KEY=`. O arquivo tem permissão 600, é ignorado por `.gitignore` e não é enviado ao frontend, PDF, logs ou GitHub. O leitor usa esse arquivo local, não credenciais globais do computador. É relido ao abrir uma emissão; preencher/alterar a chave invalida o cache sem exigir reiniciar o servidor. Uma sessão já aberta deve ser fechada e reaberta.

A aplicação envia para `https://api.openai.com/v1/responses` só texto já calculado: na sugestão, pesos, notas, porcentagem permitida, pontos por critério, condicionantes e robustez, em frases; em cada ficha, nome, valor, origem e texto por regras de cada dado, mais o guia do tema. Sem matrizes/geometrias, com `store=false`, raciocínio baixo, limite de 9.000 tokens de saída e timeout de 60 s. Não envia temperature, incompatível com a configuração escolhida do GPT-5 nano. O JSON Schema é estrito e limita os itens aos enviados. A resposta precisa estar completa; recusa, erro ou truncamento retornam às regras (cada ficha tem uma nova tentativa). Cada texto tem até 420 caracteres, todos os itens precisam estar presentes, números não fornecidos são recusados, assim como interrogação, nomes de campo e letras fora do alfabeto latino.

Quando o texto veio do modelo, o cabeçalho da coluna mostra “Leitura contextual (IA)” ou “Por que (IA)”; texto por regras aparece sem “(IA)”. Verificações de formato não garantem correção semântica de um LLM; revisão técnica continua necessária. Valores de fontes, cálculos e exemplos fictícios não são alterados pelo modelo.

## PDF e prévia

ReportLab gera o PDF. `GET /api/minas/{id}/relatorio` retorna PDF inline; `baixar=true` altera apenas Content-Disposition; `pesos=` leva os sete pesos da sugestão (inválidos: 422). Bases incompletas/vencidas ou cenário inválido impedem geração (503); mina desconhecida retorna 404. O cabeçalho `X-Relatorio-Versao` contém o hash do PDF.

A prévia usa PDFium no servidor: `/relatorio/previa?versao=...` entrega paginação/textos acessíveis; `/relatorio/paginas/{numero}?versao=...` entrega PNG. PDFium opera sob mutex global e fecha recursos explicitamente. São guardadas até quatro versões de PDF e doze imagens, com escala fixa. Versão ausente retorna 409 para reabrir; página inválida retorna 404. Download salva o mesmo Blob da versão aberta.

A assinatura do coletor continua 4.0.0: barragens declaram no catálogo o campo `name`, publicado só no GeoJSON, e a cota constante zero dos pontos. O PDF é gerado do banco atual, não de um arquivo demonstrativo fixo no repositório.
