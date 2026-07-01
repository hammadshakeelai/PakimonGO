# Work Packages

## Status Legend

- Proposed: defined but not started.
- In Progress: actively being changed.
- Complete: acceptance met.
- Blocked: cannot continue without decision or dependency.

## WP-001: Repair Git/Repo Health

- Status: Complete
- Acceptance: `git status` works or repo intentionally initialized.
- Notes: Fresh `git init` repaired invalid Git metadata on 2026-07-01.

## WP-002: Expand SRS/Requirements

- Status: Complete
- Acceptance: 196 functional requirements accepted as working baseline.
- Notes: `docs/REQUIREMENTS.md` now contains 196 functional requirements plus measurable NFRs.

## WP-003: ADR Completion Pack

- Status: Complete
- Acceptance: missing ADR drafts exist.
- Notes: ADR-001 through ADR-016 were reviewed on 2026-07-01; 13 accepted, 1 revised, 2 deferred.

## WP-013: Scaffold Monorepo Skeleton

- Status: Complete
- Acceptance: module folders and README boundaries exist.
- Notes: Mobile, API, workers, packages, infrastructure, data, tools, and knowledge graph folders exist with placeholders.

## WP-014: Commit Workflow Policy

- Status: Complete
- Acceptance: short-burst commit policy and template exist.
- Notes: `docs/COMMIT_POLICY.md` and `.gitmessage.txt` added; local Git template configured.

## WP-015: Alpha-0 Private Capture Slice

- Status: Ready
- Acceptance: see `docs/ALPHA_0_VERTICAL_SLICE.md`.
- Notes: This is the next implementation package and should start through `docs/sprints/SPRINT_0_PLAN.md`.

## WP-016: Contract-First API Draft

- Status: Complete draft
- Acceptance: `/v1` upload, submission, score, map, leaderboard, report, block, and appeal contracts are represented.
- Notes: See `docs/api/OPENAPI_DRAFT.yaml`.

## WP-017: Database ERD And Schema Plan

- Status: Complete draft
- Acceptance: canonical domains, table clusters, ERD, indexes, restricted data classes, table-level fields, privacy classes, and first migration slice documented.
- Notes: See `docs/data/DATABASE_ERD.md` and `docs/data/DATA_DICTIONARY.md`.

## WP-018: Threat Model

- Status: Complete draft
- Acceptance: assets, trust boundaries, STRIDE matrix, abuse cases, and launch-blocking controls documented.
- Notes: See `docs/security/THREAT_MODEL.md`.

## WP-019: UX Flow Specification

- Status: Complete draft
- Acceptance: onboarding, capture, collection, map, social, report/block, and accessibility states documented.
- Notes: See `docs/ux/UX_FLOW_SPEC.md`.

## WP-020: Testing Master Plan

- Status: Complete draft
- Acceptance: test levels, test ID families, launch-blocking suites, CI plan, and manual QA gates documented.
- Notes: See `docs/qa/TESTING_MASTER_PLAN.md`.

## WP-021: Goldset Manifest Standard

- Status: Complete draft
- Acceptance: manifest schema and benchmark metric categories documented.
- Notes: See `data/goldsets/MANIFEST_SCHEMA.md`.

## WP-022: Obsidian, OKF, And Graphify Setup

- Status: Complete draft
- Acceptance: vault index, OKF trace files, Graphify plan, and OKF export plan exist.
- Notes: See `docs/OBSIDIAN_VAULT_INDEX.md`, `knowledge/okf/`, and `tools/graphify/GRAPHIFY_PLAN.md`.

## WP-023: Sprint 0 Implementation Plan

- Status: Complete draft
- Acceptance: Sprint goal, scope, tasks, file ownership, commit sequence, tests, privacy/security notes, rollback, and definition of done are documented.
- Notes: See `docs/sprints/SPRINT_0_PLAN.md`.
