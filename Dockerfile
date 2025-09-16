FROM python:3.11-slim

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc curl git && \
    rm -rf /var/lib/apt/lists/*

COPY pyproject.toml /app/pyproject.toml
RUN pip install --upgrade pip && pip install -e .

COPY . /app

EXPOSE 8000
CMD ["bash", "-lc", "python src/manage.py runserver 0.0.0.0:8000"]
