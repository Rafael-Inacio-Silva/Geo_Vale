# Manual de uso

Prepare ambiente/build conforme o [README](../README.md). Execute `.venv-geovale/bin/python executar.py` e abra http://127.0.0.1:8000. O mapa abre em Minas Gerais e permite navegação mundial.

1. Pesquise e selecione **Mina Horizontes**. Selecionar pelo cartão ou pela bolinha mostra automaticamente o contorno da mina. A seleção também demarca Nova Lima e habilita **Influência** na esquerda. A seta do cartão abre os detalhes; clicar novamente no cartão desmarca e retorna a MG. A bolinha aproxima a mina.
2. Clique em **Influência**. Aparecem o contorno, a mina sombreada e todas as camadas dentro dessa extensão. Clicar novamente retira o contorno maior e as camadas recortadas; o contorno da mina continua enquanto ela estiver selecionada.
3. Marque uma camada na direita para ampliá-la além da influência. Desmarcar volta a mostrá-la somente dentro do contorno, quando Influência estiver ativa. Sem Influência, os checkboxes mostram/retiram camadas pelo enquadramento normal.
4. A seta de cada camada abre intensidade e legenda da versão ampliada. Mapa/Satélite troca o fundo. As setas das barras ocultam e reabrem sem perder estado.
5. Com Influência ativa, **Exportar JSON** baixa o relatório completo da mina para análise externa. Inclui todas as bases, independentemente dos checkboxes. Durante a preparação automática o botão indica Preparando relatório. Falha de download permite tentar novamente.

O relatório contém atributos/IDs/geometrias vetoriais, matrizes nativas de relevo/cobertura, classes, metadados, datas e evidência do contorno. Não é diagnóstico técnico nem plano de fechamento. O servidor prepara os dados automaticamente e conserva resultados válidos entre reinícios. Fontes/datas e justificativas estão no arquivo e na documentação; a tela mantém apenas controles, estados necessários e créditos cartográficos.

Internet é necessária para imagens e atualizações externas. Uma falha visual permite Recarregar sem apagar os dados guardados. Desmarcar a mina retira município/influência; não apaga o banco. [Método e atualização](DADOS_TERRITORIAIS.md), [recorte](INFLUENCIA.md).
