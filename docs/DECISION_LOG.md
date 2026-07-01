# Decision Log

## Accepted And Reviewed Decisions

### ADR-001: Mobile Platform

Accepted Flutter for Android-first and later iOS delivery, with camera/map performance validated by spikes.

### ADR-002: Database And Storage

Accepted hybrid Firebase plus PostgreSQL architecture: Firebase for Auth/App Check/Storage, PostgreSQL with PostGIS/pgvector for canonical product data.

### ADR-003: Map Provider

Deferred final provider selection. Mapbox-first prototype remains the accepted spike direction, with Google Maps Platform retained as challenger.

### ADR-004: AI Scoring Pipeline

Accepted hybrid server-side evidence pipeline instead of single LLM-only scoring.

### ADR-005: Location Privacy

Accepted exact private coordinates with public clusters/cells/fuzzed/delayed display by default.

### ADR-006: Auth Platform

Accepted Firebase Authentication behind an adapter, with Apple sign-in planned for iOS if required.

### ADR-007: Backend Framework

Accepted FastAPI-style modular monolith for the initial API.

### ADR-008: Moderation And UGC Safety

Accepted gated social exposure with report, block, hide/delete, moderation queue, appeals, audit, and critical disable switches before public social launch.

### ADR-009: Retention, Deletion, And Export

Revised: minimized retention with deletion/anonymization/export workflows and restricted audit exceptions is accepted; exact retention periods remain deferred.

### ADR-010: Age And Minor Policy

Accepted 13+ launch with neutral age gate and no under-13 accounts until family mode exists.

### ADR-011: Sensitive Species Policy

Accepted sensitive species suppression/coarsening/delay/review controls for public maps and local rankings.

### ADR-012: AI Data Sharing

Accepted minimized, purpose-bound, structured AI context with deterministic checks outside the LLM.

### ADR-013: Observability And Reliability

Accepted trace IDs, structured logs, metrics, health endpoints, Crashlytics, and OpenTelemetry-compatible backend patterns from first runnable service.

### ADR-014: Analytics Minimization

Accepted minimal analytics tied to success metrics, safety, reliability, and cost.

### ADR-015: Deployment Platform

Deferred final production deployment approval. Google Cloud/Firebase-first remains accepted for alpha planning.

### ADR-016: Release Process

Accepted ring-based release from local/staging through internal APK, Play testing, Android production, TestFlight, and iOS production.

### ADR-017: Test Tooling Standards

Accepted pytest/httpx/pytest-asyncio/ruff/mypy/coverage.py for Python services, Flutter test/integration_test/mocktail for mobile, and lightweight local secret/JSON/docs validation until generated contract and dedicated security tooling exist.

## Decision Rules

- Accepted decisions may still have explicit reversal conditions in their ADRs.
- Any agent may challenge a proposed decision by adding evidence and updating the relevant ADR.
- Reversal conditions must stay explicit.
