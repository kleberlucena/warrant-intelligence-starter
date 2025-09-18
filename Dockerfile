# Dockerfile
FROM python:3.8-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    # Ajuste conforme seu fuso
    TZ=America/Recife

# Sistema: pacotes de runtime + build (libpq para Postgres, tzdata p/ timezone)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc \
    libpq5 libpq-dev \
    curl git tzdata netcat-openbsd \
 && rm -rf /var/lib/apt/lists/*

# Diretório da app
WORKDIR /app

# Instale dependências primeiro (cache de build)
COPY requirements.txt /app/requirements.txt
RUN python -m pip install -U pip wheel setuptools \
 && pip install --no-cache-dir -r /app/requirements.txt

# Copie o código
COPY . /app

# Usuário não-root
RUN groupadd -r app && useradd -r -g app app \
 && chown -R app:app /app
USER app

# Variáveis padrão (ajuste no compose/.env em produção)
ENV DJANGO_SETTINGS_MODULE=config.settings \
    PYTHONPATH=/app/src

EXPOSE 8000

# ENTRYPOINT fará wait pelo DB, migrate e collectstatic
ENTRYPOINT ["bash", "entrypoint.sh"]
# Comando padrão: gunicorn (mais adequado que runserver)
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
