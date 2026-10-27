# Validação da etapa territorial e extração de água

Revisão de 26/10/2026, versão **3.5.0**, em macOS, Python 3.12 e Node 24. Servidor em `127.0.0.1:8000`, sem implantação pública.

## Verificações automatizadas executadas

- **92 testes Python aprovados**: mapa, desenho manual, trilhas, atributos ANM, município, referências locais e água. A suíte permanece sem importador de geometria ANM.
- **2 testes Node aprovados**: pesquisa do catálogo único e ausência de resultados inventados.
- **TypeScript e build Vite aprovados**.

Os 13 testes/casos novos de água cobrem interseção no polígono irregular (excluindo registros presentes apenas no bbox), contatos sem a dimensão esperada, linhas multipartes contadas uma vez, geometria cortada e IDs preservados, nome ausente sem preenchimento inventado, resultado vazio completo, truncamento/excesso, CRS inesperado, ID incompatível/duplicado, geometria nula/inválida, campo ausente, cache defensivo/expiração/falha/recuperação/invalidação pela evidência, parâmetros WFS fixos/timeout/bytes e API 404/503/recuperação. Desenhos e filtros não entram no contrato da extração.

Permanece um aviso de depreciação Starlette/TestClient sobre HTTPX, sem falha da suíte. Não houve mudança de dependências por esse aviso.

## Fonte oficial e fluxo real

As duas consultas WFS reais da IDE-Sisema retornaram HTTP 200 e GeoJSON EPSG:4326 com contagem completa. O envelope da AID águas/solos recebeu 72 trechos e 18 massas; a interseção com o polígono aproximado resultou em **42 trechos e 10 massas d’água**. Todos os registros recebidos nessa verificação tinham geometrias válidas. O extrator com os campos selecionados produziu os mesmos totais.

Trechos encontrados publicam BHO 2017, versão de 22/06/2018, revisão GEIRH de 07/11/2022; massas encontradas publicam FBDS (2017) e `bho_massa_dagua_2019`. Não são datas atuais de levantamento nem medições de qualidade. Nomes originais e registros sem nome foram conservados.

Fluxo conferido: botão no navegador → API local → duas bases WFS → interseção Shapely → resumo/52 geometrias no navegador. A API foi acionada pela interface, sem resultado de demonstração ou arquivo de água pré-preenchido.

## Navegação e apresentação verificadas

- Abertura sem mina selecionada mantém os modos documentais desabilitados. Selecionar Horizontes habilita Influência; a extração funciona sem desenhar ou usar a referência.
- Clique mostrou Extraindo e depois **42 trechos hidrográficos / 10 massas d’água**, data da consulta, opção do mapa e fontes.
- Registros e fontes abriu nomes, IDs, versões, figura/página do parecer e limitações; exemplo de nome ausente apareceu Sem nome publicado.
- Checkbox do resultado reduziu os paths da pane de água de 52 para 0; religar restaurou os 52. O resumo permaneceu.
- Referência ocultou o resultado cartográfico; voltar a Influência restaurou 52 paths e a mesma data sem nova extração.
- Desmarcar o filtro visual Águas e solos · AID não mudou as contagens nem as 52 geometrias extraídas. O filtro foi restaurado após conferir.
- Ocultar/reabrir a barra preservou a água recortada no mapa, consulta e resumo.
- Desmarcar a mina retornou à visão estadual e removeu os paths, crédito de água e resumo. Os modos documentais ficaram desabilitados.
- Desktop 1440 × 900 e celular 390 × 844 conferidos. Largura de conteúdo igual ao viewport, sem rolagem horizontal; o resumo de duas colunas permaneceu legível no celular.

## Alcance da verificação

Nesta revisão não foram repetidos os testes manuais completos de desenho/renomeação nem a conferência individual das dez imagens WMS e suas legendas. Seus contratos automatizados continuam aprovados. Falhas/truncamentos/recuperação da nova extração foram simulados nos testes; não se provocou indisponibilidade física do fornecedor no navegador.

O resultado é caracterização preliminar na **AID águas/solos do projeto conjunto Tamanduá/Horizontes**, digitalizada aproximadamente da figura. Não há análise de polígonos pessoais, distância, área, qualidade da água, impacto, aptidão, ranking, beneficiários ou persistência. A interseção computacional não torna preciso o contorno de entrada nem transforma influência em intervenção ou limite de fechamento.

[Justificativa e fontes para apresentação](EXTRACAO_AGUA.md).
