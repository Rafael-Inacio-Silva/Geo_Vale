"""Gera, uma vez, o vídeo do sobrevoo da Horizontes com a paisagem pós-mineração (fora do servidor do GeoVale).

A primeira tentativa, só com texto e edição média, inventou outro lugar (cava redonda com lago), perdeu a câmera
e o HUD. Num teste de um quadro, faixas pretas laterais também fizeram o FLUX Kontext reinventar a cena, e o Kontext
sem faixas pintou tudo de verde; o Nano Banana manteve câmera, HUD, cidade e estradas e mudou só a mina. Por isso:
1. O vídeo inteiro é acelerado para 10 s (o máximo do modelo) e recortado em 16:9, tirando só as bordas de cima e de baixo.
2. Quadros-chave em que a mina aparece são editados pelo Nano Banana, que muda só a mina.
3. O vídeo é editado pelo Luma Ray v3.2 com transformação mínima (adhere) e guiado por esses quadros.
4. O resultado volta à duração original. A gravação recebe o mesmo recorte, para os dois ficarem lado a lado.

Depende de `fal-client` e `imageio-ffmpeg`, num ambiente separado do GeoVale. A chave (FAL_KEY=) fica num .env local
e nunca é impressa. O resultado é ilustração, não projeto.

Uso: python gerar_video_ia.py --env caminho/.env --saida pasta [--so-quadros]
(rode primeiro com --so-quadros e confira os quadros editados antes de pagar o vídeo)
"""
import argparse
import json
import os
import subprocess
import urllib.request
from pathlib import Path

import fal_client
import imageio_ffmpeg

ORIGEM = Path('/Users/rafaelinaciosilva/PycharmProjects/Reviver/GeoVale/video_aviao.mp4')
MODELO_IMAGEM = 'fal-ai/nano-banana/edit'
MODELO_VIDEO = 'luma/agent/ray/v3.2/video-to-video'
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
DURACAO = 10
# Segundos do vídeo original. Em 0 s e 7,5 s a mina está pequena ou na borda e o modelo não muda nada ou inventa uma cava
# redonda; âncora ruim faz o vídeo inventar. Ficam só os instantes em que a edição saiu fiel.
QUADROS_COM_MINA = [2.5, 5]
QUADROS_SEM_MINA = [10, 12.4]  # entram sem edição, para o modelo manter céu e HUD como estão
# Editar, não reimaginar: só o solo exposto da cava muda, nos tons da mata vizinha; o que já é verde fica intocado.
# Sem lago (o pedido de lago gerou um lago enorme). Com o primeiro texto, o modelo pintou de verde-limão a mata existente.
PROMPT_IMAGEM = ('Edit only the open-pit mine: the terraced benches of bare red, orange, yellow, grey and purple soil. Replace that bare soil '
                 'with natural vegetation in the same dark and medium green tones as the existing forest around it, keeping the terrace lines '
                 'visible. Do not change any area that is already green or dark, and do not change the town, roads, lakes, sky, hills or the '
                 'thin green HUD lines and numbers. Keep the exact composition, camera and zoom.')
VARIACOES = 2  # o modelo varia muito: gera duas por quadro; a escolhida fica em quadros.json (a primeira, por padrão)
PROMPT_VIDEO = ('The open-pit iron ore mines are fully restored: their terraced benches and bare red and grey soil are covered by green native '
                'grass and young trees, like the surrounding hills. Everything else stays exactly the same: camera motion, framing, town, roads, '
                'existing lakes, forests, sky and the thin green flight simulator HUD lines and numbers. No new water, no buildings, no text.')


def ler_chave(env):
    for linha in Path(env).read_text().splitlines():
        nome, sep, valor = linha.partition('=')
        if sep and nome.strip() == 'FAL_KEY':
            return valor.strip().strip('"').strip("'")
    raise SystemExit('FAL_KEY não encontrada no .env')


def ffmpeg(*args):
    subprocess.run([FFMPEG, '-hide_banner', '-loglevel', 'error', '-y', *args], check=True)


def medir(video):
    """Duração (s) e tamanho do vídeo, lidos da saída do ffmpeg."""
    info = subprocess.run([FFMPEG, '-i', str(video)], capture_output=True, text=True).stderr
    h, m, s = info.split('Duration: ')[1].split(',')[0].split(':')
    largura, altura = next(p for p in info.split('Video: ')[1].split(', ') if 'x' in p and p.split('x')[0].isdigit()).split(' ')[0].split('x')
    return int(h) * 3600 + int(m) * 60 + float(s), int(largura), int(altura)


# Recorte 16:9 da gravação em 1280 px de largura: a faixa de 720 px começa em y=100, abaixo do título da janela e
# com a régua de rumo e a escada do HUD inteiras.
RECORTE = 'scale=1280:-2,crop=1280:720:0:100'


