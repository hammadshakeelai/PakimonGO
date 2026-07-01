# S0-010: Update Traceability And State Docs

## Goal

Close Sprint 0 cleanly by updating state, traceability, backlog, debt, bugs/risks, conversation archive, and tests-run evidence.

## Requirements

- `NFR-MAINT-003`

## Owned Files

- `docs/CURRENT_TASK.md`
- `docs/NEXT_TASK.md`
- `docs/CURRENT_THINKING.md`
- `docs/TASK_LOG.md`
- `docs/BACKLOG.md`
- `docs/BUGS_AND_RISKS.md`
- `docs/TECH_DEBT.md`
- `docs/conversation-archive/`
- `docs/TRACEABILITY_MATRIX.md`

## Forbidden Files

- implementation files unless state closeout reveals a documentation-only fix.

## Acceptance Criteria

- Sprint 0 status is accurate.
- Tests run and blockers are recorded.
- Next task names Sprint 1 or remaining Sprint 0 blockers.
- Conversation archive has a summary of major user/AI decisions.
- Git working tree is clean after final commit.

## Verification

```powershell
python tools/qa/validate_docs.py
git status --short
git log --oneline --decorate -10
```

## Rollback

Revert `docs(state): close sprint 0 scaffold pass`.

## Commit Target

`docs(state): close sprint 0 scaffold pass`
