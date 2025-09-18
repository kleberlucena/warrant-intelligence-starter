# entrypoint.sh
set -e

# Espera o Postgres ficar disponível (usa DATABASE_URL)
if [ -n "$DATABASE_URL" ]; then
  echo "Aguardando Postgres em $DATABASE_URL ..."
  python - <<'PY'
import os, time, sys
import urllib.parse as up
from psycopg import connect  # psycopg v3
url = os.environ.get("DATABASE_URL")
assert url, "DATABASE_URL ausente"
# psycopg aceita a URL postgresql://...
for i in range(60):
    try:
        with connect(url, connect_timeout=3) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1;")
        print("Postgres pronto.")
        sys.exit(0)
    except Exception as e:
        print(f"Aguardando DB... ({i+1}/60) -> {e}")
        time.sleep(1)
sys.exit("Timeout esperando o Postgres")
PY
fi

echo "Rodando migrações..."
python src/manage.py migrate --noinput

# Coleta estáticos (se precisar)
if [ "${DISABLE_COLLECTSTATIC:-0}" != "1" ]; then
  echo "Coletando estáticos..."
  python src/manage.py collectstatic --noinput
fi

echo "Iniciando aplicação..."
exec "$@"
