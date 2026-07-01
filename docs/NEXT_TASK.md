# Next Task

## Current Next Task

Begin Sprint 0: Alpha-0 toolchain and contract foundation. Pre-code preparation is complete enough; do not add more planning-only layers unless a new blocker is discovered.

## Exact Next Steps

1. Read `docs/sprints/SPRINT_0_PLAN.md`.
2. Read the exact task packet under `docs/sprints/sprint-0/`.
3. Read `docs/qa/README.md`, `docs/qa/TEST_CASE_CATALOGUE.md`, and `docs/qa/SPRINT_0_TEST_PLAN.md`.
4. For backend/contract work, read `docs/qa/PRIVACY_CONTRACT_TEST_SPEC.md` and `docs/api/examples/README.md`.
5. For scoring work, read `docs/qa/SCORING_STATE_TEST_SPEC.md`.
6. Read `docs/qa/LOCAL_PR_CHECKLIST.md` and `docs/qa/ARCHITECTURE_FITNESS_RULES.md`.
7. Start S0-003 worker shell, S0-004 local config, or S0-005 contract package in a short-burst commit.
8. Run `python tools/qa/validate_docs.py`, `python tools/qa/validate_json_examples.py`, and `python tools/qa/scan_secrets.py` before and after scaffold changes.
9. Keep public/social/map-provider-specific implementation out of Sprint 0.
10. Update `docs/conversation-archive/` with the full visible conversation if the user pastes it into the prepared raw text file.

## Backlog Additions From This Task

- Add detailed requirement cards for the 196 functional requirements when story tracking begins.
- Add code CI checks once runnable toolchains exist.
- Add module-level READMEs before non-trivial source code is created.
- Add Graphify generation workflow after first code exists.
- Add conversation archive summaries after major planning or implementation sessions.
- Add automated consistency checks for requirement IDs and traceability rows.
- Render Mermaid diagrams for final report after report generation tooling exists.
- Add actual pytest/Dart tests from the QA specs as Sprint 0 code appears.
- Create benchmark reports after the first goldset fixtures exist.
- Convert `docs/qa/BDD_ACCEPTANCE_SCENARIOS.md` into E2E tests after runnable mobile/API flows exist.
- Wire `.github/workflows/docs-validation.yml` as a required branch check once GitHub repo settings are configured.
