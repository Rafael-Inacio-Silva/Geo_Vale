# Manual de uso

Prepare ambiente/build conforme o [README](../README.md). Execute `.venv-geovale/bin/python executar.py` e abra http://127.0.0.1:8000. O mapa abre em Minas Gerais e permite navegação mundial.

1. Pesquise e selecione **Mina Horizontes**. Selecionar pelo cartão ou pela bolinha mostra automaticamente o contorno da mina. A seleção também demarca Nova Lima e habilita **Influência** na esquerda. A seta do cartão abre os detalhes; clicar novamente no cartão desmarca e retorna a MG. A bolinha aproxima a mina.
2. Clique em **Influência**. Aparecem o contorno, a mina sombreada e todas as camadas dentro dessa extensão. Clicar novamente retira o contorno maior e as camadas recortadas; o contorno da mina continua enquanto ela estiver selecionada.
3. Marque uma camada na direita para ampliá-la além da influência. Desmarcar volta a mostrá-la somente dentro do contorno, quando Influência estiver ativa. Sem Influência, os checkboxes mostram/retiram camadas pelo enquadramento normal.
4. A seta de cada camada abre intensidade e legenda da versão ampliada. Mapa/Satélite troca o fundo. As setas das barras ocultam e reabrem sem perder estado.
5. Após selecionar a mina, **Ver relatório** abre o PDF, mesmo com Influência desligada. Use Anterior/Próxima para navegar e **Baixar PDF** para salvar o documento visualizado. Fechar ou Escape retorna ao mapa preservando a seleção. Durante o preparo automático o botão indica Preparando relatório; falhas permitem tentar novamente.

O relatório tem identidade GeoVale, mapa geral da influência, sete mapas temáticos, dados objetivos separados entre área minerada e entorno e comentários separados, com fontes/datas por ficha. A última ficha reúne dados técnicos simulados, com pontos no mapa e valores fictícios marcados por asterisco. A leitura contextual indica implicações para o planejamento, sem alterar os dados nem calcular aptidão ou recomendação. Os atributos e valores completos permanecem no armazenamento interno; o documento evita coordenadas e matrizes extensas.

Internet é necessária para imagens e atualizações externas. Uma falha visual permite Recarregar sem apagar os dados guardados. Desmarcar a mina retira município/influência; não apaga o banco. [Método e atualização](DADOS_TERRITORIAIS.md), [recorte](INFLUENCIA.md).
