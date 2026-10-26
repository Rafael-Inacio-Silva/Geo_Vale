# Manual de uso — mapa, camadas e desenho

## Abrir

Prepare o ambiente e compile conforme o [README](../README.md). Na raiz, execute `.venv-geovale/bin/python executar.py` e abra http://127.0.0.1:8000. Internet necessária para fundos, contorno, temas e legendas.

## Navegar e localizar

O mapa abre em Minas Gerais. Arraste e use zoom, roda do mouse ou gestos para aproximar/afastar. O fundo permite navegar pelo mundo; o contorno verde representa MG. Alterne **Mapa** e **Satélite**. Pesquise Horizontes, Capitão do Mato, Vale ou Nova Lima e clique na única entrada ou no marcador. Clicar no cartão seleciona a mina e enquadra Nova Lima e a referência da mina, mostrando apenas o contorno desse município. Clicar novamente no cartão desmarca e volta para Minas Gerais. Clicar na bolinha aproxima a mina em zoom 14, inclusive se ela já estiver selecionada; o contorno municipal continua visível sem desfazer a aproximação. A bolinha também aceita Enter ou Espaço pelo teclado. Abra a seta do cartão para ver identificação e dados cadastrais da ANM; Recarregar ANM recupera uma consulta com falha. **Ver Minas Gerais** desfaz a seleção, retira o limite municipal e retorna ao estado, preservando as áreas de estudo.

## Sobrepor camadas

Na lateral, marque um ou mais temas: **Relevo e declividade**, **Água e drenagem**, **Solos**, **Vegetação e conservação**, **Entorno e infraestrutura**. Esses cinco temas têm alcance em Minas Gerais. A sexta opção, **Trilhas de Nova Lima**, mostra cadastro da Prefeitura apenas na sua cobertura municipal. Não é necessário selecionar a mina antes.

Cada tema marcado carrega a representação oficial (imagens WMS ou linhas municipais). Use a **seta da camada** para expandir ou recolher **Intensidade** e **Legenda**. As opções começam recolhidas; fechar a seta mantém a camada e a intensidade escolhida. Reduza a intensidade quando cores encobrirem outra camada. Abra Legenda para consultar as cores/classes de cada base do tema. Desmarque para remover. A ordem das sobreposições é fixa; o último clique não altera essa ordem. Trocar fundo, escolher mina e voltar ao estado preservam as camadas ativas. Recarregar a página limpa as escolhas e a área desenhada. Nas trilhas, cada traçado usa sua cor da Prefeitura; a legenda mostra apenas os nomes presentes no enquadramento, na ordem da fonte. A lista é rolável e acompanha a navegação. Passe o cursor sobre a linha ou toque nela para consultar o nome cadastrado.

## Alternar modos e delimitar

Na barra Áreas de estudo, escolha **Manual**, **Referência** ou **Influência**. O modo ativo fica verde. Referência e Influência só ficam disponíveis depois de selecionar a mina. Pode alternar livremente: isso não cria áreas duplicadas.

**Referência** mostra a área cinza de mineração do OpenStreetMap. **Usar como área** acrescenta esse contorno à sua coleção e abre Manual. Se ele já estiver na coleção sem alterações, o botão será **Selecionar esta área**, reutilizando-o. É uma referência colaborativa, sem certificação de limite atual.

**Influência** mostra quatro filtros: ADA unificada, AID água subterrânea, AID águas/solos e AII águas/solos. Marque/desmarque cada um; a mina permanece sombreada. Os filtros são conservados ao alternar. Fonte e significado explica as siglas e abre a evidência. Os recortes são do projeto Tamanduá/Horizontes, não fechamento.

**Manual** permite desenhar ou retomar o trabalho. Use Desenhar área/Adicionar área; marque pelo menos três pontos; Desfazer ponto remove o último e Cancelar abandona o rascunho. Feche pelo primeiro ponto ou Fechar contorno, ajuste os vértices e confirme. Se a geometria for inválida, ajuste e confirme novamente. É possível manter várias áreas independentes.

Se quiser consultar Referência ou Influência no meio do desenho, ajuste ou renomeação, clique no modo. O trabalho fica guardado; volte a Manual para retomar os mesmos pontos/texto e enquadramento. Clicar novamente no modo não reinicia o trabalho. O último contexto consultado continua visível em Manual como apoio; **Ocultar**, ao lado de Contexto, remove somente essa sobreposição. Ainda não há comparação automática.

Escolha uma área na lista ou mapa para Ver área, Ajustar, Redesenhar, Renomear ou Remover somente ela. Renomear aceita identificação pessoal; Salvar nome/Enter confirma, Cancelar/Escape conserva o anterior. Cancelar edição/redesenho restaura a confirmação anterior. A referência editada e confirmada torna-se recorte manual, sem mudar o arquivo de origem.

Navegar, alternar modos/fundos/camadas e ocultar barras preserva o trabalho. **Atualizar ou fechar a página descarta áreas, rascunhos e nomes.** Não há salvamento permanente. [Regras e limites](AREA_ESTUDO.md).

## Falhas e interpretação

Se o limite municipal falhar, use **Recarregar contorno**; isso não impede desenho ou consulta ANM. Se o contorno estadual falhar, use **Tentar novamente**. Se o fundo falhar, use **Recarregar**. Uma camada temática com falha oferece sua própria recarga; também pode ser desmarcada. A legenda tem recarga independente. Fora da cobertura de cada fonte, não há dados daquela opção. Trilhas não visíveis no enquadramento geram um aviso; isso não comprova inexistência de caminhos. Uma imagem transparente ou sem feições não certifica que a área esteja livre de riscos/restrições.

As sobreposições servem à exploração regional, sem determinar segurança ou uso futuro. A abrangência e idade das bases estão em [Dados geográficos](DADOS_GEOGRAFICOS.md). Encerrar o servidor descarta os caches do contorno e das trilhas; não há persistência da seleção nem banco de dados.

## Mostrar ou ocultar barras

Use as setas nas bordas do mapa para recolher **Áreas** à esquerda ou **Mina e camadas** à direita. Clique novamente para reabrir; o desenho em andamento, as áreas e as escolhas são preservados. Em telas estreitas, os dois atalhos ficam no topo; ferramentas aparecem antes do mapa e consulta depois.
