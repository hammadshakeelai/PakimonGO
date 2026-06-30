# Alpha-0 Vertical Slice

## Purpose

Define the first implementation path after scaffold readiness. This is not full PakimonGO; it is the smallest end-to-end slice that proves the architecture without exposing risky social/global features.

## Work Package

### WP-015: Alpha-0 Private Capture Slice

- Goal: prove onboarding, auth shell, camera draft, signed upload contract, private collection placeholder, pending score state, duplicate/zoo precheck placeholders, and privacy-safe state transitions.
- Owner type: mobile/backend pair.
- Dependencies: ADR-001 through ADR-016 reviewed; API contract approach accepted.
- Commit cadence: short-burst semantic commits per module boundary.

## Included Requirements

- `FR-AUTH-001` through `FR-AUTH-003`
- `FR-AGE-001` through `FR-AGE-003`
- `FR-ONB-001` through `FR-ONB-005`
- `FR-PERM-001` through `FR-PERM-007`
- `FR-CAP-001` through `FR-CAP-017`
- `FR-SCORE-002`, `FR-SCORE-003`, `FR-SCORE-008`
- `FR-DUP-001`, `FR-DUP-006`
- `FR-ZOO-001`, `FR-ZOO-003`
- `FR-COL-001` through `FR-COL-003`
- `FR-MAP-003`, `FR-MAP-004`
- `NFR-SEC-001` through `NFR-SEC-005`
- `NFR-PRIV-001` through `NFR-PRIV-004`
- `NFR-MAINT-001` through `NFR-MAINT-003`

## Explicitly Excluded

- Public feed.
- Public comments.
- Reposts.
- Groups.
- Contacts import.
- Global/country/local public leaderboards.
- Background location.
- Exact public animal pins.
- Real-money or ad features.

## Planned Short-Burst Commits

1. `scaffold(mobile): add Flutter project shell`
2. `scaffold(api): add API project shell`
3. `docs(contract): add submission upload OpenAPI draft`
4. `feat(auth): add auth adapter interfaces`
5. `feat(capture): add local capture draft model`
6. `feat(media): add signed upload contract`
7. `feat(submissions): add pending submission state`
8. `feat(scoring): add score state enum`
9. `feat(geo): add privacy cell placeholder`
10. `test(capture): cover draft lifecycle`

Each AI-authored commit must include the trailers defined in `docs/COMMIT_POLICY.md`.

## Acceptance Criteria

- App can start locally after Flutter scaffold exists.
- User can pass 13+ gate and reach auth shell.
- User can create a local capture draft after camera scaffold exists.
- Draft metadata can be represented without final upload.
- API contract can represent signed upload request, upload completion, and pending submission.
- Server-side state model can represent pending/prechecked/scored/review/rejected without client final scoring.
- Private collection placeholder can list pending local/server submissions.
- No exact public location appears in any public contract.
- No production secrets are present in repo.

## Test Plan

- Unit tests for capture draft lifecycle.
- Contract tests for upload and submission payloads.
- Privacy tests asserting public DTOs omit exact coordinates.
- State-machine tests for scoring status transitions.
- Manual device tests later for camera and permission behavior.

## Security And Privacy Notes

- Exact location, EXIF, originals, and signed URLs are restricted.
- Auth must be verified server-side before real upload/scoring endpoints.
- App Check/attestation enforcement can start in monitor mode during early local development but must be enforced before alpha scoring exposure.
- No public derivatives are created until media validation and EXIF stripping are implemented.

## Rollback Plan

Because this is the first vertical slice, rollback means disabling feature flags or reverting the affected short-burst commit. Database migrations must include rollback notes once migrations exist.

## Handoff Notes

Next agent should choose whether to scaffold actual Flutter/FastAPI toolchains first or draft OpenAPI/contracts first. Do not implement social/global features in this slice.
