"""Sugestão multicritério: pesos AHP, restrições legais, sensibilidade e contratos da API e do PDF."""
from io import BytesIO

import numpy as np
import pytest
from fastapi.testclient import TestClient
from pypdf import PdfReader
from rasterio.io import MemoryFile
from rasterio.transform import from_origin
from shapely.geometry import shape

from geovale.api.main import criar_app
from geovale.fontes_territorio import recortar_raster
from geovale.multicriterio import CRITERIOS, IDS, RESPOSTAS, USOS, calcular, explicar_por_regras, ler_pesos, notas, pesos_ahp
from geovale.territorio import DadosTerritoriais
from test_territorio import coleta_simulada, preparar_raiz

CELULA = 1 / 3600
LEGENDA = {3: {'codigo': 3, 'nome': '3 - Formação Florestal', 'cor': '#1f8d49'}, 4: {'codigo': 4, 'nome': '4 - Forte ondulado (20% - 45%)', 'cor': '#c78a4f'},
           30: {'codigo': 30, 'nome': '30 - Mineração', 'cor': '#9c0027'}}


def test_pesos_ahp_sao_consistentes_e_somam_um():
    pesos, consistencia = pesos_ahp()
    assert pesos.sum() == pytest.approx(1) and consistencia < .1
    assert IDS[int(np.argmax(pesos))] == 'relevo' and all(p > 0 for p in pesos)


def test_pesos_do_engenheiro_sao_validados_e_normalizados():
    assert ler_pesos(None) is None
    pesos = ler_pesos(','.join(['10'] * len(IDS)))
    assert pesos.sum() == pytest.approx(1) and np.allclose(pesos, 1 / len(IDS))
    for texto in ['1,2', ','.join(['0'] * len(IDS)), ','.join(['-1'] + ['5'] * (len(IDS) - 1)), ','.join(['nan'] * len(IDS)), 'a,b']:
        with pytest.raises(ValueError):
            ler_pesos(texto)


def setor_sintetico(permitido_solar=1.):
    """Setor com fatores médios conhecidos: plano favorece solar; nativo e drenagem favorecem conservação."""
    media = {u['id']: {c: 1. if u['id'] == 'conservacao' else .4 for c in RESPOSTAS[u['id']]} for u in USOS}
    media['solar'] = {c: permitido_solar * (1. if c == 'relevo' else .5) for c in RESPOSTAS['solar']}
    perfil = {'ate8': .1, 'de8a20': .3, 'acima20': .6, 'acima45': .1, 'vegetacao': .4,
              'distancias': {'drenagem': 120., 'acesso': 900., 'urbano': 4000., 'rede': None, 'trilhas': 300.}}
    return {'id': 'S1', 'ha': 30., 'media': media, 'bloqueio': {u['id']: {} for u in USOS}, 'perfil': perfil,
            'permitido': {**{u['id']: 1. for u in USOS}, 'solar': permitido_solar}, 'restricoes': {}, 'cavidades': 0.,
            'cava_ha': 0., 'barragens': [], 'montante': [], 'geometria': {'type': 'Point', 'coordinates': [-43.9, -20.1]}}


def test_contribuicoes_somam_a_nota_e_restricao_zera_o_uso():
    base = {'setores': [setor_sintetico()], 'area_minerada_ha': 30., 'fora_ha': 0.}
    r = calcular(base)
    s = r['setores'][0]
    assert s['ranking'][0]['uso'] == 'conservacao' and s['ranking'][0]['nota'] == pytest.approx(100)
    for uso in s['ranking']:
        assert sum(s['contribuicoes'][uso['uso']].values()) == pytest.approx(uso['nota'])
    bloqueado = calcular({**base, 'setores': [setor_sintetico(permitido_solar=0.)]})['setores'][0]
    solar = next(u for u in bloqueado['ranking'] if u['uso'] == 'solar')
    assert solar['nota'] == 0 and solar['permitido'] == 0 and bloqueado['ranking'][-1]['uso'] == 'solar'


def test_sensibilidade_aponta_criterio_que_troca_o_primeiro_lugar():
    setor = setor_sintetico()
    setor['media']['conservacao'] = {c: (1. if c == 'vegetacao' else .4) for c in RESPOSTAS['conservacao']}
    setor['media']['solar'] = {c: .55 for c in RESPOSTAS['solar']}
    pesos = np.ones(len(IDS)) / len(IDS)
    nota = notas(setor, pesos)
    assert abs(nota['conservacao'] - nota['solar']) < 5
    r = calcular({'setores': [setor], 'area_minerada_ha': 30., 'fora_ha': 0.}, pesos)
    s = r['setores'][0]
    assert not s['robustez']['estavel'] and any(m.startswith('vegetação nativa') for m in s['robustez']['muda_com'])
    assert r['origem_pesos'] == 'engenheiro' and [c['id'] for c in r['criterios']] == IDS


