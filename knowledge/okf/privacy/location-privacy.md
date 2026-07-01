---
id: location-privacy
type: privacy_rule
title: Location Privacy
status: accepted
updated: 2026-07-01
source_docs:
  - docs/SECURITY_PRIVACY_PLAN.md
  - docs/ARCHITECTURE.md
  - docs/adr/ADR-005-location-privacy.md
related:
  - requirements-core
  - system-architecture
---

# Location Privacy

## Summary

PakimonGO stores exact capture coordinates privately but exposes only privacy-safe public map data by default.

## Public Map Rules

- Use clusters, cells, fuzzed points, or delayed display.
- Avoid exact pins for homes, schools, rare animals, or sensitive locations.
- Query by viewport; never send global raw sightings.
- Local leaderboards use regions, not raw coordinates.

## Capture Rules

- Use foreground location only for MVP.
- Request precise location only when needed.
- Respect GPS uncertainty.
- Treat mock/spoof indicators as risk evidence.

## Zoo Rules

- Geofence zoos, aquariums, petting zoos, safari parks, sanctuaries, and exhibits.
- If capture overlaps a zoo boundary by GPS uncertainty, mark uncertain or review instead of automatic penalty.

## Decision State

ADR-005 is accepted. Exact coordinates are private; public map output must be cell/cluster/delay/fuzz/suppression based.
