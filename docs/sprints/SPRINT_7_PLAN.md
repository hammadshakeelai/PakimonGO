# Sprint 7 Plan: OpenAPI Draft Update

## Sprint Goal

Refresh the OpenAPI draft and API examples to match all Sprint 1-6 implemented endpoints. Mark planned-but-not-implemented endpoints with `x-status: planned`.

## Sprint Status

**Complete.** All 3 tasks done and verified.

## Sprint Inputs

- Existing OPENAPI_DRAFT.yaml: 13 paths, 22 schemas (all stale, pre-Sprint 1)
- Real API surface from routers: health, media (upload-intent, upload, complete, derivatives, files), submissions (create, get), users (GET/PATCH /me)
- API examples in `docs/api/examples/`

## In Scope

- Rewrite OPENAPI_DRAFT.yaml to match all implemented endpoints
- Mark future endpoints with `x-status: planned`
- Update API examples to match current response shapes
- Add missing examples: health, upload response, complete-upload response, derivative response, user profile, patch request

## Out Of Scope

- CI expansion
- AI scoring pipeline
- Schema generation from code (still hand-maintained)

## Sprint Backlog

| ID | Status | Task | Acceptance | Verification |
|---|---|---|---|---|---|
| S7-001 | ✅ DONE | Inventory all real endpoints | Route-by-route list of all 11 real endpoints + 8 planned | manual review |
| S7-002 | ✅ DONE | Rewrite OPENAPI_DRAFT.yaml | 18 paths, 23 schemas, health/media/submissions/users all up to date | validate_docs.py PASS |
| S7-003 | ✅ DONE | Update API examples | 10 existing examples fixed + 4 new (health, upload, complete, derivative, user) | validate_json_examples.py PASS |

## File Ownership

| Area | Owner |
|---|---|
| `docs/api/OPENAPI_DRAFT.yaml` | Lead agent |
| `docs/api/examples/` | Lead agent |

## Security

- No new endpoints added — existing security model unchanged
- Bearer auth on all protected endpoints correctly documented
