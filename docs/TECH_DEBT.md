# Technical Debt Register

## Current Known Debt

All 49 sprints complete. 289 tests pass. Current debt items:

## Implementation Debt

- API versioning uses middleware but no v2 routes exist yet (placeholder only)
- Storage uses local filesystem; needs cloud storage migration (S3/GCS) for production
- VisionProvider configured for Google but no real API key/environment tested
- Mapbox wired for local dev (--dart-define + gradle.properties download token); production token/CI injection still needed
- Database uses SQLite for dev; PostgreSQL connection string not wired to production DB
- Release APK is 105.8MB — needs optimization (ProGuard, R8, asset compression)
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
