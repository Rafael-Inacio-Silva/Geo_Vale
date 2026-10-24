# Método e limites

## Objetivo

Comparar três possibilidades para aprofundar estudos: agricultura, uso florestal e recreação **em áreas abertas**. A saída é prioridade relativa de estudo territorial. Não é escolha definitiva de uso, previsão, probabilidade de sucesso, licença ambiental ou diagnóstico de aptidão física completa.

## Fundamentação da abordagem

A [Anglo American](https://www.angloamerican.com/our-stories/trusted-corporate-leader/developing-our-post-mine-land-use-ecosystem-model) descreve planejamento pós-mineração com múltiplas alternativas e dimensões de valor. O [instrumento do CRC TiME](https://crctime.com.au/resource/tool-post-mining-land-use-options-assessment-tool/) trabalha avaliação de opções e aprofundamento financeiro; não é uma base supervisionada de exemplos corretos para treinar nosso modelo. O [MRIWA](https://www.mriwa.wa.gov.au/research-projects/project-portfolio/post-mining-land-use-practice-mapping-options/) registra a necessidade de evidências para decisões de uso pós-mineração.

[Singh et al. (2024)](https://www.frontiersin.org/journals/earth-science/articles/10.3389/feart.2024.1330217/full) apresentam aplicação de AHP e TOPSIS ao tema. [Worden et al. (2024)](https://doi.org/10.1016/j.resourpol.2024.104680) estudam análise espacial multicritério para usos pós-mineração. A [revisão de 2024 em Land](https://www.mdpi.com/2073-445X/13/7/1051) discute métodos de decisão para o tema. Essas fontes sustentam o tipo de abordagem e a necessidade de múltiplas dimensões; **não demonstram que os coeficientes, a janela de entorno ou as associações de classes implementadas aqui sejam adequados às duas minas ou à Vale**.

## Entrada e triagem implementada

Um GeoJSON WGS84 com uma feição Polygon ou MultiPolygon, até 1 MiB e 20 mil posições. A validação preserva partes, buracos e altitudes no documento original; não corrige geometrias automaticamente. A superfície de trabalho usa longitude/latitude, inclusive quando posições 2D e 3D aparecem misturadas. Números fora da representação finita suportada são recusados com mensagem de entrada inválida. Cálculo métrico em UTM local; validação adicional recusa amplitude longitudinal maior que 6° e centroides fora de −80° a 84°. Não é um calculador global de áreas.

A análise completa exige correspondência geométrica com um dos dois recortes preparados, integridade SHA256 de todo o pacote e cobertura raster suficiente. Nome de arquivo não decide a mina. Rasters precisam representar todas as partes, ter pelo menos nove células válidas e cobertura mínima de 90% conforme a extração. Ausência de dados não é nota zero nem aprovação. A validação do arquivo e a integridade da fonte são condições para calcular; não são certificações do território.

**Não foi implementada triagem jurídica, de contaminação ou estabilidade geotécnica.** Esses itens permanecem explicitamente não avaliados. Uma comparação territorial pode ser exibida com essas pendências, mas a decisão de uso permanece pendente de estudos. Uma restrição real conhecida não pode ser compensada por notas; a implantação operacional deverá acrescentar esse bloqueio antes de recomendar um uso.

## Caracterização real

- Área: geometria projetada em UTM, sem usar área dos pixels como área cadastral.
- Declividade: derivadas de Horn na vizinhança 3×3 do DEM, em metros; mediana e percentil 90 em graus. Bordas e vizinhanças sem dados não são preenchidas.
- Cobertura: contagem de centros de células dentro da área e no anel externo de 1 km. Denominador de percentuais é a contagem válida; NoData e limites de amostragem ficam no relatório técnico.
- Fotografia aérea: apenas contexto visual; não é entrada para classificação por visão computacional.

## Matriz exploratória de três critérios

Todos os critérios são tratados como benefício no TOPSIS. Não há estimativa automática de custo, segurança ou benefício social.

| Critério | Medição / transformação |
|---|---|
| Cobertura atual associada à opção | Percentual das classes associadas dentro do contorno |
| Contexto do entorno | Percentual das mesmas classes no anel externo de 1 km |
| Relevo exploratório | Média de `100 × (1 − declividade_em_graus / 90)^p` nas células válidas |

| Opção | Códigos NLCD associados | Expoente p |
|---|---|---:|
| Agricultura | 81 (pastagem/feno), 82 (cultivos) | 3 |
| Uso florestal | 41, 42, 43 (tipos de floresta) | 1 |
| Recreação em áreas abertas | 21 (ocupação aberta), 71 (herbáceas) | 2 |

**Esses expoentes, associações e anel de 1 km são hipóteses do protótipo, não parâmetros calibrados nem critérios aprovados pela Vale.** Não há limiar universal de declividade de agricultura, floresta ou recreação derivado dessas fontes. O critério de relevo apenas demonstra uma transformação monotônica explícita. Os dois mapas não validam essa transformação.

A classe 21 inclui gramados e ocupação residencial, não apenas parques; 71 não demonstra existência ou autorização de recreação. Floresta atual não prova possibilidade de recuperação florestal. Pastagem/feno não significa aptidão para qualquer cultivo. Cobertura existente e entorno podem se correlacionar e reforçar a mesma característica duas vezes. Isso exige revisão por especialistas e não é resolvido apenas pela soma dos pesos.

## AHP: prioridades

Três comparações par a par formam matriz recíproca 3×3, com valores entre 1/9 e 9. O autovetor principal positivo é normalizado para soma 1. Calculam-se lambda máximo, `CI=(lambda−n)/(n−1)` e `CR=CI/RI`, com RI=0,58 para n=3. Aceita-se CR≤0,10 como política do protótipo. Consistência matemática não comprova validade técnica ou consenso.

A inicialização usa importância igual. Para a edição percentual em duas casas, os valores aparecem como 33,34%, 33,33% e 33,33%. Esse arredondamento fica registrado e são estes percentuais aceitos que entram no TOPSIS. O usuário pode ajustar manualmente, mantendo soma de 100%; nesse modo a origem é manual, não AHP. Pesos iniciais não pertencem a um especialista da Vale.

## TOPSIS: comparação

1. Normalização vetorial por coluna: `r_ij=x_ij/sqrt(soma_i(x_ij²))`.
2. Matriz ponderada: `v_ij=w_j × r_ij`.
3. Ideais positivo e negativo: máximo/mínimo por critério de benefício; o núcleo também suporta critérios de custo.
4. Distâncias euclidianas `D+` e `D−` aos ideais.
5. Índice `C_i=D−/(D+ + D−)`, ordenação decrescente.

Colunas totalmente nulas não discriminam. Alternativas idênticas recebem 0,5 com aviso de ausência de discriminação. Empates usam tolerância 1e−10 e posições compartilhadas. O índice não é porcentagem de aptidão. A posição e o índice dependem do conjunto de alternativas, da normalização e das hipóteses: não se comparam índices de minas diferentes como se fossem uma escala absoluta.

## Sensibilidade e pendências

Varia-se cada peso em ±10 pontos percentuais, redistribuindo proporcionalmente o restante e preservando 100%. Cenários impossíveis são omitidos. Informa-se se a liderança mudou; não é análise de incerteza probabilística nem validação dos escores territoriais. Também não testa todas as alterações possíveis das hipóteses de nota.

Para uso real: avaliar qualidade e atualidade de fontes, solo/clima, água, geotecnia, contaminação, restrições legais, infraestrutura, custos e demanda social; validar alternativas, escalas e pesos com responsáveis técnicos e partes interessadas; registrar autoria e repetir cenários. O sistema atual não representa esse parecer multidisciplinar.
