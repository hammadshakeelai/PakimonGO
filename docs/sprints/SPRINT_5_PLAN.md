# Sprint 5 Plan: User Registration/Onboarding

## Sprint Goal

Auto-create User rows on first authenticated request, expose GET/PATCH `/v1/users/me` endpoints for profile management.

## Sprint Status

**Complete.** All 3 tasks done and verified.

## Sprint Inputs

- Sprint 4 complete: real file upload + serving
- User model exists with id, status, age_band, home_region, trust_state
- Auth adapter returns UserContext with user_id, email

## In Scope

- User repository (get_or_create, update_user)
- GET `/v1/users/me` — returns profile, auto-creates if missing
- PATCH `/v1/users/me` — update age_band, home_region
- Tests for user endpoints

## Out Of Scope

- Email/display_name storage in User model (needs migration)
- Account deletion/export endpoints
- Admin user management
- Full onboarding flow (avatar, tutorials)

## Sprint Backlog

| ID | Status | Task | Acceptance | Verification |
|---|---|---|---|---|
| S5-001 | ✅ DONE | User repository | get_or_create, update_user functions | unit tests |
| S5-002 | ✅ DONE | GET /v1/users/me | Returns profile, auto-creates if missing | all tests pass |
| S5-003 | ✅ DONE | PATCH /v1/users/me | Updates age_band, home_region | all tests pass |

## Security

- Both endpoints require auth (inherited from Sprint 3)
- Users can only access their own profile (user_id from token)
