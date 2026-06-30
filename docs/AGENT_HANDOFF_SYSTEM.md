# Agent Handoff System

## Purpose

PakimonGO is intentionally designed for long-running, multi-agent work. Every agent should be able to understand the current state, pick up one bounded task, and leave a clean trail.

## Required Read Order

1. `AGENTS.md`
2. `docs/CURRENT_TASK.md`
3. `docs/NEXT_TASK.md`
4. `docs/CURRENT_THINKING.md`
5. `docs/PROCESS.md`
6. `docs/SRS.md`
7. Relevant ADRs and work package docs
8. Relevant module README
9. Relevant source files

## Required Update Order

Before ending meaningful work:

1. Update changed artifact docs.
2. Update `docs/TRACEABILITY_MATRIX.md` if requirements/use cases/contracts/tests changed.
3. Update `docs/CURRENT_TASK.md`.
4. Update `docs/NEXT_TASK.md`.
5. Update `docs/CURRENT_THINKING.md`.
6. Update backlog/risk/debt when needed.
7. Update `docs/conversation-archive/` with raw prompt text or summary if direction changed.
8. Commit in short semantic bursts with AI trailers.

## Task Packet Template

```md
## Task

- Work package:
- Goal:
- Requirements:
- Owned files:
- Forbidden files:
- Dependencies:
- Acceptance criteria:
- Test plan:
- Security/privacy notes:
- Rollback:
- Commit plan:
- Handoff notes:
```

## AI Final Response Checklist

- State what changed.
- State files changed.
- State tests or validation run.
- State what was not done.
- State next exact task.
- Mention commit hashes if commits were created.

## Parallel Agent Rule

Do not let two agents edit the same files in parallel. If parallel work is needed, split by owned folders, for example:

- Agent A: `docs/api/`, `packages/contracts/`
- Agent B: `docs/data/`, `infrastructure/database/`
- Agent C: `docs/security/`, `docs/qa/`
- Agent D: `apps/mobile/` after mobile ADR acceptance
