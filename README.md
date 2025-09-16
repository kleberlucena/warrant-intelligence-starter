# Warrant Intelligence Starter (Django + DRF + ETL + GIS)

**What it does:** Imports CSV/API datasets, cleans and deduplicates people, exposes a REST API, and renders a minimal map/dashboard. Built for real-world portfolios and hiring managers.

## Features
- ETL with pandas (extract → transform → load)
- DRF API with filtering, ordering, pagination
- People deduplication based on (national_id, name, mother_name)
- Minimal Leaflet dashboard
- Dockerized dev + CI + tests + type hints

## Quickstart
```bash
git clone https://github.com/<you>/warrant-intelligence-starter.git
cd warrant-intelligence-starter
cp .env.example .env
docker compose up -d --build
# Open: http://localhost:8000/  and http://localhost:8000/api/
```

## Endpoints
- `GET /api/people/` – list & filters
- `GET /api/warrants/` – list & filters
- `POST /api/etl/import/` – optional, authenticated import

## Tech
Django, DRF, PostgreSQL, pandas, Docker, Leaflet, GitHub Actions.

## License
MIT
