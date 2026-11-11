# Imagen oficial de Python (el codigo usa anotaciones `X | None`, compatibles con 3.10)
FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    FLET_FORCE_WEB_SERVER=true \
    FLET_SERVER_IP=0.0.0.0 \
    FLET_SERVER_PORT=8550 \
    DB_PATH=/app/sistema_bancario.db

WORKDIR /app

# Dependencias primero para aprovechar la cache de capas
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Codigo de la aplicacion
COPY . .

EXPOSE 8550

# Verifica que el servidor web de Flet responda
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8550/', timeout=3)" || exit 1

CMD ["python", "main.py"]
