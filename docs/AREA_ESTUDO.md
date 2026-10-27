# Áreas de estudo

Versão 3.5.0. Há três modos na barra esquerda: **Manual**, **Referência** e **Influência**. Os dois últimos exigem a Mina Horizontes selecionada. Os desenhos permanecem delimitações pessoais; a caracterização de água usa separadamente a AID documental fixa, sem avaliar esses desenhos.

## Três modos, sem cópias por navegação

**Manual**, **Referência** e **Influência** são modos de trabalho exclusivos, com o ativo destacado. Os modos de consulta exigem mina selecionada e pacote local disponível. Alternar não cria, confirma, remove ou duplica áreas. Clicar novamente em Referência/Influência reenquadra a mesma visualização, sem desligá-la. Movimentos rápidos interrompem a transição anterior para manter o enquadramento correto.

- **Referência** mostra o contorno de mineração OpenStreetMap, way 315221699, como contexto de consulta. **Usar como área** é a ação explícita para acrescentá-lo à coleção. Se já houver referência OSM intacta, aparece **Selecionar esta área**, que reutiliza a existente. O contorno não é certificado. [Fonte e precisão](REFERENCIAS_TERRITORIAIS.md).
- **Influência** apresenta quatro filtros do meio físico: ADA unificada, AID hidrogeologia, AID águas/solos e AII águas/solos. A referência OSM permanece sombreada mesmo com todos desligados. Os filtros são preservados ao visitar outro modo. São recortes do projeto Tamanduá/Horizontes, não fechamento, e não são áreas editáveis do usuário.
- **Manual** reúne desenho, edição, coleção e nomes. Desenhar área/Adicionar área começa um novo recorte. Se não existir área ou rascunho, clicar no modo Manual também inicia o desenho. Clicar de novo durante um trabalho não o reinicia.

Ao entrar em Manual depois de consultar um contexto, esse contexto permanece como apoio visual. A linha **Contexto: referência/influência · Ocultar** permite removê-lo sem apagar desenhos ou filtros. Contextos não capturam cliques de desenho.

## Pausar, retomar e confirmar

Alternar durante desenho/ajuste/renomeação **guarda o trabalho na memória da página**. Pontos e texto não são descartados; marcadores de edição são suspensos durante a consulta. Ao voltar a Manual, o desenho/ajuste e seu enquadramento são retomados. A consulta exibe um aviso curto de trabalho guardado. Não há diálogo obrigatório de confirmação para trocar de modo.

Usar como área fica indisponível enquanto há trabalho manual pendente, para não substituir o rascunho; os três modos continuam acessíveis. Termine ou cancele em Manual para usar a referência. Uma validação já enviada pode terminar durante a consulta. Falha conserva o ajuste para retomar, sem ativar marcadores fora de Manual.

Desenhar: marque de 3 a 500 pontos → Fechar contorno → ajustar → Confirmar área. Desfazer ponto retira o último; tocar o primeiro fecha o anel. Várias áreas são independentes, sem união automática ou limite fixo de quantidade; o desempenho depende do navegador.

A lista Áreas ou um clique em contorno inativo seleciona a demarcação e abre Manual. Amarelo indica seleção; verde indica as outras. Ver área, Ajustar, Redesenhar, Renomear e Remover afetam só a selecionada. A numeração não é reutilizada. Remover seleciona a última restante. Cancelar adição/edição restaura a confirmação anterior e preserva as outras. Escape cancela o desenho quando estiver em Manual.

Usar a referência intacta conserva `origem=referencia_osm`; ajustar/redesenhar e confirmar produz `origem=desenho_manual`. O snapshot de origem permanece inalterado. Ocultar barras preserva os estados. Desmarcar a mina remove o contexto, desabilita os modos documentais e retorna a Manual, preservando áreas e retomando eventual rascunho. Não há comparação por cálculo nesta etapa.

## Nome personalizado

Renomear abre um campo de 1–80 caracteres após normalizar espaços. Salvar/Enter atualiza lista, identificação e tooltip; Cancelar/Escape conserva o anterior e devolve foco. Durante a renomeação, outra área não pode ser selecionada. Nomes iguais são permitidos, separados por id estável. O nome pessoal não altera geometria/origem, acompanha ajustes e é descartado ao remover ou recarregar. Usa texto seguro, sem interpretar HTML, e não é enviado ao backend ou às fontes.

## Validação e memória

`POST /api/area/validar`, JSON até 128 KiB por confirmação manual: Feature Polygon simples, anel fechado sem buracos, 3–500 vértices distintos, superfície não nula, coordenadas numéricas finitas 2D, longitude ±180°, latitude ±85°, sem segmento atravessando o antimeridiano. Shapely rejeita autointerseção e degeneração sem corrigir, simplificar ou deslocar. Várias áreas são Features Polygon independentes, não um MultiPolygon manual.

Resposta 200 preserva a geometria e entrega somente origem manual, finalidade e número de vértices. Retorna 422 para entrada inválida e 413 acima do limite; falha mantém o desenho editável. A referência OSM intacta já vem conferida pelo leitor local e sua confirmação não chama fornecedores. O desenho é enviado somente à API local para validação.

Áreas e nomes existem na memória da página: fechar ou recarregar descarta todas. Não há salvamento, banco ou retomada. Navegar, alternar fundo/temas, ocultar barras ou voltar a MG preserva confirmações. Nenhuma área certifica limite fundiário, operacional, ambiental ou pós-mineração, segurança ou autorização de uso.

## Caracterização de água independente das áreas

Em Influência, Extrair dados de água funciona sem usar a referência ou desenhar. Recorta duas bases oficiais na AID águas/solos; marcar/desmarcar os quatro filtros não muda o cálculo. Resultado não altera a coleção de áreas nem define intervenção. Alternar modos conserva a consulta, ocultando o resultado no mapa fora de Influência; desmarcar a mina limpa-o. [Contrato e justificativa](EXTRACAO_AGUA.md).
