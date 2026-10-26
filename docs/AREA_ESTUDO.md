# Áreas de estudo

Versão 3.3.0. O engenheiro pode demarcar **vários polígonos independentes** na mesma página: por exemplo, cava, morro e barragem. Cada área pode recortar somente uma parte do território; não é necessário demarcar a mina inteira. As áreas podem se sobrepor ou ficar separadas e não são unidas automaticamente. Não existe limite fixo de quantidade de áreas no produto; cada polígono tem de 3 a 500 vértices e o desempenho depende do navegador.

## Adicionar e selecionar

**Desenhar área → marcar pontos → Fechar contorno → ajustar → Confirmar área.** Desfazer ponto retira o último; o primeiro ponto também fecha o anel. Os marcadores intermediários acrescentam vértices na edição.

Depois da primeira confirmação, **Adicionar área** inicia outro desenho conservando os anteriores. A lista **Áreas** permite selecionar cada demarcação, inclusive por clique em um contorno inativo no mapa. A área selecionada tem borda amarela; as demais ficam verdes. A numeração é estável durante a sessão e não é reaproveitada após remover.

**Ver área**, **Ajustar**, **Redesenhar**, **Renomear** e **Remover** atuam somente sobre a área selecionada. Remover escolhe a última área restante; se não restar nenhuma, volta ao estado inicial. Cancelar adição retorna à área antes selecionada; cancelar edição/redesenho restaura sua geometria confirmada. As outras áreas permanecem inalteradas. Escape cancela o desenho ou a prévia ANM quando o foco está nos controles.

**Polígono ANM** é outra forma de adicionar, disponível após selecionar a mina. Exibe a prévia do processo associado e permite confirmar ou cancelar. A geometria importada pode ser ajustada; ao confirmar qualquer ajuste, torna-se recorte manual, sem manter o rótulo de origem oficial. [Fonte e limites ANM](ANM.md).

## Nome personalizado

Na área selecionada, **Renomear** abre um campo na lateral. Digite um nome (por exemplo, Barragem ou Cava principal) e use **Salvar nome** ou Enter. **Cancelar** ou Escape conserva o nome anterior. O foco retorna ao botão Renomear. Enquanto o campo está aberto, a seleção de outra área fica bloqueada para não aplicar o nome ao recorte errado.

O nome substitui o rótulo padrão na lista, na identificação da área selecionada e no tooltip do polígono, ativo ou inativo. É texto livre de 1 a 80 caracteres após retirar espaços nas extremidades e reduzir sequências de espaços a um. Nomes iguais são permitidos; os ids internos continuam distintos e estáveis. A numeração inicial permanece como padrão se não houver nome personalizado.

Renomear não altera a geometria, a fonte, o processo ou a finalidade; é uma identificação pessoal do recorte. O nome acompanha a área após ajuste ou redesenho e é removido quando ela é excluída. É mantido separadamente das propriedades cadastrais e não é enviado ao backend ou aos fornecedores. No mapa usa `textContent`, sem interpretar HTML. Assim como os polígonos, existe apenas na memória da página e se perde ao recarregar.

## Validação e memória

`POST /api/area/validar`, JSON até 128 KiB por confirmação manual. Entrada: Feature GeoJSON Polygon simples, um anel fechado sem buracos, coordenadas numéricas finitas em duas dimensões, longitude ±180° e latitude ±85°. Sem segmentos atravessando o antimeridiano; pelo menos três vértices distintos, superfície não nula e geometria válida no Shapely. Não recebe MultiPolygon: várias áreas são várias Features Polygon independentes, validadas individualmente.

A resposta 200 preserva a geometria e devolve propriedades controladas: `origem=desenho_manual`, `finalidade=area_de_estudo`, `vertices`. Retorna 422 para desenho/JSON inválido e 413 para tamanho excedente. Sem correção, simplificação ou deslocamento silencioso. Falha mantém a área editável. A confirmação ANM preserva a Feature já validada pela consulta do backend. Não calcula área/distância, interseções ou aptidão.

As áreas confirmadas existem somente na memória da página; **recarregar ou fechar descarta todas**. Não há salvamento em arquivo, banco ou sessão do servidor. Os desenhos são enviados apenas à API local para validação, sem transmissão aos provedores externos. Leaflet.draw fornece desenho/edição; controles React mantêm a identidade visual. Navegar, alternar fundo/camadas ou voltar para MG conserva todas as demarcações.

Uma área de estudo é uma escolha do usuário. Não certifica limite fundiário, ambiental, operacional ou pós-mineração. O limite municipal é contexto administrativo; o processo ANM é um cadastro minerário. Nenhum deles comprova segurança ou liberação de uso.
