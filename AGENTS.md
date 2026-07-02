# Repository Guidelines

## MANDATORY TASK LOOP — DO NOT SKIP

Every work burst follows this exact sequence. If you skip a step, the session log will show it.

### PRE-TASK (before any code/docs change)

```txt
[STEP 1] RUN: python tools/qa/pre_task_check.py
         → If FAIL: stop and fix before proceeding

[STEP 2] READ: docs/CURRENT_TASK.md, docs/NEXT_TASK.md, docs/CURRENT_THINKING.md
         → Confirm phase and active task match what you're about to do

[STEP 3] READ: The exact sprint packet for this task
         → Confirm file ownership, forbidden paths, acceptance criteria

[STEP 4] READ: docs/TRACEABILITY_MATRIX.md for the FR IDs in the task packet
         → If trace row missing: stop, add it before code

[STEP 5] DO THE WORK — short burst, small files (≤300 lines)
```

### POST-TASK (before ending burst or committing)

```txt
[STEP 6] RUN: python tools/qa/validate_docs.py
         RUN: python tools/qa/validate_json_examples.py
         RUN: python tools/qa/scan_secrets.py
         → If any FAIL: fix before commit

[STEP 7] UPDATE all state docs:
           - docs/CURRENT_TASK.md
           - docs/NEXT_TASK.md
           - docs/CURRENT_THINKING.md
           - docs/TASK_LOG.md
           - docs/BACKLOG.md
           - docs/BUGS_AND_RISKS.md
           - docs/TECH_DEBT.md
           - docs/sprints/SPRINT_0_PLAN.md (if sprint status changed)

[STEP 8] If architecture/requirement decision changed:
           - Update affected ADR in docs/adr/
           - Update affected OKF in knowledge/okf/

[STEP 9] COMMIT: semantic message + AI trailers
           AI-Agent, AI-Work-Mode, AI-Commit-Time
           Work-Package, Requirements, Process-Docs-Updated
```

## Verification Loop Rule

After every task marked complete, immediately:
1. Run pre_task_check.py again
2. Run all 3 validation scripts again
3. Update docs/SESSION_CHECKLIST.md with actual steps completed
4. Only then move to next task

## Mandatory Agent Workflow

Before meaningful work, read `docs/CURRENT_TASK.md`, `docs/NEXT_TASK.md`, `docs/CURRENT_THINKING.md`, `docs/PROCESS.md`, and relevant requirements/ADRs. Update state docs before ending work: current task, next task, backlog, bugs/risks, and technical debt.

Do not start production code before the SRS and architecture decisions are accepted. For every major decision, record alternatives, internal challenge, consequences, and reversal conditions in `docs/adr/`.

Preserve conversation context. When a user prompt, AI answer, or decision changes product direction, implementation process, requirements, architecture, or risks, update `docs/conversation-archive/` with either the full visible conversation text or a concise summary. Never store secrets, hidden system/developer instructions, private photos, or exact sensitive locations.

Follow the Software Engineering methodology artifacts in `docs/software-engineering/`. New requirements must maintain the traceability chain: requirement -> use case -> domain concept -> design class/operation -> SSD -> operation contract -> test.

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

The local toolchain has been checked, but no runnable app/backend scaffold exists yet. When scaffolding begins, document exact commands here and in `README.md`. Expected future commands:

- `python tools\qa\validate_docs.py` to validate planning docs, OpenAPI parsing, links, Mermaid files, and file-size guardrails.
- `python tools\qa\validate_json_examples.py` to validate API examples and QA fixture JSON syntax.
- `python tools\qa\scan_secrets.py` to catch obvious committed secrets.
- `powershell -ExecutionPolicy Bypass -File tools\qa\check_toolchain.ps1` to recheck local toolchain readiness.
- `flutter pub get` to install mobile dependencies.
- `flutter test` to run mobile unit/widget tests.
- `flutter build apk` for Android test APKs.
- `flutter build appbundle` for Google Play release artifacts.
- Backend commands will be added after the backend framework ADR.
- `docs/api/OPENAPI_DRAFT.yaml` should be validated once an OpenAPI linter is added.

Avoid committing generated dependency folders such as `node_modules/`, virtual environments, or build outputs.

## Coding Style & Naming Conventions

Use feature-first modules and small public interfaces. Reference durable context in comments when helpful, for example `// REQ FR-SCORE-003, ADR-004`.

Flutter/Dart code should follow Dart formatting. Backend style will be defined with its framework. Avoid comments that restate syntax.

## Testing Guidelines

Tests should live near the module or in that app/service test folder. Required test areas include scoring rules, duplicate detection, zoo/geofence detection, privacy transforms, auth, upload, map queries, and moderation flows.

Every feature needs requirement IDs, acceptance criteria, automated tests where practical, and documented manual verification for camera/map/device behavior.

Before code, read `docs/qa/README.md`, `docs/qa/REQUIREMENT_TO_TEST_MATRIX.md`, `docs/qa/TEST_CASE_CATALOGUE.md`, `docs/qa/LOCAL_PR_CHECKLIST.md`, and the relevant focused spec. Public API work must satisfy `docs/qa/PRIVACY_CONTRACT_TEST_SPEC.md`; scoring work must satisfy `docs/qa/SCORING_STATE_TEST_SPEC.md`; Android APK work must satisfy `docs/qa/MANUAL_ANDROID_QA_CHECKLIST.md`.

Respect `.github/CODEOWNERS` boundaries even before GitHub branch protection exists. Use `.github/PULL_REQUEST_TEMPLATE.md` and issue templates for future PR/issue drafting.

## Commit & Pull Request Guidelines

Use short, imperative commit subjects, for example `Add capture draft model` or `Define zoo scoring rules`.

Pull requests should include summary, requirement IDs, tests, screenshots/recordings for UI, privacy/security notes, and state-doc updates. Keep PRs focused.

Follow `docs/COMMIT_POLICY.md`: make short-burst semantic commits after stable mini-milestones, include requirement/work-package context, and add AI attribution trailers such as `AI-Agent`, `AI-Commit-Time`, and `Process-Docs-Updated` for AI-authored commits.

## Security & Configuration Tips

Never commit API keys, credentials, recovery codes, exact private datasets, or local `.env` files. Exact capture locations, photos, contacts, moderation logs, and AI evidence are sensitive. Score and leaderboard writes must stay server-authoritative.
