# Requisitos do território preparado

| ID | Comportamento e aceitação |
|---|---|
| RF-01 | Abrir em Minas Gerais com navegação mundial, contorno oficial e uma Mina Horizontes. |
| RF-02 | Cartão seleciona/enquadra município; repetir desmarca e retorna a MG. Selecionar por cartão ou bolinha já mostra o contorno da mina; bolinha sempre aproxima em zoom 14, sem resposta municipal posterior desfazer. |
| RF-03 | Cartão com detalhes sob seta, identificação e atributos ANM sem geometria, fonte/data e recuperação. |
| RF-04 | Seleção mostra somente Nova Lima via IBGE; desfazer retira município/crédito. |
| RF-05 | Um único controle Influência na esquerda, habilitado sob seleção e contorno disponível; mostra contorno externo, mina OSM sombreada e todas as camadas somente dentro dele. |
| RF-06 | Influência utiliza exatamente o mesmo vetor do processamento; fonte, figura, data e aproximação conservadas no relatório/documentação. |
| RF-07 | Preparar todas as bases do catálogo para cada mina automaticamente na abertura do servidor, sem ação de extração na interface. |
| RF-08 | Guardar os resultados por mina/base em SQLite local; reiniciar não descarta dados válidos. |
| RF-09 | Considerar todos os temas e bases independentemente de checkboxes, intensidade, fundo, zoom ou barras ocultas. |
| RF-10 | Vetores conservam todos os atributos publicados, valores nulos e ID; geometrias são recortadas pela influência irregular, com contagem única por registro. |
| RF-11 | Descobrir esquema WFS e consultar todos os campos; trilhas usam outFields=*. Conferir completude, identidade, CRS e validade; rejeitar truncamento/excesso sem apresentar resultado parcial da base como completo. |
| RF-12 | Rasters via WCS mantêm grade nativa, resolução e todas as células selecionadas pelo centro, NoData separado, classes da legenda padrão oficial e GeoTIFF guardado. Sem leitura de cores WMS, amostra isolada ou reamostragem. Áreas de classe somam células medidas em UTM 23S. |
| RF-13 | Selecionar a mina oferece Ver relatório sem exigir Influência. PDF GeoVale com mapa geral e sete mapas temáticos, fatos separados entre área minerada (classe Mineração do MapBiomas) e entorno, UCs por grupo do SNUC, comentários com implicação por dado, ficha técnica simulada com pontos, asterisco e limites de referência, e fontes; prévia por imagens renderizadas no servidor e download do mesmo arquivo. Bases incompletas/vencidas impedem geração; dados completos permanecem internos. |
| RF-14 | Atualizar automaticamente após 24 h enquanto servidor ligado; conferir pendências a cada minuto e repetir falhas após cinco minutos. |
| RF-15 | Base nova integrada ao catálogo entra no processamento sem botão; mudança de recorte/evidência invalida resultados incompatíveis. |
| RF-16 | Distinguir pendente/processando/pronto/erro e dados anteriores. Fonte indisponível não vira zero; resposta vazia completa é identificada como tal. |
| RF-17 | Limites explícitos de bytes, registros, células e tempo; no máximo três bases em paralelo. Não baixar estado/mundo em lote. |
| RF-18 | Sete checkboxes inicialmente desmarcados ampliam o tema além da influência, com intensidade/legenda/recarga. Desmarcar restaura o recorte; sem Influência controlam a exibição normal. |
| RF-19 | Trilhas visuais preservam nomes/cores da Prefeitura e legenda do enquadramento; consulta de dados persistida é independente da visualização. |
| RF-20 | Preservar identidade visual, margens pequenas iguais, mapa amplo, barras ocultáveis e responsividade/teclado. |
| RF-22 | Cenário local identificado como simulado, sem atribuir autoria à Vale ou apresentar laudos/medições fictícios como reais. Pontos simulados ficam dentro do recorte; água usa a classe real do trecho e limites da CONAMA 357/2005. Documento sem ranking ou certificação técnica. |
| RF-21 | Desmarcar mina cancela leituras da página e remove influência/município; não apaga dados guardados por mina. |

## Interpretação e qualidade

O contorno externo AII águas/solos do projeto conjunto é **recorte comum de caracterização por simplificação do MVP**, não influência oficial de cada tema ou limite de recuperação. O sombreado OSM não certifica perímetro atual. Fase ANM não indica operação ativa. Topodata não retrata a cava atual; solos são pedologia; ambos são identificados como anteriores à mineração dentro da área minerada; trilhas não comprovam acesso/segurança. Ausência de dados não comprova ausência de riscos. Não há aptidão, ranking, ML, beneficiários, recomendação de uso ou relatório de diagnóstico. A fundamentação sustenta os temas e a caracterização; não valida decisão técnica para a mina.

API/interface na mesma origem, servidor local, dados gerados fora do Git, fontes e créditos identificados. Não há integração ou faturamento Google ativado. Registre somente verificações executadas.
