# QA Documentation Index

## Purpose

This folder turns PakimonGO's test strategy into agent-ready quality gates. Start with `TESTING_MASTER_PLAN.md`, then use the focused specs below when creating code, tests, CI, or manual QA runs.

## Core Test Architecture

- `TESTING_MASTER_PLAN.md`: high-level strategy, test levels, launch-blocking suites.
- `REQUIREMENT_TO_TEST_MATRIX.md`: requirement families mapped to test IDs and gates.
- `TEST_CASE_CATALOGUE.md`: concrete 100+ test catalogue mapped to requirements, priority, automation, and gates.
- `BDD_ACCEPTANCE_SCENARIOS.md`: Gherkin-style acceptance scenarios for critical flows.
- `SPRINT_0_TEST_PLAN.md`: exact validation plan for the first code scaffold.
- `CI_GATE_DESIGN.md`: local and CI gates by project phase.
- `FAILURE_MODE_MATRIX.md`: failure, impact, detection, mitigation, and rollback matrix.
- `RELEASE_GATE_CHECKLIST.md`: release ring quality gates from local to production.
- `TEST_HARNESS_ARCHITECTURE.md`: target test folder layout, fixtures, fakes, and helper rules.
- `COVERAGE_AND_FLAKY_POLICY.md`: coverage targets and flaky/quarantine rules.
- `LOCAL_PR_CHECKLIST.md`: local commands for commits and pull requests.
- `ARCHITECTURE_FITNESS_RULES.md`: architecture rules to automate as code appears.
- `PRECODE_COMPLETION_AUDIT.md`: final pre-code readiness audit.

## Launch-Blocking Specs

- `PRIVACY_CONTRACT_TEST_SPEC.md`: public DTO and API privacy rules.
- `SCORING_STATE_TEST_SPEC.md`: score state machine invariants and test cases.
- `SECURITY_TEST_CHECKLIST.md`: auth, abuse, secrets, location, and UGC checks.

## Benchmark And Manual QA

- `GOLDSET_GOVERNANCE_PLAN.md`: dataset sourcing, consent, versioning, review, and manifests.
- `ZOO_DUPLICATE_BENCHMARK_SPEC.md`: duplicate, zoo, captive, and pet benchmark rules.
- `MANUAL_ANDROID_QA_CHECKLIST.md`: device checklist for APK/internal testing.
- `DEFINITION_OF_READY_DONE.md`: ready/done rules for work packages and test closure.
- `fixtures/`: JSON payload fixtures for future unit, contract, integration, and negative privacy tests.

## API Examples

API examples live in `docs/api/examples/` and must stay aligned with `docs/api/OPENAPI_DRAFT.yaml` until generated clients/examples exist.

## Collaboration Templates

Pull request, bug, feature, and test-gap templates live under `.github/`. Ownership boundaries are listed in `.github/CODEOWNERS`.

## Agent Rule

Every implementation agent must update the relevant QA spec before changing behavior if the current spec is missing acceptance criteria, test IDs, or privacy/security expectations.
