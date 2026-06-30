# ADR Review Pack

## Purpose

Before production feature code, review ADR-001 through ADR-016 and mark each as Accepted, Revised, Deferred, or Rejected. Proposed ADRs are strong enough for planning but not final implementation authority until reviewed.

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
| ADR-001 | Mobile platform | Proposed | Accept after Flutter camera/map spike criteria are confirmed. | Yes for mobile code |
| ADR-002 | Database and storage | Proposed | Accept as canonical direction; validate Cloud SQL/PostGIS/pgvector local setup. | Yes for backend data code |
| ADR-003 | Map provider | Proposed | Keep proposed until Mapbox/Google spike. | Yes for map implementation |
| ADR-004 | AI scoring pipeline | Proposed | Accept hybrid architecture; defer exact provider mix. | Yes for scoring code |
| ADR-005 | Location privacy | Proposed | Accept before any map/feed API. | Yes |
| ADR-006 | Auth platform | Proposed | Accept Firebase Auth adapter direction. | Yes for auth code |
| ADR-007 | Backend framework | Proposed | Accept FastAPI unless user changes stack. | Yes for API code |
| ADR-008 | Moderation and UGC safety | Proposed | Accept gated social exposure. | Yes for social code |
| ADR-009 | Retention/deletion/export | Proposed | Revise with exact retention periods later. | Yes for deletion/export |
| ADR-010 | Age and minor policy | Proposed | Accept 13+ posture. | Yes |
| ADR-011 | Sensitive species policy | Proposed | Accept policy mechanism; source details later. | Yes for map/rank exposure |
| ADR-012 | AI data sharing | Proposed | Accept minimization. | Yes for AI provider calls |
| ADR-013 | Observability and reliability | Proposed | Accept from first runnable backend. | Yes for deployable services |
| ADR-014 | Analytics minimization | Proposed | Accept minimal analytics. | No for initial scaffold |
| ADR-015 | Deployment platform | Proposed | Keep proposed until cloud project exists. | No for local contracts |
| ADR-016 | Release process | Proposed | Accept ring-based release. | Yes for alpha planning |

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
