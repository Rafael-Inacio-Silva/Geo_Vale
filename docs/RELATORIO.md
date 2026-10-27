# Relatório GeoVale: dado e contexto

Versão 4.2.0, 27/10/2026. Selecionar a mina oferece **Ver relatório**, sem exigir Influência. A marca e autoria são GeoVale.

## Estrutura simples

A primeira página apresenta influência e mina com os seis temas sobrepostos, mais um resumo de todos os dados. Seguem seis fichas: relevo, água, solos, vegetação/conservação, entorno/infraestrutura e trilhas. Cada ficha mostra somente seu tema sobre o mesmo recorte, mina sombreada, dados objetivos e comentário separado para cada dado. A ficha final reúne dados técnicos sem camada, sem mapa e com asterisco em cada valor fictício. Não há anexo de centenas de atributos, síntese de alternativas ou ranking.

Os valores observados/calculados ficam na coluna Dado / valor / origem; a leitura contextual fica em outra coluna. Os comentários não substituem ou alteram fatos. Os atributos completos e GeoTIFFs continuam no armazenamento interno e nos contratos técnicos por base.

## O que é calculável

Contagens por base, classes/valores categóricos e células sem dados vêm da coleta persistida. Comprimentos são somas dos trechos recortados em SIRGAS 2000 / UTM 23S; registros sobrepostos não são dissolvidos no comprimento. Superfícies são áreas da união dos polígonos dentro de cada base, sem duplicar sobreposição interna e sem somar esferas de conservação. São medidas cartográficas aproximadas das fontes, não levantamento cadastral ou área de recuperação.

Percentuais matriciais são de células válidas, não área. O mapa usa cores oficiais dos rasters; reprojeção por vizinho mais próximo e redução de resolução ocorrem somente na apresentação. O processamento e as contagens mantêm a grade nativa. Mapas individuais não incluem outras camadas; o mapa geral compõe os seis temas com transparência e mina/contorno por cima.

Geometria de rio não informa pH, profundidade, volume, vazão atual ou biota. O relatório registra essas ausências. Não há IA preenchendo lacunas como fatos observados.

## Dados técnicos fictícios

`dados/cenarios/horizontes.json` contém oito valores numéricos, unidade e método hipotético: fator de segurança de talude, vazão de projeto de drenagem, pH de uma amostra, resistência à penetração do solo, sobrevivência de mudas, área de uma edificação, acessos liberados e participantes de consulta comunitária. Todos têm **\*** e nota explícita de que não foram medidos na Horizontes. Não têm coordenadas fictícias no mapa.

O Plano Minas-Rio, Anglo American, revisão junho/2021, fundamenta a estrutura de planejamento, vistoria, reabilitação e participação (8.2.1.3-8.2.1.5, 11.11.3 e 11.11.7.6). Não fornece os números simulados e não comprova resultados na mina do MVP. Fonte e URL constam da ficha.

## Comentários e IA

IA generativa é adequada para redigir a leitura contextual de fatos fornecidos. ML preditivo exigiria base rotulada e validação; nenhum modelo foi treinado e nenhuma estratégia de pós-mineração é classificada nesta etapa.

`comentarios.py` separa os comentários dos fatos por ID. A integração usa a **OpenAI Responses API** e o modelo **gpt-5-nano**, exatamente o solicitado. O modelo está confirmado na [documentação oficial](https://developers.openai.com/api/docs/models/gpt-5-nano), com [Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs).

A chave é colocada somente em `.local/ia.env`, na linha `OPENAI_API_KEY=`. O arquivo tem permissão 600, é ignorado por `.gitignore` e não é enviado ao frontend, PDF, logs ou GitHub. O leitor usa esse arquivo local, não credenciais globais do computador. É relido ao abrir uma emissão; preencher/alterar a chave invalida o cache sem exigir reiniciar o servidor. Uma sessão já aberta deve ser fechada e reaberta.

A aplicação envia somente fichas compactas para `https://api.openai.com/v1/responses`, sem matrizes/geometrias, com `store=false`, raciocínio baixo, limite de 9.000 tokens de saída e timeout de 45 s. Não envia temperature, incompatível com a configuração escolhida do GPT-5 nano. O JSON Schema é estrito e limita IDs aos dados fornecidos. A resposta precisa estar completa; recusa, erro ou truncamento retornam às regras. Cada texto tem até 240 caracteres, todos os IDs precisam estar presentes e números não fornecidos são recusados.

Sem chave ou com serviço indisponível, os comentários continuam sendo por regras, com procedência explícita. Não se apresentam esses textos como IA. Não houve chamada real nesta entrega porque o arquivo de chave está vazio; o contrato foi testado com respostas controladas. Verificações de formato não garantem correção semântica de um LLM; revisão técnica continua necessária. Cache por dados/cenário/modelo evita chamadas por página ou download. Valores de fontes, cálculos e exemplos fictícios não são alterados pelo modelo.

## PDF e prévia

ReportLab gera o PDF. `GET /api/minas/{id}/relatorio` retorna PDF inline; `baixar=true` altera apenas Content-Disposition. Bases incompletas/vencidas ou cenário inválido impedem geração (503); mina desconhecida retorna 404. O cabeçalho `X-Relatorio-Versao` contém o hash do PDF.

A prévia usa PDFium no servidor: `/relatorio/previa?versao=...` entrega paginação/textos acessíveis; `/relatorio/paginas/{numero}?versao=...` entrega PNG. PDFium opera sob mutex global e fecha recursos explicitamente. São guardadas até quatro versões de PDF e doze imagens, com escala fixa. Versão ausente retorna 409 para reabrir; página inválida retorna 404. O navegador não renderiza PDF em canvas. Uma falha de imagem não exibe página antiga junto com erro; Tentar novamente recarrega o PDF/manifesto e a página, recuperando também uma versão expirada após reinício do servidor. Download salva o mesmo Blob da versão aberta.

A assinatura do coletor continua 4.0.0 porque coleta/recorte não mudaram. O PDF é gerado do banco atual, não de um arquivo demonstrativo fixo no repositório.
