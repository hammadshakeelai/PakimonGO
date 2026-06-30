---
id: agent-process
type: process
title: Agent Process
status: active
updated: 2026-07-01
source_docs:
  - docs/PROCESS.md
  - docs/KNOWLEDGE_SYSTEM.md
related:
  - current-task
---

# Agent Process

## Required Start

Read:

1. `AGENTS.md`
2. `docs/CURRENT_TASK.md`
3. `docs/NEXT_TASK.md`
4. `docs/CURRENT_THINKING.md`
5. Relevant requirements and ADRs.

## Required End

Update:

- `docs/CURRENT_TASK.md`
- `docs/NEXT_TASK.md`
- `docs/BACKLOG.md`
- `docs/BUGS_AND_RISKS.md`
- `docs/TECH_DEBT.md`
- Any affected ADR or OKF concept.

## Main Rules

- Write next task before continuing.
- Use adversarial decision thinking.
- Keep files usually around 200-300 lines.
- Preserve context through requirement, ADR, risk, and debt references.
- Do not let two agents edit the same file set in parallel.
