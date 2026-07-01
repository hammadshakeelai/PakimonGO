---
id: adr-summary
type: decision_summary
title: Architecture Decision Summary
status: reviewed
updated: 2026-07-01
source_docs:
  - docs/DECISION_LOG.md
  - docs/ADR_REVIEW_PACK.md
  - docs/adr/
related:
  - system-architecture
  - requirements-core
---

# Architecture Decision Summary

## Accepted

- ADR-001: Flutter mobile platform.
- ADR-002: PostgreSQL/PostGIS/pgvector plus object storage, with Firebase services where useful.
- ADR-004: Hybrid server-side AI evidence pipeline.
- ADR-005: Private exact coordinates with privacy-safe public map aggregation.
- ADR-006: Firebase Authentication behind an adapter.
- ADR-007: FastAPI-style modular monolith.
- ADR-008: Gated social exposure with moderation and safety controls.
- ADR-010: 13+ launch, no under-13 accounts until family mode exists.
- ADR-011: Sensitive species suppression/coarsening/delay/review policy.
- ADR-012: Minimized, purpose-bound AI data sharing.
- ADR-013: Observability and reliability from first runnable backend.
- ADR-014: Minimal analytics.
- ADR-016: Ring-based release process.

## Revised

- ADR-009: Minimized retention accepted; exact retention periods deferred pending legal/privacy review.

## Deferred

- ADR-003: final map provider; Mapbox-first prototype remains the accepted spike direction.
- ADR-015: final production deployment approval; Google Cloud/Firebase-first remains alpha planning direction.

## Handoff Notes

Sprint 0 may begin with toolchain, contracts, health endpoints, privacy DTO tests, and score/capture model shells. Do not implement final map-provider-specific features, production deployment, exact retention workflows, or final scoring formula yet.
