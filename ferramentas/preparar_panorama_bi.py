"""Consolida os CSVs exportados numa linha por mina para o panorama no Looker."""
import csv
from decimal import Decimal
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]


def ler(nome):
    """Lê a exportação sem alterar seus dados originais."""
    with (RAIZ / 'bi' / nome).open(encoding='utf-8', newline='') as arquivo:
        return list(csv.DictReader(arquivo))


def preparar():
    """Acrescenta contagens de usos e áreas de cobertura, sem multiplicar minas."""
    minas, setores, cobertura = ler('minas.csv'), ler('setores.csv'), ler('cobertura_terra.csv')
    if len({m['mina_id'] for m in minas}) != len(minas):
        raise ValueError('A exportação contém minas repetidas.')
    for mina in minas:
        identificador = mina['mina_id']
        selecionados = [s for s in setores if s['mina_id'] == identificador]
        classes = [c for c in cobertura if c['mina_id'] == identificador]
        if len(selecionados) != int(mina['setores']) or not classes:
            raise ValueError(f'Exportação incompleta para {identificador}.')
        usos = {'Conservação e restauração': 'conservacao', 'Ecoturismo e lazer': 'ecoturismo'}
        if any(s['uso_1'] not in usos for s in selecionados):
            raise ValueError('Novo uso precisa ser incluído no panorama e no gráfico.')
        mina['mina_curta'] = mina['mina'].removeprefix('Mina ')
        for nome, campo in usos.items():
            grupo = [s for s in selecionados if s['uso_1'] == nome]
            mina[f'{campo}_setores'] = len(grupo)
            mina[f'{campo}_ha'] = sum((Decimal(s['area_ha']) for s in grupo), Decimal(0))
        mina['vegetacao_nativa_ha'] = sum((Decimal(c['area_ha']) for c in classes if c['nativa'] == 'sim'), Decimal(0))
        mina['outras_coberturas_ha'] = sum((Decimal(c['area_ha']) for c in classes if c['nativa'] != 'sim'), Decimal(0))
        mina['cobertura_total_ha'] = mina['vegetacao_nativa_ha'] + mina['outras_coberturas_ha']
    destino = RAIZ / 'bi' / 'panorama.csv'
    with destino.open('w', encoding='utf-8', newline='') as arquivo:
        escrita = csv.DictWriter(arquivo, fieldnames=list(minas[0]))
        escrita.writeheader()
        escrita.writerows(minas)
    print(f'{destino.name}: {len(minas)} minas, {sum(int(m["setores"]) for m in minas)} setores, {sum(int(m["barragens"]) for m in minas)} registros de barragens por recorte.')


if __name__ == '__main__':
    preparar()
