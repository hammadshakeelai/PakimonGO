# Decision Log

## Proposed Decisions

### ADR-001: Mobile Platform

Proposed Flutter for Android-first and later iOS delivery, pending camera/map performance prototype.

### ADR-002: Database And Storage

Proposed hybrid Firebase plus PostgreSQL architecture: Firebase for Auth/App Check/Storage, PostgreSQL with PostGIS/pgvector for canonical product data.

### ADR-003: Map Provider

Proposed Mapbox-first prototype for a game-like map, with Google Maps Platform retained as challenger if POI/routing quality dominates.

### ADR-004: AI Scoring Pipeline

Proposed hybrid server-side evidence pipeline instead of single LLM-only scoring.

### ADR-005: Location Privacy

Proposed exact private coordinates with public clusters/cells/fuzzed/delayed display by default.

### ADR-006: Auth Platform

Proposed Firebase Authentication behind an adapter, with Apple sign-in planned for iOS if required.

### ADR-007: Backend Framework

Proposed FastAPI-style modular monolith for the initial API.

### ADR-008: Moderation And UGC Safety

Proposed gated social exposure with report, block, hide/delete, moderation queue, appeals, audit, and critical disable switches before public social launch.

### ADR-009: Retention, Deletion, And Export

Proposed minimized retention with deletion/anonymization/export workflows and restricted audit exceptions.

### ADR-010: Age And Minor Policy

Proposed 13+ launch with neutral age gate and no under-13 accounts until family mode exists.

### ADR-011: Sensitive Species Policy

Proposed sensitive species suppression/coarsening/delay/review controls for public maps and local rankings.

### ADR-012: AI Data Sharing

Proposed minimized, purpose-bound, structured AI context with deterministic checks outside the LLM.

### ADR-013: Observability And Reliability

Proposed trace IDs, structured logs, metrics, health endpoints, Crashlytics, and OpenTelemetry-compatible backend patterns from first runnable service.

### ADR-014: Analytics Minimization

Proposed minimal analytics tied to success metrics, safety, reliability, and cost.

### ADR-015: Deployment Platform

Proposed Google Cloud/Firebase-first deployment path for alpha planning.

### ADR-016: Release Process

Proposed ring-based release from local/staging through internal APK, Play testing, Android production, TestFlight, and iOS production.

## Decision Rules

- Proposed decisions become accepted only after SRS/architecture review.
- Any agent may challenge a proposed decision by adding evidence and updating the relevant ADR.
- Reversal conditions must stay explicit.
