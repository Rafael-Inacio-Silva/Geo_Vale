"""Inicia o mapa do GeoVale no computador local."""

import os
import sys
from pathlib import Path


def main():
    """Serve interface compilada e API na mesma origem; em loopback, salvo GEOVALE_HOST na publicação."""
    raiz = Path(__file__).resolve().parent
    if not (raiz / 'frontend/dist/index.html').is_file():
        raise SystemExit('Compile a interface primeiro: cd frontend && npm ci && npm run build')
    sys.path.insert(0, str(raiz / 'backend'))
    import uvicorn
    uvicorn.run('geovale.api.main:app', host=os.environ.get('GEOVALE_HOST', '127.0.0.1'), port=int(os.environ.get('GEOVALE_PORT', '8000')))


if __name__ == '__main__':
    main()
