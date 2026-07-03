# PakimonGO

PakimonGO is a 13+ mobile app for real-animal photography, discovery, collections, map exploration, privacy-safe social sharing, and server-scored competition.

## Current Phase

Phase 6: Feature implementation. All Sprints 2-42 complete. 103 API tests + 61 scoring-rules tests + 102 Flutter tests = 266 total, all passing.

## Repository Layout

- `apps/mobile/pakimon_go_app/`: Flutter app with Mapbox map prototype.
- `services/api/`: FastAPI modular monolith (auth, media, submissions, users, leaderboard).
- `services/workers/`: async scoring worker (in-process daemon thread).
- `packages/scoring-rules/`: scoring engine, precheck, VisionProvider protocol, goldset runner.
- `infrastructure/`: database, Firebase, Docker, Cloud Run assets.
- `data/goldsets/`: duplicate and zoo detection benchmark datasets.
- `docs/`: SRS, ADRs, process, QA specs, sprint plans, backlog, and state docs.
- `knowledge/`: OKF and project knowledge files.
- `tools/qa/`: validation scripts (docs, JSON, secrets, toolchain).

## Quick Start

### Prerequisites

- Python 3.13+
- Docker (recommended) or PostgreSQL locally
- Flutter SDK (for mobile)

### Run with Docker (recommended)

```bash
docker compose -f infrastructure/docker/docker-compose.local.yml up --build
```

This starts PostgreSQL + pgvector and the FastAPI server on port 8000.

```bash
curl http://localhost:8000/health/live
# {"status":"ok"}
```

### Run without Docker

```bash
cd services/api
pip install -r requirements.txt
# Set env: SYNC_DATABASE_URL, UPLOAD_BASE (see .env.example)
python -m uvicorn src.main:app --reload --port 8000
```

### Deploy to Render

```bash
# 1. Push repo to GitHub, then connect at https://render.com
# 2. Render auto-detects render.yaml — click "Deploy"
# 3. Set secrets (see .env.example) in Render dashboard
# 4. First deploy: apply Alembic migrations:
#    render shell: cd services/api && alembic upgrade head
```

See `render.yaml` for service definition. The API uses gunicorn + uvicorn workers for production.

### Run Tests

```bash
# API tests (103 tests)
cd services/api
python -m pytest -v

# Scoring-rules tests (61 tests)
cd packages/scoring-rules
python -m pytest -v

# Flutter tests (102 tests)
cd apps/mobile/pakimon_go_app
flutter test
```

### QA Validation

```powershell
python tools/qa/validate_docs.py
python tools/qa/validate_json_examples.py
python tools/qa/scan_secrets.py
python tools/qa/pre_task_check.py
```

## API Endpoints (all under `/v1/`)

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | /health/live | No | Liveness check |
| GET | /health/ready | No | Readiness check |
| POST | /media/upload-intent | Yes | Create upload intent |
| PUT | /media/upload/{id} | Yes | Upload file |
| POST | /media/complete-upload | Yes | Complete upload, generate derivatives |
| GET | /media/derivatives/{id} | Yes | Get derivative URLs |
| GET | /media/files/{subdir}/{filename} | No | Serve stored file |
| POST | /submissions | Yes | Create submission (with precheck + scoring) |
| GET | /submissions | Yes | List user submissions (paginated) |
| GET | /submissions/{id} | Yes | Get submission details |
| GET | /users/me | Yes | Get/sync user profile |
| PATCH | /users/me | Yes | Update profile |
| GET | /users/me/collection | Yes | Get species collection (paginated) |
| GET | /leaderboard | No | Global leaderboard (paginated) |
| GET | /notifications | Yes | List notifications (paginated, unread filter) |
| PATCH | /notifications/{id}/read | Yes | Mark notification as read |
| GET | /notifications/unread-count | Yes | Unread notification count |

See `docs/api/OPENAPI_DRAFT.yaml` for full schema details.

## Planning & Design Artifacts

- SRS: `docs/SRS.md`
- Requirements: `docs/REQUIREMENTS.md`
- Traceability matrix: `docs/TRACEABILITY_MATRIX.md`
- Architecture decisions: `docs/adr/` (17 ADRs, all accepted)
- Sprint plans: `docs/sprints/`
- QA specs: `docs/qa/`
- State docs: `docs/CURRENT_TASK.md`, `docs/NEXT_TASK.md`, `docs/CURRENT_THINKING.md`

## Process

1. Read `AGENTS.md`, then `docs/CURRENT_TASK.md`, `docs/NEXT_TASK.md`.
2. Follow the mandatory 9-step task loop (pre-check → read state → do work → validate → commit).
3. Make short-burst semantic commits with AI attribution trailers.
