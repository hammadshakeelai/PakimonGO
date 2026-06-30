# Repository Guidelines

## Mandatory Agent Workflow

Before meaningful work, read `docs/CURRENT_TASK.md`, `docs/NEXT_TASK.md`, `docs/CURRENT_THINKING.md`, `docs/PROCESS.md`, and relevant requirements/ADRs. Update state docs before ending work: current task, next task, backlog, bugs/risks, and technical debt.

Do not start production code before the SRS and architecture decisions are accepted. For every major decision, record alternatives, internal challenge, consequences, and reversal conditions in `docs/adr/`.

Preserve conversation context. When a user prompt, AI answer, or decision changes product direction, implementation process, requirements, architecture, or risks, update `docs/conversation-archive/` with either the full visible conversation text or a concise summary. Never store secrets, hidden system/developer instructions, private photos, or exact sensitive locations.

## Project Structure & Module Organization

This is planned as a large modular monorepo. Target layout:

- `apps/mobile/` for the Flutter app.
- `services/api/` and `services/workers/` for backend modules and async jobs.
- `packages/` for shared contracts, scoring rules, taxonomy, geo, and moderation logic.
- `infrastructure/` for database, Firebase, Docker, and deployment assets.
- `data/goldsets/` for AI, duplicate, zoo, and scoring test datasets.
- `docs/` for SRS, ADRs, process, QA, security, backlog, and task state.
- `knowledge/okf/` for compact agent-readable project knowledge.

Keep source files usually around 200-300 lines. Split by feature/domain before files become hard to test or hand off.

## Build, Test, and Development Commands

No app tooling is installed yet. When scaffolding begins, document exact commands here and in `README.md`. Expected future commands:

- `flutter pub get` to install mobile dependencies.
- `flutter test` to run mobile unit/widget tests.
- `flutter build apk` for Android test APKs.
- `flutter build appbundle` for Google Play release artifacts.
- Backend commands will be added after the backend framework ADR.

Avoid committing generated dependency folders such as `node_modules/`, virtual environments, or build outputs.

## Coding Style & Naming Conventions

Use feature-first modules and small public interfaces. Reference durable context in comments when helpful, for example `// REQ FR-SCORE-003, ADR-004`.

Flutter/Dart code should follow Dart formatting. Backend style will be defined with its framework. Avoid comments that restate syntax.

## Testing Guidelines

Tests should live near the module or in that app/service test folder. Required test areas include scoring rules, duplicate detection, zoo/geofence detection, privacy transforms, auth, upload, map queries, and moderation flows.

Every feature needs requirement IDs, acceptance criteria, automated tests where practical, and documented manual verification for camera/map/device behavior.

## Commit & Pull Request Guidelines

Use short, imperative commit subjects, for example `Add capture draft model` or `Define zoo scoring rules`.

Pull requests should include summary, requirement IDs, tests, screenshots/recordings for UI, privacy/security notes, and state-doc updates. Keep PRs focused.

Follow `docs/COMMIT_POLICY.md`: make short-burst semantic commits after stable mini-milestones, include requirement/work-package context, and add AI attribution trailers such as `AI-Agent`, `AI-Commit-Time`, and `Process-Docs-Updated` for AI-authored commits.

## Security & Configuration Tips

Never commit API keys, credentials, recovery codes, exact private datasets, or local `.env` files. Exact capture locations, photos, contacts, moderation logs, and AI evidence are sensitive. Score and leaderboard writes must stay server-authoritative.
