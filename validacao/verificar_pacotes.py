"""Confere integridade, extração dos dois casos e leitura do GeoPackage sem rede."""
from pathlib import Path
import json
import sys

RAIZ=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(RAIZ/'backend'))
from geovale.decisao.territorio import CODIGOS,DADOS,carregar_caso,resumo_entrada,analisar_territorio
from geovale.decisao.metodos import calcular_topsis


def main():
    """Executa os mesmos indicadores da API e informa dados verificáveis, sem validar a decisão de uso."""
    for codigo in CODIGOS:
        m=carregar_caso(codigo)
        entrada=resumo_entrada((DADOS/codigo/'area.geojson').read_bytes(),'mapa.geojson')
        a=analisar_territorio(entrada)
        resultado=calcular_topsis(a['matriz'],[33.34,33.33,33.33],['beneficio']*3)
        print(json.dumps({'mina':m['nome'],'arquivos_conferidos':len(m['sha256']),'area_ha':entrada['area_ha'],
              'declividade_mediana_graus':a['relevo']['declividade_mediana_graus'],'ano_cobertura':a['cobertura']['ano'],
              'indices_relativos':resultado['escores'],'decisao_de_uso':a['triagem']['decisao_de_uso']},ensure_ascii=False))
    import geopandas as gpd
    mapa=gpd.read_file(RAIZ/'dados/qgis/minas.gpkg',layer='minas')
    assert len(mapa)==2 and mapa.geometry.is_valid.all()
    print('GeoPackage: 2 geometrias válidas. Interface QGIS não executada.')


if __name__=='__main__':
    main()
