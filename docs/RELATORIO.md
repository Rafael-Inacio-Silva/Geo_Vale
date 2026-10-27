# Relatório GeoVale e cenário técnico simulado

Versão 4.1.0, 27/10/2026. **Ver relatório** aparece ao selecionar a mina pelo cartão ou marcador, independentemente de Influência. Documento padronizado com marca e logo GeoVale, sem identidade visual ou autoria corporativa Vale.

## Documento gerado

O PDF tem capa e mapa, território/bases consultadas, relevo/solos, água, vegetação/conservação, entorno/trilhas, cenário simulado, síntese, referências e Anexo A. Todos os registros vetoriais aparecem no inventário com ID curto na base, nome e descritores disponíveis. O identificador curto é o trecho final do ID publicado; prefixo e atributos completos permanecem internos. Ausência de nome é explícita.

Rasters aparecem com todas as classes presentes, contagens, proporção de células válidas e NoData. Não se apresentam percentuais como área ou se despejam matrizes em texto. Tabelas, mapa e contagens são gerados a partir do catálogo persistido, sem números demonstrativos fixos nos blocos reais. O armazenamento mantém geometrias, todos os atributos e GeoTIFFs completos.

ReportLab gera o PDF com fontes Unicode incorporadas e marca vetorial. Mapas são desenhados das geometrias guardadas, projetadas para UTM 23S apenas na apresentação, com norte e escala; não baixam tiles, não usam imagem de satélite e não alteram o dado de análise. Fontes/creditos dos mapas são conservados. Marcadores PDF permitem navegar por seção no leitor externo.

## Cenário fictício autorizado

`dados/cenarios/horizontes.json` contém natureza simulado, mina, versão, horizonte pós-fechamento hipotético, premissas e referência metodológica. Todas as condições são fictícias para demonstrar entradas técnicas que as camadas não fornecem:

- Estabilidade física considerada atendida para iniciar revegetação, sem abranger visitação.
- Drenagem considerada implantada/operacional, sem medição de qualidade da água.
- Preparo de solo com adequações pendentes e revegetação prevista.
- Uma edificação candidata fictícia, com avaliação específica pendente.
- Segurança de visitantes, acesso autorizado e interesse comunitário não caracterizados.

Referência: Plano de Fechamento Minas-Rio, Anglo American, revisão junho/2021. Seções 8.2.1.3-8.2.1.5 (PDF 40-44/impressas 34-38), 11.11.3 (68-69/62-63), 11.11.7.6 (84/78). O plano prescreve ações e verificações; não é evidência de execução na Horizontes. Não foram transferidos custos, parâmetros geotécnicos ou resultados de outra mina. A síntese cruza contexto real e premissas como condições/pendências, sem pontuação ou recomendação de uso futuro. A análise multicritério permanece por definir.

## Fluxo técnico e atualização

`GET /api/minas/{id}/relatorio` entrega application/pdf inline; `?baixar=true` entrega attachment. Mina desconhecida: 404; dados incompletos/vencidos/incompatíveis ou cenário inválido/ausente: 503, com recuperação. Todos os temas entram, sem parâmetros de checkbox/zoom.

A geração lê SQLite e cenário local, sem chamadas externas. Cache por mina usa conteúdo dos dados, cenário e versão do modelo; mudanças invalidam o documento. O coletor mantém a assinatura do método 4.0.0 porque cálculos/recorte não mudaram. A API/interface é 4.1.0. Não há uma cópia fixa do PDF no repositório substituindo dados dinâmicos.

PDF.js e worker carregam apenas ao abrir o relatório. Renderizam uma página de cada vez em canvas, com texto acessível para leitores de tela e adaptação à largura. Anterior/Próxima, Baixar PDF e Fechar são os controles. Download utiliza o mesmo Blob aberto. Fechar/Escape devolve foco e libera recursos; falha permite nova tentativa. Um diálogo aberto permanece retratando sua coleta, mesmo se houver atualização posterior do banco.

[Dados territoriais](DADOS_TERRITORIAIS.md), [justificativas](ESCOLHAS_TERRITORIAIS.md), [verificação](VALIDACAO.md).
