# Manual de uso — mapa, camadas e desenho

## Abrir

Prepare o ambiente e compile conforme o [README](../README.md). Na raiz, execute `.venv-geovale/bin/python executar.py` e abra http://127.0.0.1:8000. Internet necessária para fundos, contorno, temas e legendas.

## Navegar e localizar

O mapa abre em Minas Gerais. Arraste e use zoom, roda do mouse ou gestos para aproximar/afastar. O fundo permite navegar pelo mundo; o contorno verde representa MG. Alterne **Mapa** e **Satélite**. Pesquise Horizontes, Capitão do Mato, Vale ou Nova Lima e clique na única entrada ou no marcador. A seleção enquadra Nova Lima e a referência da mina, mostrando apenas o contorno desse município. Abra a seta do cartão para ver identificação e dados cadastrais da ANM; Recarregar ANM recupera uma consulta com falha. **Ver Minas Gerais** desfaz a seleção, retira o limite municipal e retorna ao estado, preservando as áreas de estudo.

## Sobrepor camadas

Na lateral, marque um ou mais temas: **Relevo e declividade**, **Água e drenagem**, **Solos e condição ambiental**, **Vegetação e conservação**, **Entorno e infraestrutura**. Esses cinco temas têm alcance em Minas Gerais. A sexta opção, **Trilhas de Nova Lima**, mostra cadastro da Prefeitura apenas na sua cobertura municipal. Não é necessário selecionar a mina antes.

Cada tema marcado carrega a representação oficial (imagens WMS ou linhas municipais). Use a **seta da camada** para expandir ou recolher **Intensidade** e **Legenda**. As opções começam recolhidas; fechar a seta mantém a camada e a intensidade escolhida. Reduza a intensidade quando cores encobrirem outra camada. Abra Legenda para consultar as cores/classes de cada base do tema. Desmarque para remover. A ordem das sobreposições é fixa; o último clique não altera essa ordem. Trocar fundo, escolher mina e voltar ao estado preservam as camadas ativas. Recarregar a página limpa as escolhas e a área desenhada. Nas trilhas, cada traçado usa sua cor da Prefeitura; a legenda mostra apenas os nomes presentes no enquadramento, na ordem da fonte. A lista é rolável e acompanha a navegação. Passe o cursor sobre a linha ou toque nela para consultar o nome cadastrado.

## Delimitar a área de estudo

Clique em **Desenhar área**. Clique ou toque no mapa para marcar pelo menos três pontos. **Desfazer ponto** remove o último; **Cancelar** abandona o rascunho. Use **Fechar contorno** ou o primeiro ponto para fechar. Arraste os vértices para ajustar; os marcadores intermediários permitem acrescentar pontos. Clique em **Confirmar área**. Caso a geometria seja inválida, ajuste o contorno e confirme novamente.

Após confirmar, **Adicionar área** começa outro polígono sem apagar os anteriores. A lista Áreas ou o clique em um contorno inativo seleciona qual será editado; amarelo indica a seleção e verde indica as demais. **Polígono ANM**, habilitado ao selecionar a mina, oferece uma prévia cadastral para confirmar como outra área independente. Editar e confirmar esse polígono o transforma em recorte manual.

Na área selecionada, **Ver área** enquadra o desenho; **Ajustar** permite editar, **Redesenhar** começa outro e **Remover** apaga apenas ela. Cancelar uma edição/redesenho restaura a última área confirmada. Escape cancela o desenho em andamento. Todas as áreas permanecem ao navegar e alternar camadas/fundo, mas se perde ao atualizar ou fechar a página. Não há salvamento permanente.

O contorno é a área escolhida para estudo, não o perímetro físico ou operacional da mina. [Limites do desenho](AREA_ESTUDO.md).

## Falhas e interpretação

Se o limite municipal falhar, use **Recarregar contorno**; isso não impede desenho ou consulta ANM. Se o contorno estadual falhar, use **Tentar novamente**. Se o fundo falhar, use **Recarregar**. Uma camada temática com falha oferece sua própria recarga; também pode ser desmarcada. A legenda tem recarga independente. Fora da cobertura de cada fonte, não há dados daquela opção. Trilhas não visíveis no enquadramento geram um aviso; isso não comprova inexistência de caminhos. Uma imagem transparente ou sem feições não certifica que a área esteja livre de riscos/restrições.

As sobreposições servem à exploração regional, sem determinar segurança ou uso futuro. A abrangência e idade das bases estão em [Dados geográficos](DADOS_GEOGRAFICOS.md). Encerrar o servidor descarta os caches do contorno e das trilhas; não há persistência da seleção nem banco de dados.

## Mostrar ou ocultar barras

Use as setas nas bordas do mapa para recolher **Áreas** à esquerda ou **Mina e camadas** à direita. Clique novamente para reabrir; o desenho em andamento, as áreas e as escolhas são preservados. Em telas estreitas, os dois atalhos ficam no topo; ferramentas aparecem antes do mapa e consulta depois.
