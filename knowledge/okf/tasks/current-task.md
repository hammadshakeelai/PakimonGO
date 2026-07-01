---
id: current-task
type: task_state
title: Current Task
status: active
updated: 2026-07-01
source_docs:
  - docs/CURRENT_TASK.md
  - docs/NEXT_TASK.md
  - docs/sprints/SPRINT_0_PLAN.md
related:
  - agent-process
  - adr-summary
---

# Current Task

## Summary

The project is in Phase 5: scaffold, methodology alignment, and implementation readiness. ADR review, data dictionary, diagram pack, traceability matrix, and Sprint 0 plan are complete drafts.

The QA test architecture is now expanded with focused specs under `docs/qa/`, including requirement-to-test mapping, Sprint 0 tests, privacy contract tests, scoring state tests, goldset governance, zoo/duplicate benchmarks, Android QA, security checks, CI gates, and ready/done rules.

The concrete test layer now includes a test case catalogue, BDD scenarios, failure-mode matrix, release gates, API examples, QA JSON fixtures, JSON validation, secret scan, and docs validation workflow.

## Ready Next

Begin Sprint 0: Alpha-0 toolchain and contract foundation.

Allowed next work:

- Flutter app shell.
- FastAPI API shell.
- Worker shell.
- Contract package shell.
- OpenAPI validation.
- Public DTO privacy tests.
- Score state model shell.
- Capture draft model shell.
- Use task packets in `docs/sprints/sprint-0/`.
- Use QA specs in `docs/qa/` before writing code.
- Run `python tools/qa/validate_docs.py`, `python tools/qa/validate_json_examples.py`, and `python tools/qa/scan_secrets.py` before and after scaffold work.

## Still Gated

- Public social features.
- Final map provider implementation.
- Production deployment.
- Final retention workflows.
- Final scoring formula.
- Real AI provider calls.

## Handoff

Read `docs/sprints/SPRINT_0_PLAN.md` and `docs/qa/README.md` before coding.
