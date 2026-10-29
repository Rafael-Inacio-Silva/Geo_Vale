"""Exporta para bi/ os dados já calculados das minas, em CSV para o Looker Studio.

    PYTHONPATH=backend .venv-geovale/bin/python ferramentas/exportar_bi.py

Usa o banco local com dados fixos (o mesmo da publicação) e a sugestão padrão salva em dados/prontos,
para os números baterem com o relatório e com o site. CSV em UTF-8, vírgula como separador e ponto decimal.
"""
import csv
import json
from pathlib import Path

from geovale.fichas import NATIVA, chave_base, dividir, distribuicao, montar_fichas, normalizar, preparar, projetar
from geovale.relatorio import ler_cenario
from geovale.territorio import DadosTerritoriais

RAIZ = Path(__file__).resolve().parents[1]
DESTINO = RAIZ / 'bi'


def r(valor, casas=1):
    return None if valor is None else round(float(valor), casas)


def gravar(nome, linhas):
    with (DESTINO / nome).open('w', encoding='utf-8', newline='') as arquivo:
        escrita = csv.DictWriter(arquivo, fieldnames=list(linhas[0]))
        escrita.writeheader()
        escrita.writerows(linhas)
    print(nome, len(linhas), 'linhas')


def main():
    DESTINO.mkdir(exist_ok=True)
    fonte = DadosTerritoriais(RAIZ, fixos=True)
    minas = json.loads((RAIZ / 'dados/minas.json').read_text(encoding='utf-8'))
    tabelas = {n: [] for n in ('minas', 'setores', 'notas_uso', 'cobertura_terra', 'fatos_relatorio')}
    pesos = None
    for mina in minas:
        m = mina['id']
        dados = fonte.relatorio(m)
        dados['rasters'] = {b['base']['id']: fonte.arquivo(m, b['base']['id']) for b in dados['bases'] if b['tipo'] == 'raster'}
        preparar(dados)
        minerada = dados['area_minerada']
        sugestao = json.loads((RAIZ / f'dados/prontos/{m}-sugestao.json').read_text(encoding='utf-8'))
        pesos = pesos or sugestao['criterios']

        def medir(chave):
            fs = [x for b in dados['bases'] if b['tipo'] == 'vetor' and chave_base(b) == chave for x in b['dados']['features']]
            return dividir(fs, minerada), len(fs)

        cobertura = next(b for b in dados['bases'] if b['tipo'] == 'raster' and b['base']['tema_id'] == 'vegetacao')
        grade = dados['grades'][cobertura['base']['id']]
        _, classes = distribuicao(grade, cobertura.get('classes', []), grade['validos'])
        app, _ = medir('apps_fbds')
        zas, _ = medir('zas_pae')
        _, barragens = medir('barragens')
        cava = projetar(next(f['geometry'] for f in dados['influencia']['features'] if f['properties']['id'] == 'mina')).area / 1e4
        primeiro = {}
        for s in sugestao['setores']:
            primeiro[s['ranking'][0]['nome']] = primeiro.get(s['ranking'][0]['nome'], 0) + s['ha']
        processo = mina.get('processo_anm') or {}
        tabelas['minas'].append({
            'mina_id': m, 'mina': mina['nome'], 'empresa': mina['empresa'], 'municipio': mina['municipio'], 'uf': mina['uf'],
            'latitude': mina['latitude'], 'longitude': mina['longitude'], 'lat_long': f"{mina['latitude']},{mina['longitude']}",
            'processo_anm': f"{processo.get('numero')}/{processo.get('ano')}" if processo else None,
            'tipo_recorte': 'AII de estudo (FEAM)' if 'sha256_pdf' in dados['influencia']['fonte'] else 'Faixa de 3 km da cava',
            'recorte_ha': r(dados['recorte_ha']), 'area_minerada_ha': r(minerada['ha']),
            'area_minerada_pct': r(minerada['ha'] * 100 / dados['recorte_ha']), 'cava_osm_ha': r(cava),
            'vegetacao_nativa_pct': r(sum(c['percentual'] for c in classes if NATIVA.search(normalizar(c['nome'])))),
            'app_ha': r(app['total']), 'app_na_minerada_ha': r(app['dentro']), 'zas_ha': r(zas['total']), 'zas_na_minerada_ha': r(zas['dentro']),
            'barragens': barragens, 'setores': len(sugestao['setores']), 'uso_predominante': max(primeiro, key=primeiro.get),
            'trilhas_com_dado': 'nao' if any(c.get('sem_dado') for c in sugestao['criterios']) else 'sim',
        })
        for c in classes:
            tabelas['cobertura_terra'].append({'mina_id': m, 'mina': mina['nome'], 'classe': c['nome'], 'area_ha': r(c['ha']), 'percentual': r(c['percentual'], 2),
                                               'nativa': 'sim' if NATIVA.search(normalizar(c['nome'])) else 'nao'})
        for s in sugestao['setores']:
            perfil = s['perfil']
            tabelas['setores'].append({
                'mina_id': m, 'mina': mina['nome'], 'setor': s['id'], 'mina_setor': f"{mina['nome']} · {s['id']}", 'area_ha': r(s['ha']),
                'uso_1': s['ranking'][0]['nome'], 'nota_1': r(s['ranking'][0]['nota']), 'uso_2': s['ranking'][1]['nome'], 'nota_2': r(s['ranking'][1]['nota']),
                'margem': r(s['margem']), 'estavel_20pct': 'sim' if s['robustez']['estavel'] else 'nao',
                'app_pct': r(s['restricoes']['app']), 'zas_pct': r(s['restricoes']['zas']), 'uc_protecao_integral_pct': r(s['restricoes']['pi_restrita'] + s['restricoes']['pi_visitacao']),
                'cavidades_alto_pct': r(s['cavidades']), 'declividade_acima_20_pct': r(perfil['declividade']['acima20']),
                'declividade_ate_8_pct': r(perfil['declividade']['ate8']), 'vegetacao_entorno_pct': r(perfil['vegetacao']),
                'dist_drenagem_m': r(perfil['distancias']['drenagem'], 0), 'dist_rodovia_m': r(perfil['distancias']['acesso'], 0),
                'dist_urbano_m': r(perfil['distancias']['urbano'], 0), 'barragens': len(s['barragens']),
            })
            for posicao, u in enumerate(s['ranking'], 1):
                tabelas['notas_uso'].append({'mina_id': m, 'mina': mina['nome'], 'setor': s['id'], 'mina_setor': f"{mina['nome']} · {s['id']}",
                                             'uso': u['nome'], 'posicao': posicao, 'nota': r(u['nota']), 'lei_permite_pct': r(u['permitido'])})
        for ficha in montar_fichas(dados, ler_cenario(RAIZ, m)):
            for d in ficha['dados']:
                tabelas['fatos_relatorio'].append({'mina_id': m, 'mina': mina['nome'], 'tema': ficha['nome'], 'dado': d['nome'],
                                                   'resumo': d.get('resumo', ''), 'valor': d['valor'].replace('\n', ' | '), 'origem': d['origem']})
    tabelas['pesos'] = [{'criterio': c['nome'], 'peso_ahp_pct': r(c['peso_ahp'] * 100)} for c in pesos]
    for nome, linhas in tabelas.items():
        gravar(f'{nome}.csv', linhas)


if __name__ == '__main__':
    main()