def raster_mineracao(recorte, valor_fundo, mineracao=True):
    """Grade SIRGAS 2000 de um segundo cobrindo o recorte, com bloco de mineração de 60x60 células (cerca de 310 ha) no centro."""
    x0, y0, x1, y1 = recorte.bounds
    largura, altura = int((x1 - x0) / CELULA) + 6, int((y1 - y0) / CELULA) + 6
    valores = np.full((altura, largura), valor_fundo, dtype='uint8')
    if mineracao:
        centro = recorte.representative_point()
        lin, col = int((y1 + 3 * CELULA - centro.y) / CELULA), int((centro.x - x0 + 3 * CELULA) / CELULA)
        valores[lin - 30:lin + 30, col - 30:col + 30] = 30
    with MemoryFile() as memoria:
        with memoria.open(driver='GTiff', width=largura, height=altura, count=1, dtype='uint8', crs='EPSG:4674',
                          transform=from_origin(x0 - 3 * CELULA, y1 + 3 * CELULA, CELULA, CELULA), nodata=0) as d:
            d.write(valores, 1)
        return memoria.read()


def coleta_com_mineracao(base, recorte):
    """Vetores cobrem todo o recorte: APP, ZAS e água excluem silvicultura, solar e ecoturismo."""
    if base['processamento'] != 'wcs':
        return coleta_simulada(base, recorte)
    fundo = 4 if 'decliv' in base['camada'] else 3
    return recortar_raster(raster_mineracao(recorte, fundo, 'mapbiomas' in base['camada']), recorte, LEGENDA)


def test_api_sugere_por_setor_aplica_restricoes_e_leva_pesos_ao_pdf(tmp_path):
    raiz = preparar_raiz(tmp_path)
    fonte = DadosTerritoriais(raiz, coletar=coleta_com_mineracao)
    cliente = TestClient(criar_app(raiz=raiz, territorios=fonte))
    assert cliente.get('/api/minas/horizontes/sugestao').status_code == 503
    fonte.atualizar()
    assert cliente.get('/api/minas/outra/sugestao').status_code == 404
    assert cliente.get('/api/minas/horizontes/sugestao?pesos=1,2').status_code == 422
    resposta = cliente.get('/api/minas/horizontes/sugestao')
    assert resposta.status_code == 200
    r = resposta.json()
    assert r['origem_pesos'] == 'AHP' and r['razao_consistencia'] < .1 and len(r['criterios']) == len(CRITERIOS)
    setor = r['setores'][0]
    assert setor['id'] == 'S1' and setor['ha'] >= r['minimo_ha'] and shape(setor['geometria']).is_valid
    permitidos = {u['uso']: u['permitido'] for u in setor['ranking']}
    assert setor['ranking'][0]['uso'] == 'conservacao' and permitidos['conservacao'] == pytest.approx(100)
    assert permitidos['solar'] == permitidos['silvicultura'] == permitidos['ecoturismo'] == 0
    assert setor['restricoes']['app'] == pytest.approx(100) and setor['explicacao'].startswith('Conservação e restauração: ') and 'APP, onde só conservação e ecoturismo são permitidos' in setor['explicacao']
    explicacao = cliente.get('/api/minas/horizontes/sugestao/explicacao').json()
    assert explicacao == {'metodo': 'regras', 'textos': {s['id']: s['explicacao'] for s in r['setores']}}
    pesos = ','.join(['0'] * (len(IDS) - 1) + ['10'])
    ajustado = cliente.get('/api/minas/horizontes/sugestao?pesos=' + pesos).json()
    assert ajustado['origem_pesos'] == 'engenheiro' and ajustado['criterios'][-1]['peso'] == pytest.approx(1)
    padrao = cliente.get('/api/minas/horizontes/relatorio')
    pdf = cliente.get('/api/minas/horizontes/relatorio?pesos=' + pesos)
    assert padrao.status_code == pdf.status_code == 200 and padrao.content != pdf.content
    texto = ' '.join(' '.join(p.extract_text() for p in PdfReader(BytesIO(pdf.content)).pages).split())
    assert 'Sugestão multicritério' in texto and 'ajustados pelo engenheiro' in texto and 'Por que' in texto and '(IA)' not in texto and 'laudo' not in texto
    assert cliente.get('/api/minas/horizontes/relatorio?pesos=x').status_code == 422


def test_explicacao_por_regras_fala_do_terreno_e_nao_de_pontos():
    resultado = calcular({'setores': [setor_sintetico()], 'area_minerada_ha': 30., 'fora_ha': 0.})
    setor = resultado['setores'][0]
    texto = explicar_por_regras(setor, resultado)
    assert texto.startswith(setor['ranking'][0]['nome'] + ': ') and 'ponto' not in texto and 'peso' not in texto
    assert '% do setor tem declividade' in texto or 'fica a' in texto or 'vegetação nativa cobre' in texto
    assert setor['perfil']['declividade']['acima20'] == pytest.approx(60) and setor['perfil']['distancias']['rede'] is None
