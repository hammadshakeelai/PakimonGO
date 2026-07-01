# Work Package Board

## Purpose

This board turns the expanded plan into agent-ready work before production coding. Each work package must include requirement IDs, owned modules, non-owned boundaries, acceptance criteria, tests, security/privacy notes, rollback, and commit plan.

## Board

| ID | Status | Package | Primary Requirements | Owner Type | Next Gate |
|---|---|---|---|---|---|
| WP-001 | Complete | Repair Git/repo health | NFR-MAINT-003 | Dev lead | none |
| WP-002 | Complete | Expand SRS/requirements | all FR/NFR | Product/BA | SRS review |
| WP-003 | Complete | ADR completion pack | NFR-MAINT-003 | Architect | ADR review |
| WP-013 | Complete | Monorepo scaffold | NFR-MAINT-001..003 | Dev lead | toolchain scaffold |
| WP-014 | Complete | Commit workflow policy | NFR-MAINT-003 | Dev lead | use in every commit |
| WP-015 | Ready | Alpha-0 private capture slice | FR-CAP, FR-SCORE, FR-DUP, FR-ZOO | Mobile/backend pair | start Sprint 0 |
| WP-016 | Complete draft | Contract-first API draft | FR-CAP-011, FR-CAP-012, FR-SCORE-008 | Backend lead | OpenAPI review |
| WP-017 | Complete draft | Database ERD and data dictionary | data, privacy, scoring, social | Data lead | migration tool choice |
| WP-018 | Complete draft | Threat model and abuse cases | NFR-SEC, NFR-PRIV | Security lead | mitigation checklist |
| WP-019 | Complete draft | UX flow specification | onboarding, capture, map, social | UX lead | wireframe/prototype |
| WP-020 | Complete draft | Testing master plan | all FR/NFR | QA lead | first CI checks |
| WP-021 | Complete draft | Goldset manifest standard | FR-DUP, FR-ZOO, FR-TAX, FR-SCORE | AI/data lead | seed data policy |
| WP-022 | Complete draft | Obsidian/OKF/Graphify setup | NFR-MAINT-003 | Docs/knowledge lead | automation scripts later |
| WP-023 | Complete draft | Sprint 0 implementation plan | WP-015 | TPM/architect | begin Sprint 0 |
| WP-024 | Complete | Toolchain, QA scripts, and Sprint 0 packets | WP-015 | Dev lead | start S0-001 or S0-002 |
| WP-025 | Complete | Pre-code test architecture pack | WP-020, WP-015 | QA lead | implement first tests in Sprint 0 |
| WP-026 | Complete | Concrete test catalogue and CI guardrails | WP-020, WP-025 | QA/DevOps lead | start Sprint 0 code with tests |

## WP-016: Contract-First API Draft

- Goal: define `/v1` request/response boundaries before backend code.
- Owned files: `docs/api/OPENAPI_DRAFT.yaml`, `packages/contracts/`.
- Non-owned files: mobile feature implementation, worker implementation.
- Acceptance: upload, submission, score, map, moderation, leaderboard, and error envelopes are represented.
- Test plan: schema lint later; manual review now.
- Security/privacy notes: public DTOs must omit exact coordinates and private URLs.
- Rollback: revert contract doc commit before generated clients exist.
- Commit plan: `docs(api): draft alpha openapi contract`.

## WP-017: Database ERD And Schema Plan

- Goal: define canonical entities, relationships, indexes, privacy classes, and audit paths.
- Owned files: `docs/data/DATABASE_ERD.md`, `infrastructure/database/`.
- Non-owned files: migrations until toolchain selected.
- Acceptance: ERD covers identity, media, submissions, evidence, scoring, geo, social, moderation, audit.
- Test plan: schema review; migration tests later.
- Security/privacy notes: exact coordinates and originals are restricted data.
- Rollback: docs-only revert before migrations exist.
- Commit plan: `docs(data): add database erd plan`.

## WP-018: Threat Model

- Goal: enumerate trust boundaries, assets, attackers, abuse paths, and mitigations.
- Owned files: `docs/security/THREAT_MODEL.md`.
- Non-owned files: implementation.
- Acceptance: covers location leaks, sensitive species, GPS spoofing, zoo fraud, duplicate farming, UGC abuse, AI provider leakage, account deletion gaps, admin misuse.
- Test plan: mitigation-to-test mapping in QA plan.
- Security/privacy notes: this is a launch-gate artifact.
- Rollback: not expected; revise with ADR if posture changes.
- Commit plan: `docs(security): add threat model`.

## WP-019: UX Flow Specification

- Goal: define screen flows and states before UI code.
- Owned files: `docs/ux/UX_FLOW_SPEC.md`.
- Non-owned files: Flutter implementation.
- Acceptance: onboarding, auth, capture, upload, pending score, collection, map, report/block, settings covered.
- Test plan: accessibility and state checklist.
- Security/privacy notes: permission prompts are just-in-time and non-coercive.
- Rollback: docs-only revert.
- Commit plan: `docs(ux): define alpha flows`.

## WP-020: Testing Master Plan

- Goal: define complete automated/manual test strategy.
- Owned files: `docs/qa/TESTING_MASTER_PLAN.md`.
- Non-owned files: actual tests until code exists.
- Acceptance: test IDs map to traceability matrix and risky systems.
- Test plan: self-referential; first CI later validates docs.
- Security/privacy notes: privacy leak tests are launch-blocking.
- Rollback: revise by QA ADR if test tooling changes.
- Commit plan: `docs(qa): add testing master plan`.
