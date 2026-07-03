<p align="center">
  <img src="docs/assets/app-icon.svg" alt="PakimonGO app icon" width="120" height="120">
</p>

<p align="center">
  <img src="docs/assets/banner.svg" alt="PakimonGO" width="100%">
</p>

<p align="center">
  <a href="https://github.com/hammadshakeelai">
    <img src="https://img.shields.io/badge/GitHub-hammadshakeelai-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub" height="34">
  </a>
  &nbsp;
  <a href="https://www.linkedin.com/in/hammadshakeelai">
    <img src="https://img.shields.io/badge/LinkedIn-Hammad_Shakeel-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" height="34">
  </a>
</p>

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

## 👤 Author

**Hammad Shakeel** — [@hammadshakeelai](https://github.com/hammadshakeelai)

<p>
  <a href="https://github.com/hammadshakeelai">
    <img src="https://img.shields.io/badge/GitHub-hammadshakeelai-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub" height="30">
  </a>
  &nbsp;
  <a href="https://www.linkedin.com/in/hammadshakeelai">
    <img src="https://img.shields.io/badge/LinkedIn-Hammad_Shakeel-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" height="30">
  </a>
</p>

Builder of AI-agent tooling, scientific simulators, and full-stack apps. PakimonGO is
one of many projects exploring agent-driven engineering at scale.

### Skills & Tech

| Area | Tools & Technologies |
|------|----------------------|
| **Languages** | Python, Dart, TypeScript, JavaScript, C++, C, Java, R, NASM Assembly, SQL |
| **AI / ML** | Machine Learning, Deep Learning, NLP, LSTMs, computer vision, agentic AI, RAG |
| **Mobile & Web** | Flutter, FastAPI, Node/TypeScript, vanilla JS, HTML/CSS, Vercel |
| **Backend & Data** | REST APIs, PostgreSQL, pgvector, Docker, OpenAPI, databases & data structures |
| **AI Agent Tooling** | Claude Code skills & slash commands, Kaggle automation, multi-agent workflows |
| **CS Foundations** | Operating systems, computer architecture, assembly/NASM, algorithms |

## 🔗 More of My Work

A selection of other projects and ideas I've built:

### AI Agents & Developer Tooling
- [**agentic-ai-megaproject-template**](https://github.com/hammadshakeelai/agentic-ai-megaproject-template) — Topic-agnostic starter for building super-large software projects with AI agents: phase-gated lifecycle, state-file memory, traceability chain, adversarial ADRs, and CI gates. *(The methodology behind PakimonGO.)*
- [**kaggle-run-skill**](https://github.com/hammadshakeelai/kaggle-run-skill) — Kaggle slash command for Claude Code & 35+ AI agents: deploy notebooks, auto-fix 13 error patterns, submit competitions — a token-minimal 165-line router + Python scripts.
- [**mcq-maker**](https://github.com/hammadshakeelai/mcq-maker) — Reusable Claude Skill that turns any document into a high-quality MCQ quiz (interactive site + Word export).
- [**cli-chatbot**](https://github.com/hammadshakeelai/cli-chatbot) — Web terminal with agents, built for phones — a step toward web-based full computer systems.
- [**chatbot-like-claude**](https://github.com/hammadshakeelai/chatbot-like-claude) — Minimal, self-hostable Claude-style AI chat app with streaming replies and OpenAI-compatible models.
- [**food-suggestor**](https://github.com/hammadshakeelai/food-suggestor) — 🍽️ Pink Plate (Agnes AI): a mobile-first AI recipe chatbot, zero deps, Vercel-ready.
- [**ClaudeSessionScheduler**](https://github.com/hammadshakeelai/ClaudeSessionScheduler) — Fast, offline, single-file planner for sleep, life, and up to 10 Claude sessions per reset cycle.

### Scientific Simulation & Visualization
- [**RetinoTwin**](https://github.com/hammadshakeelai/RetinoTwin) — Synthetic retinoblastoma digital-twin & multimodal imaging simulator using real volumetric MRI from the MNI152 eye atlas.
- [**Nano-Swarm-Intelligence-Coronary-Clot-Simulator**](https://github.com/hammadshakeelai/Nano-Swarm-Intelligence-Coronary-Clot-Simulator) — Swarm-intelligence simulation of nanobots clearing coronary clots.
- [**LSTM-visualized**](https://github.com/hammadshakeelai/LSTM-visualized) — Interactive visualization of LSTM internals.
- [**TOP-10-NLP-ALGORITHMS-SIMULATORS**](https://github.com/hammadshakeelai/TOP-10-NLP-ALGORITHMS-SIMULATORS) — Simulators for the top 10 NLP algorithms.

### Apps & Systems
- [**Game-Database-Project**](https://github.com/hammadshakeelai/Game-Database-Project) — A game built to be deployed and appified.
- [**Software-Engineering-Project--UTOS**](https://github.com/hammadshakeelai/Software-Engineering-Project--UTOS) — University timetabling & scheduling website.
- [**GPA-Calculator-Adanced-Project-IMS**](https://github.com/hammadshakeelai/GPA-Calculator-Adanced-Project-IMS) — Fast public/private GPA calculator with presets.
- [**Mafia-Host-Tool**](https://github.com/hammadshakeelai/Mafia-Host-Tool) — Web tool that distributes Mafia roles between players.

> Explore the full set at [github.com/hammadshakeelai](https://github.com/hammadshakeelai?tab=repositories).
