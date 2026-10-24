"""Provas analíticas de declividade e de conservação de ausência na vizinhança."""
import numpy as np
import pytest
from geovale.decisao.territorio import declividade_horn


def test_plano_com_gradiente_conhecido():
    """Um plano com dz/dx=1 e dz/dy=0 deve produzir exatamente 45 graus."""
    z=np.tile(np.arange(7)*30.0,(7,1))
    s=declividade_horn(z,30,30)
    assert np.allclose(s[1:-1,1:-1],45)
    assert np.isnan(s[0]).all() and np.isnan(s[:,0]).all()


def test_relevo_plano_e_nodata_nao_preenchido():
    """Grade plana produz zero; uma célula ausente invalida a vizinhança completa."""
    z=np.ones((9,9))*200
    assert np.allclose(declividade_horn(z,30,30)[1:-1,1:-1],0)
    z[4,4]=np.nan
    s=declividade_horn(z,30,30)
    assert np.isnan(s[3:6,3:6]).all()
    assert s[1,1]==pytest.approx(0)
