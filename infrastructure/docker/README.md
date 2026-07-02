# Docker Local Development

## Quick Start

```bash
docker compose -f infrastructure/docker/docker-compose.local.yml up --build
```

This starts:

- **db** — PostgreSQL + pgvector on port 5432
- **api** — FastAPI server on port 8000

## Verify

```bash
curl http://localhost:8000/health/live
# {"status":"ok"}
curl http://localhost:8000/v1/leaderboard
# {"entries":[],"pagination":{"limit":100,"offset":0,"total":0}}
```

## Services

| Service | Image | Port | Notes |
|---------|-------|------|-------|
| db | ankane/pgvector:latest | 5432 | Persistent volume `pgdata` |
| api | local build | 8000 | Hot-reload with `docker compose watch` |

## Environment

Default env vars are set in `docker-compose.local.yml`. Override with a `.env` file in the `infrastructure/docker/` directory or via `environment` block.

## Alembic Migrations

Run migrations from the host (requires psql on PATH):

```bash
cd services/api
alembic upgrade head
```

Or exec into the api container:

```bash
docker compose -f infrastructure/docker/docker-compose.local.yml exec api alembic upgrade head
```
