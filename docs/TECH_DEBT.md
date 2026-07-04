# Technical Debt Register

## Current Known Debt

All 46 sprints complete. 291 tests pass. Current debt items:

## Implementation Debt

- API versioning uses middleware but no v2 routes exist yet (placeholder only)
- Storage uses local filesystem; needs cloud storage migration (S3/GCS) for production
- VisionProvider configured for Google but no real API key/environment tested (activates via VISION_PROVIDER=google + GOOGLE_VISION_API_KEY)
- Firebase auth backend adapter built (AUTH_PROVIDER=firebase) but not activated: needs firebase-admin installed, GOOGLE_APPLICATION_CREDENTIALS, google-services.json, and Flutter sign-in wiring
- Mapbox wired for local dev (--dart-define + gradle.properties download token); production token/CI injection still needed
- Database uses SQLite for dev; PostgreSQL connection string not wired to production DB
- APK optimized (R8 minify + shrinkResources + split-per-ABI, arm64 39.8MB). R8 logs benign com.mapbox.common ClassNotFound warnings at startup; verify map renders on a physical arm64 release build (emulator x86_64 can't fully confirm Mapbox native)
- No iOS build tested
- Submission rate limiting uses a single-instance DB-query cooldown; a multi-instance deployment needs a shared limiter (e.g. Redis) — NFR-SEC-004

## Decision Debt

- Scoring point ranges and economy formulas intentionally undefined until product review
- Moderation staffing/tooling undefined
- Species rarity taxonomy needs formal source of truth
- GitHub CODEOWNERS uses placeholder teams
- Branch protection not enabled in GitHub repository settings
- adb not on PATH (at SDK path: AppData/Local/Android/sdk/platform-tools)
- Full conversation export not pasted to raw archive; only summaries exist

## Future Debt Controls

- Files should usually stay near 200-300 lines. If a file grows larger, split by responsibility or document why not.
- Every module needs a local README or module overview once it becomes non-trivial.
- Every shortcut must be logged here with owner, reason, and removal condition.
- No generated code should be hand-edited unless the generator workflow is documented.
- Any temporary scoring or moderation rule must include an expiry review date.

## Debt Entry Template

```md
## TD-000: Title

- Area:
- Introduced:
- Reason:
- Risk:
- Removal plan:
- Owner:
- Review date:
```
