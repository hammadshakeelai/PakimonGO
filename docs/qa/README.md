# QA Documentation Index

## Purpose

This folder turns PakimonGO's test strategy into agent-ready quality gates. Start with `TESTING_MASTER_PLAN.md`, then use the focused specs below when creating code, tests, CI, or manual QA runs.

## Core Test Architecture

- `TESTING_MASTER_PLAN.md`: high-level strategy, test levels, launch-blocking suites.
- `REQUIREMENT_TO_TEST_MATRIX.md`: requirement families mapped to test IDs and gates.
- `SPRINT_0_TEST_PLAN.md`: exact validation plan for the first code scaffold.
- `CI_GATE_DESIGN.md`: local and CI gates by project phase.

## Launch-Blocking Specs

- `PRIVACY_CONTRACT_TEST_SPEC.md`: public DTO and API privacy rules.
- `SCORING_STATE_TEST_SPEC.md`: score state machine invariants and test cases.
- `SECURITY_TEST_CHECKLIST.md`: auth, abuse, secrets, location, and UGC checks.

## Benchmark And Manual QA

- `GOLDSET_GOVERNANCE_PLAN.md`: dataset sourcing, consent, versioning, review, and manifests.
- `ZOO_DUPLICATE_BENCHMARK_SPEC.md`: duplicate, zoo, captive, and pet benchmark rules.
- `MANUAL_ANDROID_QA_CHECKLIST.md`: device checklist for APK/internal testing.
- `DEFINITION_OF_READY_DONE.md`: ready/done rules for work packages and test closure.

## Agent Rule

Every implementation agent must update the relevant QA spec before changing behavior if the current spec is missing acceptance criteria, test IDs, or privacy/security expectations.
