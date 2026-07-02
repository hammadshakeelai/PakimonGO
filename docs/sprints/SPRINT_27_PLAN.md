# Sprint 27 Plan: Docker Compose Local Dev Environment

## Sprint Goal

Create a full local development environment using Docker Compose so new contributors can run the API stack with a single command.

## Sprint Status

Complete.

## Sprint Backlog

| ID | Status | Task | Acceptance | Verification |
|---|---|---|---|---|
| S27-001 | Done | Create API Dockerfile | Python 3.13-slim, installs deps, runs uvicorn | File exists, parsed correctly, uvicorn in CMD |
| S27-002 | Done | Expand docker-compose.local.yml with api service | Builds from repo root, depends on db (health check), port 8000, named volumes | Compose YAML validates |
| S27-003 | Done | Add .env.docker example | Documented env vars for each compose service | File exists with all required vars |
| S27-004 | Done | Update README with Docker instructions | Docker as primary dev path, curl verify, alembic instructions | README updated |

## File Ownership

| Area | Owner | Notes |
|---|---|---|
| `services/api/Dockerfile` | Backend agent | Multi-stage build (future) |
| `infrastructure/docker/docker-compose.local.yml` | Backend agent | db + api services |
| `infrastructure/docker/.env.docker` | Backend agent | Environment overrides |
| `README.md` | Lead agent | Docker section |
