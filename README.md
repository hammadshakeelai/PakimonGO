# PakimonGO

PakimonGO is a planned 13+ mobile app for real-animal photography, discovery, collections, map exploration, privacy-safe social sharing, and server-scored competition.

This repository is currently in scaffold-plus-planning state. It contains the project process, expanded requirements, architecture direction, and a modular monorepo skeleton. It does not yet contain production feature implementation.

## Current Phase

Phase 5: repository scaffold and implementation readiness.

Before production coding starts, finish the SRS/ADR acceptance pass and define the first Alpha-0 vertical slice.

## Repository Layout

- `apps/mobile/pakimon_go_app/`: Flutter app home, organized by feature.
- `services/api/`: FastAPI-style modular monolith shell.
- `services/workers/`: async media, evidence, scoring, moderation, privacy, and leaderboard jobs.
- `packages/`: shared contracts and domain rule packages.
- `infrastructure/`: database, Firebase, Docker, Cloud Run, and IaC assets.
- `data/goldsets/`: duplicate, zoo, species, scoring, and sensitive-species benchmark datasets.
- `docs/`: SRS, requirements, process, decisions, risks, roadmap, and templates.
- `knowledge/`: OKF, Obsidian, and future Graphify/code-graph knowledge outputs.
- `tools/`: repo automation, graph export, QA, and utility scripts.

## Contributor Start

1. Read `AGENTS.md`.
2. Read `docs/CURRENT_TASK.md`.
3. Read `docs/NEXT_TASK.md`.
4. Read `docs/PROCESS.md`.
5. Read the relevant module README before editing.

## Planning And Design Artifacts

- Methodology-aligned SRS: `docs/SRS.md`
- Full requirement catalogue: `docs/REQUIREMENTS.md`
- Traceability matrix: `docs/TRACEABILITY_MATRIX.md`
- Software Engineering artifacts: `docs/software-engineering/`
- OpenAPI draft: `docs/api/OPENAPI_DRAFT.yaml`
- Database ERD: `docs/data/DATABASE_ERD.md`
- Data dictionary: `docs/data/DATA_DICTIONARY.md`
- Threat model: `docs/security/THREAT_MODEL.md`
- UX flow spec: `docs/ux/UX_FLOW_SPEC.md`
- Testing master plan: `docs/qa/TESTING_MASTER_PLAN.md`
- QA spec index: `docs/qa/README.md`
- Requirement-to-test matrix: `docs/qa/REQUIREMENT_TO_TEST_MATRIX.md`
- Test case catalogue: `docs/qa/TEST_CASE_CATALOGUE.md`
- BDD acceptance scenarios: `docs/qa/BDD_ACCEPTANCE_SCENARIOS.md`
- Sprint 0 test plan: `docs/qa/SPRINT_0_TEST_PLAN.md`
- Privacy contract test spec: `docs/qa/PRIVACY_CONTRACT_TEST_SPEC.md`
- Scoring state test spec: `docs/qa/SCORING_STATE_TEST_SPEC.md`
- Goldset governance and zoo/duplicate benchmarks: `docs/qa/GOLDSET_GOVERNANCE_PLAN.md`, `docs/qa/ZOO_DUPLICATE_BENCHMARK_SPEC.md`
- Manual Android and security checklists: `docs/qa/MANUAL_ANDROID_QA_CHECKLIST.md`, `docs/qa/SECURITY_TEST_CHECKLIST.md`
- CI gates and ready/done rules: `docs/qa/CI_GATE_DESIGN.md`, `docs/qa/DEFINITION_OF_READY_DONE.md`
- Failure and release gates: `docs/qa/FAILURE_MODE_MATRIX.md`, `docs/qa/RELEASE_GATE_CHECKLIST.md`
- Test harness, coverage, checklist, and fitness rules: `docs/qa/TEST_HARNESS_ARCHITECTURE.md`, `docs/qa/COVERAGE_AND_FLAKY_POLICY.md`, `docs/qa/LOCAL_PR_CHECKLIST.md`, `docs/qa/ARCHITECTURE_FITNESS_RULES.md`
- Pre-code completion audit: `docs/qa/PRECODE_COMPLETION_AUDIT.md`
- Test tooling ADR: `docs/adr/ADR-017-test-tooling-standards.md`
- API examples: `docs/api/examples/`
- QA JSON fixtures: `docs/qa/fixtures/`
- Reusable templates: `docs/templates/`
- GitHub templates and ownership: `.github/PULL_REQUEST_TEMPLATE.md`, `.github/ISSUE_TEMPLATE/`, `.github/CODEOWNERS`
- Sprint 0 plan: `docs/sprints/SPRINT_0_PLAN.md`
- Sprint 0 task packets: `docs/sprints/sprint-0/`
- Toolchain readiness: `docs/tooling/TOOLCHAIN_READINESS.md`
- QA validation tools: `tools/qa/`
- Obsidian vault home: `docs/OBSIDIAN_VAULT_INDEX.md`
- Mermaid diagram pack: `docs/diagrams/README.md`

## Build Status

No runnable app or backend exists yet. Do not expect `flutter test`, backend tests, or CI to pass until toolchains are scaffolded in a later task.

Current pre-code validation:

```powershell
python tools/qa/validate_docs.py
python tools/qa/validate_json_examples.py
python tools/qa/scan_secrets.py
powershell -ExecutionPolicy Bypass -File tools/qa/check_toolchain.ps1
```

Pre-code planning is now complete enough for Sprint 0 implementation. Remaining test work requires actual scaffold/code files.
