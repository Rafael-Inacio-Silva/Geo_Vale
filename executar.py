"""Inicia a demonstração local com interface compilada e API na mesma origem."""
import os
import sys
from pathlib import Path


def main():
    """Serve somente no computador local e exige a compilação prévia da interface."""
    raiz=Path(__file__).resolve().parent
    if not (raiz/'frontend/dist/index.html').is_file():
        raise SystemExit('Compile a interface primeiro: cd frontend && npm ci && npm run build')
    sys.path.insert(0,str(raiz/'backend'))
    import uvicorn
    uvicorn.run('geovale.api.main:app',host='127.0.0.1',port=int(os.environ.get('GEOVALE_PORT','8000')))


if __name__=='__main__':
    main()
