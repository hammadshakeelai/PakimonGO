---
id: system-architecture
type: architecture_summary
title: System Architecture
status: reviewed
updated: 2026-07-01
source_docs:
  - docs/ARCHITECTURE.md
  - docs/REPO_STRUCTURE.md
related:
  - requirements-core
  - scoring-pipeline
  - location-privacy
---

# System Architecture

## Summary

PakimonGO is server-authoritative. The Flutter app captures evidence and displays experiences. Backend services own scoring, moderation, privacy, leaderboards, and trust decisions. Core architecture ADRs are accepted enough to start Sprint 0 scaffold work.

## Main Components

- Flutter mobile app.
- Backend API.
- Async worker pipeline.
- PostgreSQL with PostGIS and pgvector.
- Object storage for media.
- Firebase Auth/App Check.
- AI vision/scoring adapters.
- Moderation/admin tools.

## Key Boundaries

- Mobile never writes final score.
- Media originals stay private.
- Public map data is fuzzed or clustered.
- AI provider details do not leak into core domain models.
- Map provider SDK types do not leak into backend contracts.

## Deferred Boundaries

- Final map provider choice waits for the Mapbox vs Google spike.
- Final production deployment approval waits for cloud project, budget, region, and compliance review.
