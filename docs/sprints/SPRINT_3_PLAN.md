# Sprint 3 Plan: Auth Integration

## Sprint Goal

Wire Firebase Auth (via adapter pattern) into existing API endpoints. Users must be authenticated to create uploads, submissions, and access media. Health endpoints remain public.

## Sprint Status

**Complete.** All 3 tasks done and verified.

## Sprint Inputs

- ADR-006: Firebase Authentication behind an auth adapter
- FR-AUTH-001 through FR-AUTH-012
- Sprint 1 endpoints: upload-intent, complete-upload, derivatives, submissions
- User model exists with nullable owner_user_id (placeholder)

## In Scope

- Auth adapter interface + FakeAuthAdapter for dev/test
- `get_current_user` FastAPI dependency
- Protect media upload endpoints (POST /v1/media/upload-intent, POST /v1/media/complete-upload, GET /v1/media/derivatives/{id})
- Protect submission endpoints (POST /v1/submissions, GET /v1/submissions/{id})
- Health endpoints remain public
- Tests for auth success, missing token, invalid token

## Out Of Scope

- Real Firebase Admin SDK credentials in CI
- Mobile-side auth flows (Google sign-in, email/password)
- Account deletion/export endpoints
- App Check integration
- Firebase token refresh logic

## Sprint Backlog

| ID | Status | Task | Acceptance | Verification |
|---|---|---|---|---|
| S3-001 | ✅ DONE | Auth adapter + dependency | FakeAuthAdapter verifies tokens; get_current_user returns UserContext | tests pass |
| S3-002 | ✅ DONE | Protect media routes | All 3 media endpoints require auth | 401 without token, 200 with |
| S3-003 | ✅ DONE | Protect submission routes | Both submission endpoints require auth | 401 without token, 200 with |

## File Ownership

| Area | Owner |
|---|---|
| `services/api/src/infrastructure/auth/` | Backend agent |
| `services/api/src/modules/media/` | Backend agent |
| `services/api/src/modules/submissions/` | Backend agent |

## Security And Privacy Notes

- Auth adapter must never leak Firebase credentials
- Fake adapter for dev only — never in production
- User IDs flow into owner_user_id on media/assets

## Definition Of Done

- All Sprint 3 tasks complete
- All 45+ tests pass
- State docs updated
