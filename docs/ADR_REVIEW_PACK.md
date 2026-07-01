# ADR Review Pack

## Purpose

This file records the ADR acceptance pass for ADR-001 through ADR-017 and captures what implementation work is now unlocked. Future ADRs should use the same checklist before production feature code depends on them.

## Review Checklist

For each ADR:

- Is the decision still compatible with `docs/SRS.md`?
- Are alternatives fairly represented?
- Is the internal challenge serious?
- Are consequences clear?
- Are reversal conditions concrete?
- Are requirement IDs and related docs referenced?
- Does the decision reduce future refactoring?
- Does it preserve privacy, security, and testability?

## ADR Status Board

| ADR | Topic | Current Status | Recommended Action | Blocking Before Code? |
|---|---|---|---|---|
| ADR-001 | Mobile platform | Accepted | Flutter is implementation baseline; validate camera/map/low-end performance in spikes. | Yes for mobile code |
| ADR-002 | Database and storage | Accepted | PostgreSQL/PostGIS/pgvector plus object storage is canonical data direction. | Yes for backend data code |
| ADR-003 | Map provider | Accepted (prototyping direction) | Mapbox-first prototyping accepted; final commitment after prototype cost/SDK/legal spike (Sprint 12+). | Yes for map implementation |
| ADR-004 | AI scoring pipeline | Accepted | Hybrid deterministic + structured AI evidence pipeline is baseline. | Yes for scoring code |
| ADR-005 | Location privacy | Accepted | Exact private coordinates and privacy-safe public outputs are mandatory. | Yes |
| ADR-006 | Auth platform | Accepted | Firebase Auth behind adapter is baseline. | Yes for auth code |
| ADR-007 | Backend framework | Accepted | FastAPI-style modular monolith is baseline. | Yes for API code |
| ADR-008 | Moderation and UGC safety | Accepted | Full public social stays gated by safety/moderation readiness. | Yes for social code |
| ADR-009 | Retention/deletion/export | Revised | Minimized-retention posture accepted; exact retention periods deferred. | Yes for deletion/export |
| ADR-010 | Age and minor policy | Accepted | 13+ launch and no under-13 accounts are baseline. | Yes |
| ADR-011 | Sensitive species policy | Accepted | Sensitive species suppression/coarsening policy is required. | Yes for map/rank exposure |
| ADR-012 | AI data sharing | Accepted | Minimized structured AI context is baseline. | Yes for AI provider calls |
| ADR-013 | Observability and reliability | Accepted | Trace/log/metric/health patterns start with first runnable backend. | Yes for deployable services |
| ADR-014 | Analytics minimization | Accepted | Minimal analytics tied to safety, reliability, cost, and success metrics. | No for initial scaffold |
| ADR-015 | Deployment platform | Accepted (alpha/beta direction) | Google Cloud/Firebase-first accepted: Cloud Run, Cloud SQL, Cloud Storage, Firebase Auth. Detailed architecture during beta prep. | No for local contracts |
| ADR-016 | Release process | Accepted | Ring-based release is baseline. | Yes for alpha planning |
| ADR-017 | Test tooling standards | Accepted | pytest/FastAPI and Flutter testing defaults are baseline for Sprint 0. | Yes for scaffold tests |

## ADR Review: 2026-07-01

- Reviewer: Codex GPT-5, acting on user approval to complete the pre-code locks.
- ADRs reviewed: ADR-001 through ADR-017.
- Accepted: ADR-001, ADR-002, ADR-003, ADR-004, ADR-005, ADR-006, ADR-007, ADR-008, ADR-010, ADR-011, ADR-012, ADR-013, ADR-014, ADR-015, ADR-016, ADR-017.
- Revised: ADR-009, with minimized-retention posture accepted and exact retention windows deferred.
- Deferred: none remaining.
- Rejected: none.
- New ADRs required: scoring formula version policy, migration tooling, final deployment region/budget during beta prep.
- Implementation unlocked: All 17 ADRs now accepted or revised. No ADR blockers remain for feature development.
- Remaining blockers: map provider still needs prototype spike before final UX commitment; production deployment needs cloud project setup during beta prep.

## Decision Meeting Output Template

```md
## ADR Review: YYYY-MM-DD

- Reviewer:
- ADRs reviewed:
- Accepted:
- Revised:
- Deferred:
- Rejected:
- New ADRs required:
- Implementation unlocked:
- Remaining blockers:
```
