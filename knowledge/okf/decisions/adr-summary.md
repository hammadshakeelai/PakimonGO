---
id: adr-summary
type: decision_summary
title: Proposed Architecture Decisions
status: proposed
updated: 2026-07-01
source_docs:
  - docs/DECISION_LOG.md
  - docs/adr/ADR-001-mobile-platform.md
  - docs/adr/ADR-002-database-and-storage.md
  - docs/adr/ADR-003-map-provider.md
  - docs/adr/ADR-004-ai-scoring-pipeline.md
  - docs/adr/ADR-005-location-privacy.md
  - docs/adr/ADR-006-auth-platform.md
related:
  - system-architecture
  - requirements-core
---

# Proposed Architecture Decisions

## Summary

Current proposed decisions:

- Flutter for mobile.
- Firebase Auth/App Check/Storage plus PostgreSQL/PostGIS/pgvector.
- Mapbox-first map prototype with Google Maps as challenger.
- Hybrid server-side AI evidence pipeline.
- Private exact coordinates with privacy-safe public map aggregation.
- Firebase Authentication behind an adapter.

## Rule

These decisions are proposed, not final. Review SRS and ADRs before production scaffolding.
