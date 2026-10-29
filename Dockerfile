# GeoVale publicado (Render, plano Free): API e interface na mesma origem, com o banco territorial
# já coletado como retrato datado (GEOVALE_DADOS_FIXOS=1), sem nova coleta nos servidores do Estado.

# Interface compilada a partir do código, para a imagem não depender de dist/ local.
FROM node:24-slim AS interface
WORKDIR /app/frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

FROM python:3.12-slim
WORKDIR /app
COPY requirements/compatibilidade-linux-x86_64.txt requirements.txt
RUN pip install --no-cache-dir --require-hashes -r requirements.txt
COPY executar.py ./
COPY backend ./backend
COPY dados ./dados
COPY deploy/territorios.sqlite3 ./.local/territorios.sqlite3
COPY --from=interface /app/frontend/dist ./frontend/dist
ENV GEOVALE_HOST=0.0.0.0 \
    GEOVALE_DADOS_FIXOS=1 \
    PYTHONUNBUFFERED=1
# O Render informa a porta em PORT.
CMD ["sh", "-c", "GEOVALE_PORT=${PORT:-10000} exec python executar.py"]
