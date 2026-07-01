# Sprint 10 Plan: Deferred ADR Review

## Sprint Goal

Review and resolve the two deferred ADRs: ADR-003 (map provider) and ADR-015 (deployment platform). Both have clear provisional directions that are ready to accept.

## Sprint Status

**Complete.** Both ADRs accepted.

## Sprint Inputs

- ADR-003: Mapbox-first prototyping direction. Deferred since pre-code.
- ADR-015: Google Cloud/Firebase-first alpha direction. Deferred since pre-code.
- No new technical information has emerged to challenge either direction.
- Both serve as planning directions, not final commitments.

## ADR Review

### ADR-003 — Map Provider

**Resolution: Accepted (prototyping direction).** Mapbox-first for prototyping is confirmed. Google Maps Platform retained as challenger. Final commitment depends on prototype results (cost, Flutter SDK performance, legal review). A map prototype spike should be planned for Sprint 12+ once the API and scoring pipeline are stable.

### ADR-015 — Deployment Platform

**Resolution: Accepted (alpha/beta direction).** Google Cloud/Firebase-first is confirmed: Cloud Run for API/workers, Cloud SQL PostgreSQL (pgvector), Cloud Storage, Firebase Auth/App Check. Local Docker Compose + SQLite remains the development standard. Cloud deployment is not needed until beta testing. Detailed architecture (tier, region, budget) will be finalized during beta preparation.

## Outcome

All 17 ADRs are now accepted or revised (ADR-009). Zero deferred ADRs remain. No ADR blockers for feature development.

## Sprint Backlog

| ID | Status | Task | Acceptance | Verification |
|---|---|---|---|---|---|
| S10-001 | ✅ DONE | Review ADR-003 | Accept Mapbox-first for prototyping | ADR-003 status updated |
| S10-002 | ✅ DONE | Review ADR-015 | Accept Google Cloud/Firebase-first for alpha/beta | ADR-015 status updated |
| S10-003 | ✅ DONE | Update ADR review pack | All 17 ADRs accepted/revised; zero deferred | ADR_REVIEW_PACK.md updated |

## File Ownership

| Area | Owner |
|---|---|
| `docs/adr/ADR-003-map-provider.md` | Lead agent |
| `docs/adr/ADR-015-deployment-platform.md` | Lead agent |
| `docs/ADR_REVIEW_PACK.md` | Lead agent |
