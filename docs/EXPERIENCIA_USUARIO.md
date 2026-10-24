# Interface pública

1. Abrir o site e enviar o GeoJSON do computador pelo seletor ou arrastando o arquivo para a caixa de envio.
2. Ver nome, área em hectares e poligonal sobre fotografia aérea, com zoom e enquadramento.
3. Clicar **Analisar área** para obter declividade mediana/P90 e cobertura predominante com ano.
4. Ajustar três prioridades somando 100%. **Comparar prioridades** abre o diálogo opcional de AHP.
5. Clicar **Comparar opções** para ver a ordenação, o índice relativo e o estado de sensibilidade.
6. **Salvar resultado** libera **Relatório simples** e **Relatório técnico** da mesma revisão.

**Trocar mapa** retorna à escolha do arquivo, sem apagar revisões já salvas. Mudar prioridades esconde o resultado desatualizado até uma nova comparação. A interface comunica processamento, erros e total de pesos inválido. A ausência de cobertura impede a análise, sem fabricar resultados.

Não há login, painéis técnicos, editor de regras, cadastro de cenários, tabelas de fontes ou histórico na tela principal. A marca é estática. As explicações detalhadas ficam no [Manual de uso](MANUAL_USO.md) e nos relatórios; a interface preserva títulos, dados, ações, estados e avisos breves.

## Composição vigente

Cabeçalho com marca GeoVale, verde-petróleo e amarelo. Título “Qual o melhor futuro para esta área?”, com sublinhado amarelo em “futuro”. As três etapas aparecem abaixo do título, em contraste claro sobre o painel verde. Caixa de envio centralizada na coluna direita, com largura máxima de 30rem, borda, sombra, tipografia legível e proporções ajustadas. O rodapé identifica Rafael Inácio Silva, MVP, 2026 e as fontes públicas.

O fundo utiliza pedra na cor original, derivada da referência fornecida, sem marca ou letras. O arquivo local `frontend/src/assets/textura-pedra.png` é servido pelo build. Uma única imagem cobre a viewport, sem repetição ou emenda horizontal; permanece fixa durante a rolagem. Cabeçalho, painel frontal, caixa de envio e demais superfícies mantêm fundos lisos. O gradiente claro é suave. A textura é decorativa e não participa da análise.

## Responsividade e interação

Estrutura flexível com altura mínima de viewport dinâmica e alternativa `100vh`; cabeçalho/rodapé têm altura natural. Margens revelam o fundo, e o painel ocupa a altura disponível. O título fica no alto; a caixa permanece centralizada na vertical em telas com duas colunas. Em telas pequenas, os blocos são empilhados e a página permite rolagem vertical. Os rótulos das etapas passam a três colunas com número acima do texto quando necessário.

Tipografia e espaçamentos usam limites fluidos. Consultas ao contêiner definem as colunas, com alternativa por media query. Campos e controles são rotulados; o diálogo de prioridades possui altura limitada e rolagem própria. O mapa reenquadra a poligonal ao redimensionar e libera observador/quadros de animação ao desmontar.

Abertura verificada por viewport do navegador em dez dimensões entre 320×640 e 1920×1080, sem overflow horizontal ou rótulos das etapas cortados. Isso não representa teste físico em todos os dispositivos. Detalhes em [Validação](VALIDACAO.md).
