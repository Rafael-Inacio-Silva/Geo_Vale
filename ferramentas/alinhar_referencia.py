"""Transforma uma imagem "depois" (editada fora, por exemplo no ChatGPT) em quadros-chave alinhados ao vídeo do sobrevoo.

A imagem editada vem de um print da tela, com escala e recorte diferentes do vídeo. Sem alinhamento exato, o modelo de
vídeo puxa a cena para a imagem e a câmera entorta. Por isso:
1. Acha o instante do vídeo que corresponde à imagem e a transformação entre os dois, casando pontos do terreno (ORB +
   RANSAC) e ignorando o HUD, que é fixo na tela.
2. Leva a imagem para o recorte 16:9 do vídeo; bordas que ela não cobre recebem o quadro original.
3. Projeta a área que a edição mudou (a mina) para instantes vizinhos e troca só essa área; o resto do quadro, e o HUD,
   continuam originais. O HUD da imagem editada é apagado antes, senão aparece duplicado.
4. Grava quadros.json no formato de gerar_video_ia.py, com os quadros originais do fim (só céu e serra).

Depende de `opencv-python-headless`, no mesmo ambiente separado de gerar_video_ia.py.

Uso: python alinhar_referencia.py --imagem depois.png --saida pasta [--vizinhos 3.0 5.6]
"""
import argparse
import json
from pathlib import Path

import cv2
import numpy as np

from gerar_video_ia import DURACAO, ORIGEM, QUADROS_SEM_MINA, medir

LARGURA, ALTURA_TOTAL, TOPO, ALTURA = 1280, 990, 100, 720  # mesmo recorte de gerar_video_ia.RECORTE


def ler_quadros():
    """Todos os quadros, lidos em sequência: o seek do HEVC cai no quadro-chave mais próximo e erra o instante."""
    video = cv2.VideoCapture(str(ORIGEM))
    quadros = []
    while True:
        ok, quadro = video.read()
        if not ok:
            return quadros, video.get(cv2.CAP_PROP_FPS)
        quadros.append(cv2.resize(quadro, (LARGURA, ALTURA_TOTAL)))


def hud(imagem):
    """Linhas e números verdes do simulador: verde claro, bem acima do vermelho e do azul."""
    b, g, r = (imagem[..., i].astype(int) for i in range(3))
    return cv2.dilate(((g > 150) & (g > r + 50) & (g > b + 20)).astype(np.uint8), np.ones((7, 7), np.uint8)) > 0


def casar(orb, a, b):
    """Transformação de a para b pelos pontos do terreno; devolve a matriz e quantos pontos concordam."""
    ka, da = orb.detectAndCompute(cv2.cvtColor(a, cv2.COLOR_BGR2GRAY), np.where(hud(a), 0, 255).astype(np.uint8))
    kb, db = orb.detectAndCompute(cv2.cvtColor(b, cv2.COLOR_BGR2GRAY), np.where(hud(b), 0, 255).astype(np.uint8))
    pares = [m for m, n in cv2.BFMatcher(cv2.NORM_HAMMING).knnMatch(da, db, k=2) if m.distance < .75 * n.distance]
    if len(pares) < 20:
        return None, 0
    H, ok = cv2.findHomography(np.float32([ka[m.queryIdx].pt for m in pares]), np.float32([kb[m.trainIdx].pt for m in pares]), cv2.RANSAC, 3)
    return H, int(ok.sum()) if ok is not None else 0


def main(imagem, saida, vizinhos):
    pasta = Path(saida)
    pasta.mkdir(parents=True, exist_ok=True)
    editada = cv2.imread(str(imagem))
    quadros, fps = ler_quadros()
    orb = cv2.ORB_create(6000)

    # 1. Instante e transformação: o quadro com mais pontos de terreno em comum.
    melhor = max(((i, *casar(orb, editada, q)) for i, q in enumerate(quadros) if i % 3 == 0), key=lambda x: x[2])
    indice, H, pontos = melhor
    print(f'imagem corresponde a {indice / fps:.2f} s ({pontos} pontos de terreno)')

    # 2. Imagem no recorte 16:9 do vídeo.
    para_recorte = np.array([[1, 0, 0], [0, 1, -TOPO], [0, 0, 1]]) @ H
    original = quadros[indice][TOPO:TOPO + ALTURA]
    alinhada = cv2.warpPerspective(editada, para_recorte, (LARGURA, ALTURA), flags=cv2.INTER_CUBIC)
    cobre = cv2.warpPerspective(np.full(editada.shape[:2], 255, np.uint8), para_recorte, (LARGURA, ALTURA))
    alinhada = np.where(cobre[..., None] > 250, alinhada, original)

    # 3. Área mudada (diferença forte, suavizada, sem HUD) e projeção para os vizinhos.
    diferenca = cv2.cvtColor(cv2.absdiff(original, alinhada), cv2.COLOR_BGR2GRAY)
    area = cv2.morphologyEx((cv2.GaussianBlur(diferenca, (0, 0), 6) > 28).astype(np.uint8) * 255, cv2.MORPH_CLOSE, np.ones((41, 41), np.uint8))
    area[hud(original)] = 0
    area = cv2.GaussianBlur(area, (0, 0), 8).astype(np.float32) / 255
    sem_hud = cv2.inpaint(alinhada, cv2.dilate(hud(alinhada).astype(np.uint8) * 255, np.ones((5, 5), np.uint8)), 5, cv2.INPAINT_TELEA)

    total, _, _ = medir(ORIGEM)
    fator = total / DURACAO

    def posicao(t):
        return round(min(t / fator, DURACAO - 1 / 30) * 30)

    chaves = [(posicao(indice / fps), pasta / 'quadro_referencia.png')]
    cv2.imwrite(str(chaves[0][1]), alinhada)
    for t in vizinhos:
        alvo = quadros[round(t * fps)][TOPO:TOPO + ALTURA]
        Hv, pontos = casar(orb, original, alvo)
        mistura = cv2.warpPerspective(area, Hv, (LARGURA, ALTURA))
        mistura[cv2.dilate(hud(alvo).astype(np.uint8), np.ones((5, 5), np.uint8)) > 0] = 0
        quadro = (alvo * (1 - mistura[..., None]) + cv2.warpPerspective(sem_hud, Hv, (LARGURA, ALTURA)) * mistura[..., None]).astype(np.uint8)
        arquivo = pasta / f'quadro_referencia_{t}.png'
        cv2.imwrite(str(arquivo), quadro)
        chaves.append((posicao(t), arquivo))
        print(f'{t} s projetado ({pontos} pontos)')

    # 4. Fim do voo sem mina: quadros originais, para céu e HUD não mudarem.
    for t in QUADROS_SEM_MINA:
        arquivo = pasta / f'quadro_{t}.png'
        cv2.imwrite(str(arquivo), quadros[min(round(t * fps), len(quadros) - 1)][TOPO:TOPO + ALTURA])
        chaves.append((posicao(t), arquivo))
    (pasta / 'quadros.json').write_text(json.dumps([[i, str(a)] for i, a in sorted(chaves)]))
    print('quadros.json pronto; confira os quadros antes de rodar gerar_video_ia.py')


if __name__ == '__main__':
    argumentos = argparse.ArgumentParser()
    argumentos.add_argument('--imagem', required=True)
    argumentos.add_argument('--saida', required=True)
    argumentos.add_argument('--vizinhos', nargs='*', type=float, default=[3.0, 5.6])
    a = argumentos.parse_args()
    main(a.imagem, a.saida, a.vizinhos)
