# Vídeo pós-mineração (IA generativa)

Versão 4.7.0, 28/10/2026. O botão **Ver pós-mineração**, abaixo de Sugerir uso, abre sobre o mapa um vídeo com dois sobrevoos iguais da Mina Horizontes: em cima o atual, embaixo a mesma câmera sobre a área minerada já recuperada. A legenda diz que é ilustração gerada previamente por IA, não projeto. Serve para a conversa com comunidade e partes interessadas, que entendem melhor uma imagem do que uma tabela de notas.

## Fluxo

1. Gravação do sobrevoo no Google Earth 3D (simulador de voo), 12,5 s.
2. Imagem "depois" de um quadro do sobrevoo, editada no ChatGPT: só a mina vira vegetação nativa.
3. `ferramentas/alinhar_referencia.py` acha o instante desse quadro, alinha a imagem ao vídeo e a projeta para instantes vizinhos.
4. `ferramentas/gerar_video_ia.py` envia o vídeo ao Luma Ray v3.2 (video-to-video, fal.ai) preso a esses quadros-chave.
5. Montagem (original em cima, gerado embaixo) feita pelo engenheiro; convertida para H.264 em `dados/videos/horizontes.mp4`.
6. `GET /api/minas/{id}/video` serve o arquivo, com leitura por trechos; o navegador toca dentro do diálogo.

## Decisões e porquês

| Decisão | Por quê | Evidência |
|---|---|---|
| Vídeo gerado previamente, não na hora | Gerar custa crédito e leva cerca de 15 min por vídeo; numa demonstração não cabe. No produto, o prompt sai da sugestão do setor e o vídeo é gerado sob demanda. | Custos e tempos das gerações deste trabalho. |
| Legenda dizendo que foi gerado antes | Uma barra de "gerando…" simulada derrubaria a credibilidade do resto, que se apoia em "cada escolha tem evidência". A legenda também identifica as ferramentas e o crédito das imagens. | Decisão do engenheiro, 28/10/2026. |
| Sobrevoo do avião, não o giro 360° | O giro e o avião foram gerados; o engenheiro escolheu o avião para comparar lado a lado. | Gerações de 28/10/2026. |
| Vídeo inteiro acelerado para 10 s | O modelo aceita 5 ou 10 s. A primeira tentativa mandou os últimos 5 s, em que a mina já saiu de cena; acelerar e desacelerar de volta mantém o voo inteiro e a sincronia com o original. | Quadros do sobrevoo: a mina aparece entre 0 e 8 s. |
| Recorte 16:9, sem faixas pretas | Faixas pretas fizeram os modelos de imagem reinventarem a cena; o recorte tira só as bordas de cima e de baixo, sem perder o HUD. | Teste de um quadro com FLUX Kontext. |
| Texto que edita, não reimagina | “Paisagem após o fechamento, com um pequeno lago” gerou outro lugar com um lago enorme. O texto final diz só o que muda (solo exposto da cava) e lista o que fica igual. | Primeiras gerações (360 e avião). |
| Imagem de referência editada fora e alinhada | Nano Banana e Kontext variavam entre quadros (às vezes inventando uma cava redonda). A imagem do ChatGPT, escolhida pelo engenheiro, foi alinhada ao quadro de 4,36 s por pontos do terreno (ORB + RANSAC, 832 pontos), com o HUD ignorado. | Sobreposição e diferença: fora da mina, idêntico ao original. |
| Âncoras projetadas e quadros originais do fim | A edição foi levada a 3,0 s e 5,6 s trocando só a área da mina; o HUD da imagem editada foi apagado antes, porque aparecia duplicado. O fim do voo, só céu e serra, usa quadros originais. | Quadros conferidos antes de pagar o vídeo. |
| Transformação mínima (adhere) | Com âncoras fiéis, o modelo só precisa propagar a mudança; liberdade maior mexia na câmera. | Edição média (flex) deslocou a câmera nas primeiras tentativas. |
| H.264 em `dados/videos` | A montagem veio em HEVC; H.264 toca em qualquer navegador. 4,5 MB, versionado com o projeto. | Teste no navegador: 9,2 s, 1072×1220. |

## Limites

- É ilustração: a vegetação, os terraços e as trilhas são inventados pela IA, não projeto de recuperação.
- Os números do HUD saem levemente borrados na metade gerada.
- Imagens de base do Google Earth (© Google); uso restrito a apresentação.
- Os scripts dependem de `fal-client`, `imageio-ffmpeg` e `opencv-python-headless` num ambiente separado; a chave `FAL_KEY` fica num `.env` local e nunca é impressa.
