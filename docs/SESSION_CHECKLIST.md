# Session Checklist

Update this after every work burst. Each row tracks one task cycle.

| # | Task | pre_task_check | State Docs Updated | Validation Pass | Commit Done | Notes |
|---|---|---|---|---|---|---|---|
| 1 | Create pre_task_check.py | ✅ PASS | ✅ | ✅ | ❌ no commit | New file, part of safeguard system |
| 2 | Fix SPRINT_0_PLAN.md drift | ✅ PASS | ✅ | ✅ | ❌ no commit | Marked S0-001–005 complete |
| 3 | Verify S0-001–005 completeness | ✅ PASS | ✅ TASK_LOG.md | ✅ ALL PASS | ❌ no commit | All 5 completed tasks verified clean |
| 4 | Update AGENTS.md + SESSION_CHECKLIST.md | ✅ PASS | ✅ CURRENT_THINKING.md, NEXT_TASK.md, TASK_LOG.md | ✅ ALL PASS | ❌ no commit | Safeguard system complete |
| 5 | Preparing for S0-006 | ✅ PASS | ✅ CURRENT_TASK.md | ✅ | ❌ pre-code read phase | Must read priv spec + traceability first |
| 6 | S0-006 public DTO privacy tests | ✅ PASS | ✅ ALL state docs | ✅ ALL PASS | ❌ no commit | 7 tests in services/api/tests/, all pass |
| 7 | S0-007 score state model | ✅ PASS | ✅ ALL state docs | ✅ ALL PASS | ❌ no commit | 18 pkg tests + 17 API tests, all pass |
| 8 | S0-008 capture draft model | ✅ PASS | ✅ ALL state docs | ✅ ALL PASS | ❌ no commit | 14 Flutter tests, all pass |
| 9 | S0-009 extend CI workflow | ✅ PASS | ✅ ALL state docs | ✅ ALL PASS | ❌ no commit | 5 jobs, all non-deploy |
| 10 | S0-010 Sprint 0 closeout | ✅ PASS | ✅ ALL state docs + conversation archive | ✅ ALL PASS | ❌ no commit | Sprint 0 complete — 59 tests, 4/4 validations |
| 11 | Sprint 1 plan + S1-001 upload intent | ✅ PASS | ✅ ALL state docs | ✅ ALL PASS | ❌ no commit | 9 tests, 2 endpoints, 45 total |
| 12 | S1-002 submission private DTO | ✅ PASS | ✅ ALL state docs | ✅ ALL PASS | ❌ no commit | 5 tests, 2 endpoints, pending state hook |
| 13 | S1-003 media derivative stubs | ✅ PASS | ✅ ALL state docs | ✅ ALL PASS | ❌ no commit | 5 tests, EXIF strip contract, CDN URLs |
| 14 | S1-004 CI extension | ✅ PASS | ✅ ALL state docs | ✅ ALL PASS | ❌ no commit | CI auto-covers 45 tests |
| 15 | S2-001/S2-002 DB models + wire DB | ✅ PASS | ✅ ALL state docs | ✅ ALL PASS | ❌ no commit | 45 API tests, SQLAlchemy + Alembic |
| 16 | Sprint 3 auth integration | ✅ PASS | ✅ ALL state docs | ✅ ALL PASS | ❌ no commit | 46 API tests, auth adapter pattern |
| 17 | Sprint 4 real upload handler | ✅ PASS | ✅ ALL state docs | ✅ ALL PASS | ❌ no commit | 47 API tests, LocalFileStorage, PUT upload |
| 18 | Sprint 5 user profiles | ✅ PASS | ✅ ALL state docs | ✅ ALL PASS | ❌ no commit | 52 API tests, GET/PATCH /v1/users/me |
| 19 | Sprint 6 duplicate/zoo precheck | ✅ PASS | ✅ ALL state docs + conversation archive | ✅ ALL PASS | ❌ no commit | 54 API + 26 scoring-rules = 95 total |
| 20 | Sprint 7 OpenAPI draft update | ✅ PASS | ✅ ALL state docs + conversation archive | ✅ ALL PASS | ❌ no commit | 18 paths, 23 schemas, 14 examples |
| 21 | Sprint 8 CI expansion | ✅ PASS | ✅ ALL state docs + conversation archive | ✅ ALL PASS | ❌ no commit | ruff 16→0, mypy 38→0, CI 5→7 jobs |
| 22 | Sprint 9 AI scoring pipeline stub | ✅ PASS | ✅ ALL state docs + conversation archive | ✅ ALL PASS | ❌ no commit | 101 total tests, scoring wired into submissions |
| 23 | Sprint 10 deferred ADR review | ✅ PASS | ✅ ALL state docs + conversation archive | ✅ ALL PASS | ❌ no commit | ADR-003 + ADR-015 accepted; zero deferred remain |
| 24 | Sprint 11 AI provider adapter framework | ✅ PASS | ✅ ALL state docs + conversation archive | ✅ ALL PASS | ❌ no commit | 112 total tests, AIScoringService wired |
| 25 | Sprint 12 async worker scoring | ✅ PASS | ✅ ALL state docs + conversation archive | ✅ ALL PASS | ❌ no commit | 112 tests, worker thread, async scoring |
| 26 | Sprint 13 map prototype spike | ✅ PASS | ✅ ALL state docs + conversation archive | ✅ ALL PASS | ❌ no commit | Mapbox SDK wired, MapScreen with fallback |
| 27 | Sprint 14 real Google Vision provider | ✅ PASS | ✅ ALL state docs + conversation archive | ✅ ALL PASS | ❌ no commit | Real REST API impl, 6 mock tests, 117 total |
| 28 | Sprint 15 collection/leaderboard endpoints | ✅ PASS | ✅ ALL state docs + conversation archive | ✅ ALL PASS | ❌ no commit | 7 tests, 61 API total, 2 new paths, 4 new schemas |
| 29 | Sprint 16 goldset integration | ✅ PASS | ✅ ALL state docs + conversation archive | ✅ ALL PASS | ❌ no commit | 2 manifests (18 scenarios), goldset_runner, 12 tests, CI job |
| 30 | Sprint 17 API pagination/filter/sort | ✅ PASS | ✅ ALL state docs + conversation archive | ✅ ALL PASS | ❌ no commit | 3 endpoints enhanced, 7 tests updated, 136 total tests |
| 31 | Sprint 18 OPENAPI_DRAFT.yaml update | ✅ PASS | ✅ ALL state docs + conversation archive | ✅ ALL PASS | ❌ no commit | 4 new schemas, 3 endpoints documented, 31 schemas total |
| 32 | Sprint 19 sensitive species suppression | ✅ PASS | ✅ ALL state docs + conversation archive | ✅ ALL PASS | ❌ no commit | SensitiveSpecies model, location suppression, 4 tests |
| 33 | Sprint 20 sensitive species filtering | ✅ PASS | ✅ ALL state docs + conversation archive | ✅ ALL PASS | ❌ no commit | Filtering in collection/leaderboard/submissions, 6 tests, 7 repo modules |
| 34 | Sprint 21 OPENAPI_DRAFT.yaml update | ✅ PASS | ✅ ALL state docs + conversation archive | ✅ ALL PASS | ❌ no commit | include_sensitive params, fixed duplicate path, 31 schemas |
| 35 | Sprint 22 API v1 prefix routing | ✅ PASS | ✅ ALL state docs + conversation archive | ✅ ALL PASS | ✅ COMMIT | /v1 prefix at app level, 4 module routers updated, internal paths fixed |
| 36 | Sprint 22 API version negotiation | ✅ PASS | ✅ ALL state docs | ✅ ALL PASS | ✅ COMMIT | Accept-Version header, API-Version response, 6 tests, 150 total tests |
| 37 | Sprint 23 corpus staging and commits | ✅ PASS | ✅ CURRENT_TASK.md, NEXT_TASK.md | ✅ ALL PASS | ✅ COMMIT | All Sprints 0-22 files committed, 150 tests verified |
| 38 | Sprint 23 complete + state docs | ✅ PASS | ✅ ALL state docs | ✅ ALL PASS | ✅ COMMIT | All files staged, TECH_DEBT updated, validations pass |
