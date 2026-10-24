"""Referências analíticas de AHP/TOPSIS e limites que impedem resultados indevidos."""
import numpy as np
import pytest
from geovale.decisao.metodos import calcular_ahp,calcular_topsis,analisar_sensibilidade,ErroDecisao


def test_ahp_recupera_razoes_conhecidas():
    """Razões 6:3:1 produzem 60/30/10% sem inconsistência."""
    r=calcular_ahp([[1,2,6],[.5,1,3],[1/6,1/3,1]])
    assert r['pesos']==pytest.approx([.6,.3,.1]);assert r['razao_consistencia']<1e-10 and r['consistente']


def test_ahp_detecta_ciclo_inconsistente():
    """Preferências cíclicas extremas não são aceitas como consistentes."""
    r=calcular_ahp([[1,9,1/9],[1/9,1,9],[9,1/9,1]])
    assert not r['consistente'] and r['razao_consistencia']>.1


@pytest.mark.parametrize('m',[[[1,2],[2,1]],[[1,0],[0,1]],[[True,1],[1,1]],[[1,float('nan')],[1,1]],[[1,10],[.1,1]],[[1,1],[1]],[]])
def test_ahp_recusa_matriz_invalida(m):
    """Exige reciprocidade, escala, dimensão e números finitos."""
    with pytest.raises(ErroDecisao):calcular_ahp(m)


def test_topsis_exemplo_analitico_com_custo():
    """A primeira opção domina em benefício e custo; resultado exato 1 contra 0."""
    r=calcular_topsis([[10,2],[5,4]],[50,50],['beneficio','custo'])
    assert r['escores']==pytest.approx([1,0]) and r['posicoes']==[1,2]
    assert np.asarray(r['normalizada'])==pytest.approx(np.array([[10,2],[5,4]])/np.sqrt([125,20]))


def test_topsis_invariancia_de_unidade_e_coluna_nula():
    """Alterar unidade não muda resultado; coluna sem informação não inventa diferença."""
    a=calcular_topsis([[1,4,0],[2,2,0],[3,1,0]],[40,60,0],['beneficio']*3)
    b=calcular_topsis([[100,4,0],[200,2,0],[300,1,0]],[40,60,0],['beneficio']*3)
    assert a['escores']==pytest.approx(b['escores']);assert a['colunas_nulas']==[2]


def test_topsis_empate_sem_vencedor_arbitrario():
    """Alternativas iguais ou nulas mantêm empate explícito em 0,5."""
    for m in ([[4,4],[4,4]],[[0,0],[0,0]]):
        r=calcular_topsis(m,[50,50],['beneficio']*2)
        assert r['escores']==[.5,.5] and r['posicoes']==[1,1] and r['sem_discriminacao']


@pytest.mark.parametrize('p',[[20,20],[-10,110],[True,99],[float('inf'),0],[10**400,0],None])
def test_pesos_invalidos_sem_normalizacao_silenciosa(p):
    """Não substitui um pedido inválido por uma prioridade diferente."""
    with pytest.raises(ErroDecisao):calcular_topsis([[1,2],[2,1]],p,['beneficio']*2)


def test_sensibilidade_preserva_soma_e_detecta_mudanca():
    """Verifica cenários de pesos sem apresentá-los como confiança estatística."""
    r=analisar_sensibilidade([[100,0,50],[0,100,50]],[40,40,20],['beneficio']*3)
    assert len(r['cenarios'])==6 and r['mudou_em']>0
    assert all(sum(c['pesos'])==pytest.approx(100) for c in r['cenarios'])
