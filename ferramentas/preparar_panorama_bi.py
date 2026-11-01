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
    preparar_comparacao_usos(minas, setores, ler('notas_uso.csv'))
    print(f'{destino.name}: {len(minas)} minas, {sum(int(m["setores"]) for m in minas)} setores, {sum(int(m["barragens"]) for m in minas)} registros de barragens por recorte.')



def preparar_comparacao_usos(minas, setores, notas):
    """Resume as quatro notas por mina, ponderando pela área dos seus setores."""
    usos = {'Conservação e restauração', 'Ecoturismo e lazer', 'Silvicultura', 'Energia solar e infraestrutura'}
    areas = {(s['mina_id'], s['setor']): Decimal(s['area_ha']) for s in setores}
    if len(areas) != len(setores) or any(not a.is_finite() or a <= 0 for a in areas.values()):
        raise ValueError('Setores repetidos ou com área inválida.')
    valores = {}
    for nota in notas:
        chave = (nota['mina_id'], nota['setor'], nota['uso'])
        valor = Decimal(nota['nota'])
        if chave in valores or chave[:2] not in areas or chave[2] not in usos or not valor.is_finite() or not 0 <= valor <= 100:
            raise ValueError(f'Nota inválida, repetida ou sem setor: {chave}.')
        valores[chave] = valor
    esperados = {(m, s, u) for m, s in areas for u in usos}
    if set(valores) != esperados:
        raise ValueError('As quatro opções precisam ter nota para todos os setores.')
    linhas = []
    for mina in minas:
        identificador = mina['mina_id']
        grupo = {k: a for k, a in areas.items() if k[0] == identificador}
        area_total = sum(grupo.values(), Decimal(0))
        for uso in sorted(usos):
            soma = sum((a * valores[(m, s, uso)] for (m, s), a in grupo.items()), Decimal(0))
            linhas.append({'mina_id': identificador, 'uso': uso,
                           'nota_ponderada': (soma / area_total).quantize(Decimal('0.1')),
                           'area_setores_ha': area_total, 'quantidade_setores': len(grupo)})
    destino = RAIZ / 'bi' / 'comparacao_usos.csv'
    with destino.open('w', encoding='utf-8', newline='') as arquivo:
        escrita = csv.DictWriter(arquivo, fieldnames=list(linhas[0]))
        escrita.writeheader()
        escrita.writerows(linhas)
    print(f'{destino.name}: {len(linhas)} combinações de mina e uso.')


if __name__ == '__main__':
    preparar()
