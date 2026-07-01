# Definition Of Ready And Done

## Definition Of Ready

A task is ready for coding only when it has:

- requirement IDs or work-package ID
- owned files/modules
- forbidden files/modules
- acceptance criteria
- test plan
- privacy/security notes
- rollback plan
- expected commit subject
- state-doc update expectation

For Sprint 0, the packet files under `docs/sprints/sprint-0/` are the source of truth.

## Definition Of Done

A task is done only when:

- implementation or documentation change is complete
- required tests or validators pass
- skipped tests have explicit reason and follow-up
- no secrets, private photos, exact locations, or build artifacts are staged
- file-size guardrails are respected or documented
- public contracts have privacy checks when applicable
- state docs are updated
- commit follows `docs/COMMIT_POLICY.md`

## Test Closure Template

Add this to task closeout notes:

```txt
Tests Run:
- command:
- result:
- evidence:

Tests Not Run:
- command:
- reason:
- follow-up:

Privacy/Security:
- checked:
- unresolved:
```

## Ready Review Questions

- What behavior is being protected?
- Which requirement proves this work is needed?
- What test would fail if the behavior regresses?
- Could this leak exact location, private media, or moderation evidence?
- Could this reward unsafe animal interaction or score farming?
- How will the next agent know where to continue?

## Done Review Questions

- Can a fresh agent run the same checks?
- Are the changed files narrow enough to review?
- Is the next task written before stopping?
- Are bugs, risks, and technical debt recorded?
- Is the commit small enough to revert independently?