def preparar(pasta):
    """Vídeo de 10 s, 1280×720, acelerado e recortado; e a gravação com o mesmo recorte, para o lado esquerdo."""
    total, _, _ = medir(ORIGEM)
    fator = total / DURACAO
    entrada, esquerda = pasta / 'entrada_ia.mp4', pasta / 'aviao_original_recortado.mp4'
    ffmpeg('-i', str(ORIGEM), '-an', '-vf', f'{RECORTE},setpts=PTS/{fator},fps=30,format=yuv420p',
           '-t', str(DURACAO), '-c:v', 'libx264', '-crf', '16', str(entrada))
    ffmpeg('-i', str(ORIGEM), '-an', '-vf', f'{RECORTE},fps=30,format=yuv420p', '-c:v', 'libx264', '-crf', '18',
           '-movflags', '+faststart', str(esquerda))
    return entrada, fator


def editar(pasta, t, arquivo):
    """Edita um quadro no Nano Banana e guarda as variações; devolve a primeira. Referência a outro quadro deslocava a cena."""
    resultado = fal_client.subscribe(MODELO_IMAGEM, arguments={
        'prompt': PROMPT_IMAGEM, 'image_urls': [fal_client.upload_file(str(arquivo))], 'aspect_ratio': '16:9',
        'output_format': 'png', 'num_images': VARIACOES})
    variacoes = []
    for i, imagem in enumerate(resultado['images']):
        bruto, editado = pasta / f'quadro_{t}_nano_{i}.png', pasta / f'quadro_{t}_editado_{i}.png'
        urllib.request.urlretrieve(imagem['url'], bruto)
        ffmpeg('-i', str(bruto), '-vf', 'scale=1280:720', str(editado))
        variacoes.append(editado)
    return variacoes[0]


def quadros(pasta, entrada, fator):
    """Extrai os quadros-chave; os que têm mina são editados, os outros seguem iguais."""
    saida = []
    for t in QUADROS_COM_MINA + QUADROS_SEM_MINA:
        tempo = min(t / fator, DURACAO - 1 / 30)
        arquivo = pasta / f'quadro_{t}.png'
        ffmpeg('-ss', f'{tempo:.3f}', '-i', str(entrada), '-frames:v', '1', str(arquivo))
        if t in QUADROS_COM_MINA:
            arquivo = editar(pasta, t, arquivo)
        saida.append((round(tempo * 30), arquivo))
        print(f'quadro {t} s → índice {saida[-1][0]}: {arquivo.name}')
    return saida


def video(pasta, entrada, chaves):
    resultado = fal_client.subscribe(MODELO_VIDEO, arguments={
        'prompt': PROMPT_VIDEO, 'video_url': fal_client.upload_file(str(entrada)), 'resolution': '720p',
        'duration': f'{DURACAO}s', 'edit_strength': 'adhere_3',
        'keyframes': [fal_client.upload_file(str(a)) for _, a in chaves], 'keyframe_indexes': [i for i, _ in chaves],
    }, with_logs=True, on_queue_update=lambda u: print(type(u).__name__) if type(u).__name__ != 'InProgress' else None)
    gerado = pasta / 'gerado_ia.mp4'
    urllib.request.urlretrieve(resultado['video']['url'], gerado)
    return gerado


def finalizar(pasta, gerado, fator):
    """Volta à duração original, no mesmo tamanho do lado esquerdo (1280×720)."""
    final = pasta / 'aviao_pos_mineracao.mp4'
    ffmpeg('-i', str(gerado), '-an', '-vf', f'setpts=PTS*{fator},fps=30,scale=1280:720,format=yuv420p',
           '-c:v', 'libx264', '-crf', '18', '-movflags', '+faststart', str(final))
    return final


if __name__ == '__main__':
    argumentos = argparse.ArgumentParser()
    argumentos.add_argument('--env', required=True)
    argumentos.add_argument('--saida', required=True)
    argumentos.add_argument('--so-quadros', action='store_true', help='para depois dos quadros-chave, para conferir antes de pagar o vídeo')
    a = argumentos.parse_args()
    os.environ['FAL_KEY'] = ler_chave(a.env)
    pasta = Path(a.saida)
    pasta.mkdir(parents=True, exist_ok=True)
    entrada, fator = preparar(pasta)
    estado = pasta / 'quadros.json'
    if a.so_quadros or not estado.exists():
        chaves = quadros(pasta, entrada, fator)
        estado.write_text(json.dumps([[i, str(p)] for i, p in chaves]))
        if a.so_quadros:
            raise SystemExit(0)
    chaves = [(i, Path(p)) for i, p in json.loads(estado.read_text())]
    final = finalizar(pasta, video(pasta, entrada, chaves), fator)
    print(f'pronto: {final}')
