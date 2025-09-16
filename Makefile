.PHONY: dev test lint fmt type cov makemigrations migrate superuser

dev:
	docker compose up --build -d
	sleep 3
	docker compose exec web bash -lc "python src/manage.py migrate && python src/manage.py createsuperuser --noinput || true"

test:
	docker compose exec web bash -lc "pytest -q --disable-warnings"

lint:
	docker compose exec web bash -lc "ruff check src tests"

fmt:
	docker compose exec web bash -lc "ruff check --fix src tests || true; black src tests; isort src tests"

type:
	docker compose exec web bash -lc "mypy src"

migrate:
	docker compose exec web bash -lc "python src/manage.py migrate"

makemigrations:
	docker compose exec web bash -lc "python src/manage.py makemigrations"

superuser:
	docker compose exec web bash -lc "python src/manage.py createsuperuser"
