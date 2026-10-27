# Validação das fichas e prévia

Versão 4.2.0, 27/10/2026, macOS/Python 3.12/Node 24, aplicação local em 127.0.0.1:8024.

## Automatização

90 testes Python aprovados no conjunto completo; os testes territoriais/fichas passaram após os ajustes de diagramação e medidas. Dois testes Node, TypeScript/build e pip check aprovados. Lock macOS instalado com hashes; lock Linux atualizado, sem execução Linux. Avisos de depreciação Starlette/HTTPX e Rasterio/NumPy permanecem sem falhas.

As regressões conferem recorte/persistência, todos os atributos, grade/NoData, relatórios sem reextração, cenário inválido e cache. Os testes novos verificam comprimentos métricos, área sem duplicar polígonos sobrepostos, separação fatos/comentários, ausência de rede sem IA configurada, contrato simulado de LLM e recusa de números inventados. A prévia é testada como PNG real, com manifesto acessível e hash vinculado ao PDF; inclui versões antigas ainda guardadas, versão ausente (409) e página inexistente (404).

## Dados e documento reais

As onze bases persistidas da Horizontes continuam com: 68 trechos hidrográficos, 16 massas de água, 3 solos, 3 UCs estaduais/1 federal/1 municipal, 34 áreas urbanizadas, 4 rodovias e 34 trilhas; declividade com 171.428 células válidas/seis classes e cobertura com 182.154/dez classes. Não são constantes inseridas no relatório.

Medidas cartográficas conferidas no documento: 38,10 km de trechos hidrográficos, 213,48 ha de massas de água, 14,10 km de trechos rodoviários, 139,08 km de registros de trilhas e 1.438,02 ha urbanizados, calculados em UTM 23S. Comprimentos somam registros; áreas usam união por base. Essas medidas não são volume, vazão, qualidade ou levantamento de campo.

A emissão conferida pela API possui oito páginas, oito marcadores e 481.287 bytes. Todas as páginas foram renderizadas e inspecionadas: primeira página com todos os temas, seis mapas individuais e última ficha sem mapa com oito valores fictícios identificados. Sem anexo extenso ou classificação de usos. Cabeçalhos, tabelas, fontes e numeração legíveis.

A API retornou PDF inline/attachment com mesmos bytes e hash. O download por Baixar PDF no navegador foi comparado byte a byte com a cópia conferida e coincidiu. O manifesto contém texto de todas as páginas. As oito rotas de imagem retornaram PNGs válidos com mais de 900 x 1300 pixels. A prévia vem do próprio PDF; não é outro relatório HTML divergente.

## Navegador

Ver relatório permanece disponível sem ativar Influência. A versão compilada foi verificada com canvas bloqueado e APIs JavaScript recentes removidas antes da inicialização. As oito páginas renderizaram, pois a prévia usa imagens do servidor. Uma falha de imagem foi provocada apontando temporariamente a primeira página para uma página inexistente: erro não deixou imagem antiga visível. Tentar novamente recarregou o documento e recuperou a página. O arquivo temporário foi removido do build.

O controle nativo do Safari não foi usado nesta conferência; o teste demonstra independência de canvas/PDF.js, sem afirmar uma execução automatizada nesse navegador. O texto acessível acompanha a imagem. Os seletores visuais não filtram dados do relatório.

## IA e alcance

A integração OpenAI Responses / GPT-5 nano está preparada, com chave exclusivamente no arquivo local ignorado pelo Git. O arquivo permanece vazio, sem chamada real à OpenAI. O contrato foi testado com respostas controladas, incluindo JSON Schema, ausência de temperature, saída completada e recusa de números inventados; o documento atual identifica comentários por regras. Não houve ML treinado, chamada paga, validação de especialista, ensaio real de pH/estabilidade ou decisão de pós-mineração. Os oito números técnicos são fictícios, com asterisco e nota. As fontes reais e o recorte comum mantêm suas datas, escalas e limitações. [Método](RELATORIO.md), [dados](DADOS_TERRITORIAIS.md), [recorte](INFLUENCIA.md).
