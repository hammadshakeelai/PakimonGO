You are entering the PakimonGO repository. Read this entire prompt before doing anything else.

## ⚠️ CRITICAL: Read This First

This app is a **working prototype** — not production-ready. It uses dev-only providers (FakeAuthAdapter, DummyVisionProvider, SQLite). Real security and scoring are NOT active. **Read `docs/REMAINING_WORK.md` before proposing or building any feature.**

## Immediate Steps

1. Read `CLAUDE.md` — the grounded context file with all file paths, class names, function signatures, test commands, and critical rules.
2. Read `docs/REMAINING_WORK.md` — honest breakdown of what's left before this app is shippable.
3. Read `AGENTS.md` — the mandatory pre/post-task checklist (required before every edit).
4. Read `docs/CURRENT_TASK.md` — current phase and what's actively being worked on.
5. Read `docs/NEXT_TASK.md` — what comes next.

## One-Sentence Summary

Full-stack wildlife discovery app: Flutter mobile (10 screens, 125 tests) + FastAPI backend (15 endpoints, 103 tests) + shared scoring-rules package (61 tests) = 289 total tests, all passing. Code is complete as a prototype. Production-hardening needs an estimated 22-32 days of work across 15 tasks.

## State of the Project

- **46 sprints completed. 92 commits.**
- **Code is DONE.** No more features need to be written.
- **All that's left is OPS:** Get API keys, create cloud accounts, deploy.
- The app runs locally right now with `.\run_local.ps1` using SQLite + fake auth + dummy AI.
- Two seed users: `seed_user_alpha` and `seed_user_beta`. Login token: `test_user_seed_user_alpha`.

## Architecture At A Glance

```
Flutter App (10 screens)
    │ HTTP (ApiClient)
    ▼
FastAPI (5 modules, 15 endpoints)
    │ SQLAlchemy
    ├── SQLite (dev) / PostgreSQL (prod)
    ├── LocalFileStorage (dev) / S3 or GCS (prod)
    ├── FakeAuthAdapter (dev) / Firebase (prod)
    └── DummyVisionProvider (dev) / Google Vision (prod)
        │
        ▼
packages/scoring-rules/ (shared: state machine, precheck, scoring, vision adapter)
```

## Key Files To Read First

| File | Why |
|------|-----|
| `CLAUDE.md` | Complete grounded context with file:line references |
| `AGENTS.md` | Required workflow checklist |
| `services/api/src/main.py` | App entrypoint, middleware stack, router registration |
| `apps/mobile/pakimon_go_app/lib/main.dart` | Flutter app root, auth gate, tab navigation |
| `docs/NEXT_TASK.md` | Exactly what needs to happen next |

## What NOT To Do

- **Do NOT propose or write new features** without reading `docs/REMAINING_WORK.md` first. The app needs hardening, not expansion.
- Do NOT assume the app is production-ready because 291 tests pass. All auth, AI, storage, and DB are dev-only stubs.
- Do NOT modify API routes, DB models, or Flutter screens without reading `CLAUDE.md` first.
- Do NOT skip the pre-task check (`python tools/qa/pre_task_check.py`).
- Do NOT commit without running all 3 validation scripts.
- Do NOT modify files in `docs/adr/` unless an architecture decision changes.

## Your First Actions

1. Read `CLAUDE.md` fully.
2. Run `python tools/qa/pre_task_check.py` to confirm the repo is in a valid state.
3. Run `python -m pytest services/api/tests/ -q` to see 103 passing API tests.
4. Run `flutter test` in `apps/mobile/pakimon_go_app/` to see 125 passing Flutter tests.
5. Read `docs/NEXT_TASK.md` to understand what the user needs next.

After that, you're ready to help with whatever the user asks.
