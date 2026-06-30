# Services

Backend deployables live here.

- `api/`: modular HTTP API, planned as a FastAPI-style modular monolith unless ADR changes it.
- `workers/`: async jobs for media processing, evidence extraction, scoring, moderation, privacy transforms, and leaderboards.

Service code should depend on shared contracts and domain rule packages where practical, but PostgreSQL remains the canonical product data store.
