# Subagent Roles

## Purpose

The Codex UI may show available helper subagents such as Aristotle, James, Kant, Dewey, and Noether. These are optional coordination helpers for this development environment, not PakimonGO product requirements, architecture components, users, services, or release blockers.

## What To Tell Another AI

Say this:

```txt
Those names are optional Codex subagents visible in the current workspace. They are not required for the app. Continue from AGENTS.md, docs/CURRENT_TASK.md, docs/NEXT_TASK.md, and the Sprint 0 packets. Use the subagents only if parallel review/research would help, and keep ownership boundaries clear.
```

## Suggested Use If Available

| Subagent | Suggested Role | Good Tasks |
|---|---|---|
| Aristotle | architecture and reasoning reviewer | ADR review, domain boundaries, tradeoff checks |
| James | implementation/integration helper | backend scaffold, API contracts, local tooling |
| Kant | rules, security, and privacy critic | privacy DTOs, authz, threat model, policy checks |
| Dewey | process and QA helper | test plans, Agile workflow, acceptance criteria |
| Noether | data, invariants, and scoring helper | state machines, scoring rules, duplicate/zoo logic |

## Rules

- Do not wait for these subagents if they are unavailable.
- Do not encode these names into app code, API contracts, database tables, requirements, or user-facing docs.
- Do not let multiple agents edit the same files in parallel.
- If subagents are used, assign owned folders/files and ask each agent to report tests run, changed files, blockers, and next task.
- Sprint 0 can continue without them.

## Current Decision

Store only this lightweight note. The exact subagent availability is environment-specific and may change between AI sessions.
