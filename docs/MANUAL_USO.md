# Manual de uso — GeoVale

## Abrir uma área

Na tela inicial, escolha **Enviar GeoJSON** ou arraste o arquivo para a caixa de envio. O arquivo deve conter uma única feição Polygon ou MultiPolygon em WGS84, ter extensão .geojson e até 1 MiB. Partes e recortes internos são preservados. Um contorno válido não comprova segurança ou autorização de uso.

Os arquivos de Rapatee (aproximadamente 162,29 hectares) e Burning Star 3 (aproximadamente 530,55 hectares), áreas reais de Illinois, EUA, estão em `~/Desktop/Mapas GeoVale/`. A cobertura completa desta versão está limitada às duas geometrias preparadas; um contorno diferente pode ser exibido, mas a análise fica indisponível.

A marca no cabeçalho é apenas identificação visual. **Trocar mapa** retorna à escolha da área. Isso abandona o rascunho exibido, sem apagar revisões já salvas.

## Ver e analisar

O mapa mostra o contorno e a extensão em hectares. Use zoom, **Enquadrar área** e a opção **Imagem aérea** conforme necessário. A fotografia pública é histórica e serve de contexto; não é imagem atual em tempo real, nem comprova o estado atual de recuperação.

Clique **Analisar área** para obter declividade mediana, declividade P90 e cobertura predominante com seu ano. P90 indica o valor abaixo do qual estão 90% das amostras válidas de declividade. O relevo e a cobertura vêm dos dados públicos preparados; a fotografia não é usada para classificar a área. Uma fonte ausente ou corrompida impede o cálculo.

## Definir prioridades

Os três pesos representam a importância dada à cobertura atual, à continuidade com o entorno e à condição relativa do relevo. Edite os valores até o total ser 100%. Os valores iniciais representam importância igual, com arredondamento de duas casas; não são pesos aprovados por especialistas da Vale.

Opcionalmente, use **Comparar prioridades**. Compare os três pares de critérios e clique **Aplicar prioridades**. O sistema usa AHP para calcular os pesos e verificar consistência matemática. Se os julgamentos forem inconsistentes, revise as escolhas. A consistência não comprova validade técnica; numa aplicação real, os critérios e pesos dependem dos responsáveis técnicos e envolvidos.

## Comparar usos

Clique **Comparar opções**. As alternativas implementadas são Agricultura, Uso florestal e Recreação em áreas abertas. Energia solar não é calculada nesta versão.

O índice relativo do TOPSIS ordena possibilidades para aprofundar estudos; não é probabilidade de sucesso, porcentagem de aptidão ou garantia de viabilidade. Os índices dependem das opções, dos pesos e das regras exploratórias. Não compare índices de minas diferentes como uma escala absoluta. A associação entre classes de cobertura, as transformações de relevo e o anel de entorno são hipóteses ainda não calibradas por especialistas.

O aviso de sensibilidade informa se a primeira posição mudou nos ajustes de pesos testados, sem representar todas as incertezas possíveis. Depois de alterar os pesos, compare novamente para atualizar o resultado. O sistema não permite exportar uma comparação desatualizada.

Custos, segurança geotécnica, contaminação, solo, clima, permissões e demanda social não são avaliados automaticamente. O resultado orienta estudos e não autoriza uso. As descrições e pendências de cada alternativa constam dos relatórios; uso florestal não equivale a restauração nativa aprovada e recreação em áreas abertas não avalia esportes aquáticos ou acesso público.

## Salvar e obter relatórios

Clique **Salvar resultado**. Depois, escolha **Relatório simples** ou **Relatório técnico**. Ambos correspondem à mesma revisão salva. O simples resume a área, as prioridades e o resultado; o técnico reúne dados, hipóteses, fontes e memória de cálculo. Os arquivos HTML baixados podem ser abertos sem conexão.

Rascunhos dependem da sessão local e podem expirar. Reiniciar o servidor ou recarregar a página pode retirar o rascunho da tela. As revisões salvas permanecem no banco; os links de download exigem a mesma sessão. Esta versão não possui uma tela de recuperação de histórico.

Para executar o programa, consulte o [README](../README.md). Para compreender os cálculos e as limitações científicas, consulte a [Metodologia](METODOLOGIA.md).
