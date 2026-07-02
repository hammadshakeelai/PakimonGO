# Sprint 6 Plan: Duplicate/Zoo Precheck

## Sprint Goal

Extend scoring pipeline with duplicate detection (SHA256 matching) and animal-context precheck rules (zoo/pet caps).

## Sprint Status

**Complete.** All 3 tasks done and verified.

## Sprint Inputs

- ScoreState machine with PENDING → PRECHECKED → AI_EVALUATED transitions
- EXPLANATION_CATEGORIES includes duplicate_cap, zoo_cap, pet_cap
- MediaAsset has sha256 for duplicate detection
- Submission has animal_context (wild/zoo/pet/unknown)

## In Scope

- Precheck service in scoring-rules package (pure logic, no DB)
- Duplicate detection: compare incoming SHA256 against existing submissions
- Context rules: zoo → zoo_cap, pet → pet_cap, wild → normal
- Wire precheck into submission creation POST endpoint
- Package + API tests

## Out Of Scope

- Real AI scoring pipeline
- LLM-based duplicate detection (image similarity)
- Geo-based duplicate detection
- Admin review interface

## Sprint Backlog

| ID | Status | Task | Acceptance | Verification |
|---|---|---|---|---|---|
| S6-001 | ✅ DONE | Precheck service | run_precheck returns PrecheckResult with duplicate_found, explanation_category, suggested_state | 8 package tests pass |
| S6-002 | ✅ DONE | Wire into submission flow | POST /v1/submissions runs precheck, updates submission status | all 54 API tests pass |
| S6-003 | ✅ DONE | Package + API tests | Precheck logic tested in isolation + integration | all 95 tests pass |
