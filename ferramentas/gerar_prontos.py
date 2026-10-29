"""Gera em dados/prontos a sugestão, a explicação e o relatório padrão (pesos AHP) servidos na publicação.

Usa o banco local, que precisa ser igual ao da imagem (deploy/territorios.sqlite3), e a chave de .local/ia.env.
Rodar de novo sempre que trocar o banco, as réguas, os pesos ou o relatório:
    PYTHONPATH=backend .venv-geovale/bin/python ferramentas/gerar_prontos.py
"""
import filecmp
import json
import os
import sys
from pathlib import Path

from fastapi.testclient import TestClient

RAIZ = Path(__file__).resolve().parents[1]
os.environ.pop('GEOVALE_DADOS_FIXOS', None)  # gera ao vivo, nunca a partir de prontos antigos

from geovale.api.main import criar_app
from geovale.territorio import DadosTerritoriais


def gerar(cliente, mina_id, destino):
    base = f'/api/minas/{mina_id}'
    explicacao = cliente.get(base + '/sugestao/explicacao')
    if explicacao.status_code != 200 or explicacao.json()['metodo'] != 'ia':
        sys.exit(f'{mina_id}: explicação sem IA ({explicacao.status_code}); confira .local/ia.env.')
    relatorio = cliente.get(base + '/relatorio')
    if relatorio.status_code != 200:
        sys.exit(f'{mina_id}: relatório {relatorio.status_code}.')
    sugestao = cliente.get(base + '/sugestao').json()
    (destino / f'{mina_id}-sugestao.json').write_text(json.dumps(sugestao, ensure_ascii=False), encoding='utf-8')
    (destino / f'{mina_id}-explicacao.json').write_text(json.dumps(explicacao.json(), ensure_ascii=False), encoding='utf-8')
    (destino / f'{mina_id}-relatorio.pdf').write_bytes(relatorio.content)
    print(mina_id, len(relatorio.content), 'bytes')


def main():
    destino = RAIZ / 'dados/prontos'
    destino.mkdir(exist_ok=True)
    minas = json.loads((RAIZ / 'dados/minas.json').read_text(encoding='utf-8'))
    if not filecmp.cmp(RAIZ / '.local/territorios.sqlite3', RAIZ / 'deploy/territorios.sqlite3', shallow=False):
        sys.exit('O banco local difere de deploy/territorios.sqlite3; copie um sobre o outro antes.')
    # Com o ciclo de vida iniciado, como no servidor; dados fixos, sem coletar.
    with TestClient(criar_app(territorios=DadosTerritoriais(RAIZ, fixos=True))) as cliente:
        for mina in minas:
            gerar(cliente, mina['id'], destino)


if __name__ == '__main__':
    main()
