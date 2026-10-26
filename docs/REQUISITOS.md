# Requisitos — mapa, camadas e área de estudo

| ID | Comportamento e aceitação |
|---|---|
| RF-01 | Abrir com mapa já centralizado em Minas Gerais. |
| RF-02 | Permitir navegação mundial sem limitar o arraste ao estado. |
| RF-03 | Consultar o limite oficial estadual no WFS da IDE-Sisema e desenhar o contorno. |
| RF-04 | Oferecer somente Mina Horizontes; reconhecer Capitão do Mato como nome anterior da mesma entrada. |
| RF-05 | Cartão seleciona e enquadra município/referência; novo clique no mesmo cartão desmarca e retorna a MG. Marcador sempre seleciona/aproxima a mina em zoom 14, sem reenquadramento municipal posterior; aceita teclado. Detalhes dentro do cartão expansível. |
| RF-06 | Alternar Mapa/Satélite com créditos visíveis. |
| RF-07 | Zoom e “Ver Minas Gerais”; retornar ao estado desfaz a seleção da mina. |
| RF-08 | Informar carregamento e falhas, com recuperação, sem inventar geometria. |
| RF-09 | Preservar fundo e pesquisa se o contorno falhar; avisar quando reaproveitar cache vencido. |
| RF-10 | Exibir seis controles independentes inicialmente desmarcados: cinco temas estaduais e Trilhas de Nova Lima, conforme catálogo fixo. |
| RF-11 | Marcar adiciona a sobreposição real WMS ou GeoJSON municipal; desmarcar remove. Combinar temas com ordem fixa e sem perder a navegação. |
| RF-12 | Expandir/recolher pela seta as opções de cada tema ativo, inicialmente fechadas; ajustar intensidade e consultar legendas sem desligar a camada ao recolher. Manter carregamento/falhas visíveis. |
| RF-13 | Carregar WMS e trilhas somente ao ativar e na região/zoom visíveis. Falha de uma camada não interrompe as demais; permitir recarregar. |
| RF-14 | Manter temas ativos ao mudar fundo, selecionar mina ou retornar ao estado. Fora da cobertura, informar o alcance específico: Minas Gerais ou Nova Lima. |
| RF-15 | Remover o título visual acima do painel e ocupar o espaço disponível com margens pequenas e iguais; preservar responsividade e mapa utilizável. |
| RF-16 | Desenhar um polígono simples com 3 a 500 vértices, desfazer o último ponto e fechar o contorno. |
| RF-17 | Permitir ajustar vértices antes da confirmação e validar no backend; rejeitar interseções e coordenadas inválidas sem correção silenciosa. |
| RF-18 | Enquadrar, ajustar, redesenhar e remover a área confirmada; cancelar restaura a última confirmação. |
| RF-19 | Conservar a área ao navegar ou alternar fundo/camadas; recarregar a página descarta o desenho. Sem persistência. |
| RF-20 | Consultar trilhas da fonte municipal fixa com recorte visível, crédito e nome por interação; falha recuperável sem interromper outras fontes. |
| RF-21 | Associar cada trilha ao nome e cor publicados no item oficial; legenda com categorias do enquadramento, sem duplicatas e na ordem da fonte. Ao navegar, atualizar; ao falhar ou sair da cobertura, não conservar legenda de outra região. |

| RF-22 | Revelar os detalhes pela seta do cartão, com teclado e estado expandido; consultar titular, fase, processo e área cadastrada na ANM, com recarga na falha. |
| RF-23 | Polígono ANM na barra esquerda junto às ferramentas de desenho, desabilitado até selecionar a mina; prévia, confirmação e cancelamento sem substituir outras áreas. |
| RF-24 | Preservar origem cadastral ao confirmar a geometria ANM intacta; confirmar sua edição produz origem manual sem identificação oficial. |
| RF-25 | Selecionar a mina acrescenta apenas o município associado, via IBGE; retornar para MG retira o limite e seu crédito. Requisição tardia não desfaz desenho ou navegação. |
| RF-26 | Adicionar várias áreas independentes; escolher uma pela lista ou contorno e editar, redesenhar, enquadrar ou remover só ela. Cancelar conserva as confirmações e demais áreas. |
| RF-27 | Validar cada polígono individualmente e descartar todas as áreas ao recarregar. Sem unir automaticamente áreas separadas ou sobrepostas. |

## Regras de interpretação

Os cinco temas são adaptação para MVP, apoiada em referências, sem validação de especialista da Vale. Não equivalem a cinco critérios obrigatórios ou diagnóstico completo. Marcador aproximado e contorno estadual simplificado são apenas localização/navegação. Cada área manual é um recorte de estudo escolhido pelo usuário. O polígono ANM é cadastral, não perímetro físico ou operacional. Fase cadastral não informa operação ativa/encerrada. O limite IBGE é contexto municipal simplificado, sem certificação cadastral. Trilhas são cadastro municipal; não comprovam segurança ou permissão de acesso. Mapa de solos não comprova condição ambiental; Topodata não representa a cava atual. Há validação geométrica do desenho, mas não cruzamento espacial, pesos, ranking, ML ou relatório nesta etapa. Justificativas e limites em [Escolhas territoriais](ESCOLHAS_TERRITORIAIS.md).

## Qualidade

Interface limpa em português, operável por teclado, com foco e rótulos; identidade verde/amarelo e textura apenas no fundo. Sem controles decorativos ou detalhes de integração na jornada. Créditos cartográficos visíveis. API e frontend na mesma origem, execução local. WMS direto no navegador usa HTTPS; WFS tem timeout e limite de tamanho. Não há download em lote. Ausência de dados visíveis não significa ausência de risco ou restrição.
