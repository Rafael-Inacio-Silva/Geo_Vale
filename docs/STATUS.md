# Estado atual — mapa, camadas e área de estudo

Atualizado em 26/10/2026. Versão **3.3.0**. Mapa mundial aberto em Minas Gerais, contorno estadual oficial e pesquisa exclusiva da Mina Horizontes. Fundos OpenStreetMap e Esri World Imagery, sem integração Google.

A lateral contém cinco temas estaduais da IDE-Sisema (dez bases) e **Trilhas de Nova Lima**, de fonte municipal independente. As seis opções iniciam desmarcadas e podem ser sobrepostas. Cada camada ativa tem uma seta para expandir intensidade e legenda, inicialmente recolhidas. Recolher mantém a camada e a intensidade; carregamento e falhas permanecem visíveis. Nas trilhas, cores e nomes são lidos da configuração oficial da Prefeitura; a legenda acompanha o enquadramento, sem repetir categorias de regiões não consultadas. A cobertura das trilhas é municipal, não estadual ou mundial. [Fontes e justificativa](TRILHAS_NOVA_LIMA.md).

**Desenhar área** e **Adicionar área** permitem manter várias áreas independentes, selecionar cada uma e removê-la sem afetar as demais. Cada desenho permite marcar pontos, desfazer o último, fechar o contorno, ajustar os vértices e confirmar. A API valida o polígono; não corrige automaticamente desenho inválido. A área confirmada pode ser enquadrada, ajustada, redesenhada ou removida. Cancelar restaura a última confirmação. O desenho fica na memória da página e se perde ao recarregar. Não é limite oficial da mina. [Contrato e operação](AREA_ESTUDO.md).

O painel ocupa a área disponível com margens externas pequenas e iguais, sem título visual acima; barras roláveis no desktop: áreas à esquerda e mina/camadas à direita, com setas independentes para ocultar/reabrir. Em telas estreitas, ferramentas antes do mapa e consulta depois. A etapa termina na exploração visual e delimitação, sem cruzamento espacial, diagnóstico, recomendação de uso, upload ou banco.

Contorno WFS com cache temporário em memória. WMS e fundos sob demanda; trilhas via consulta REST da região visível com cache de dez minutos, até 16 enquadramentos. Sem download estadual em lote. Internet necessária para as fontes. Ambiente Python 3.12 e Node 24; executar conforme o [manual](MANUAL_USO.md).

Verificações desta entrega em [Validação](VALIDACAO.md). Ferramentas e justificativas em [Ferramentas](FERRAMENTAS.md); fundamentação dos cinco temas em [Escolhas territoriais](ESCOLHAS_TERRITORIAIS.md). Entrega versionada no GitHub por solicitação do usuário; execução continua local, sem implantação pública. As escolhas e bases não foram validadas por especialista da Vale.

O cartão reúne os detalhes sob seta expansível. A seleção consulta [ANM](ANM.md) para processo, titular, fase e área cadastrada; Polígono ANM permite adicionar a geometria cadastral com prévia/confirmação. Editar e confirmar torna a área manual. A seleção acrescenta apenas o [limite de Nova Lima via IBGE](LIMITE_MUNICIPAL.md); voltar ao estado o remove. Cache ANM de dez minutos e municipal de uma hora, sob demanda, sem banco.

Cartão alterna seleção e retorno a MG; marcador aproxima a mina em zoom 14, sem a chegada do limite municipal desfazer essa ação. Visualização 3D adiada pelo usuário como acabamento da apresentação. Pesquisa Google registrada em [Consulta 3D](CONSULTA_3D_GOOGLE.md); nenhuma API Google foi ativada ou integrada.
