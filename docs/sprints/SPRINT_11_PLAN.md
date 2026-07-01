# Sprint 11 Plan: AI Provider Adapter Framework

## Sprint Goal

Build the AI provider adapter framework: VisionProvider protocol, AIScoringService, DummyVisionProvider, GoogleVisionProvider placeholder. Wire into the submission flow without committing API keys.

## Sprint Status

**Complete.** 112 total tests all passing. Ruff and mypy clean.

## Sprint Backlog

| ID | Status | Task | Acceptance | Verification |
|---|---|---|---|---|
| S11-001 | ✅ DONE | Define VisionProvider protocol + AnalysisResult + DummyVisionProvider | Protocol with analyze(), dataclass, and no-op stub | `packages/scoring-rules/src/vision_provider.py` |
| S11-002 | ✅ DONE | Create AIScoringService using VisionProvider + scoring rules | Uses provider for context when available, falls back to stub | AIScoringService in `scoring_service.py` |
| S11-003 | ✅ DONE | DummyVisionProvider for CI/testing | Always returns "Passer domesticus" / 0.95 / "wild" | `test_vision_provider.py` |
| S11-004 | ✅ DONE | GoogleVisionProvider placeholder with env-var config | Reads GOOGLE_VISION_API_KEY env var, raises NotImplementedError | `google_vision_provider.py` |
| S11-005 | ✅ DONE | Wire AIScoringService into submission routes | DummyVisionProvider by default; VISION_PROVIDER=google switches to GCP | Routes use `AIScoringService(vision_provider=_VISION_IMPL)` |
| S11-006 | ✅ DONE | Update tests — 11 new (5 vision_provider + 6 AIScoringService) | All pass | 43 scoring-rules + 54 API + 1 worker = 112 total |

## Key Architecture Decisions

- `ScoringService.evaluate()` gains optional `media_path: str | None` parameter — backward compatible
- `AIScoringService` delegates capped paths (zoo, pet, duplicate) to `StubScoringService` fallback
- Vision provider protocol uses duck typing (no trait/Protocol import at use site) to keep sys.path-based imports working
- `VISION_PROVIDER` env var controls which provider loads: `dummy` (default) or `google`/`gcp`
- GoogleVisionProvider requires `GOOGLE_VISION_API_KEY` env var; raises ValueError if missing at init

## File Ownership

| Area | Owner |
|---|---|
| `packages/scoring-rules/src/vision_provider.py` | Scoring-rules package |
| `packages/scoring-rules/src/google_vision_provider.py` | Scoring-rules package |
| `packages/scoring-rules/src/scoring_service.py` | Scoring-rules package |
| `packages/scoring-rules/tests/test_scoring_service.py` | Scoring-rules tests |
| `packages/scoring-rules/tests/test_vision_provider.py` | Scoring-rules tests |
| `services/api/src/modules/submissions/api/routes.py` | API routes |
| `services/api/tests/test_submission.py` | API tests (unchanged) |
