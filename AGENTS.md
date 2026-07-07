# Agent Entry Point

**Read `CLAUDE.md` first** — it contains the complete grounded context: all file paths, class names, function signatures, test commands, navigation flow, conventions, and critical rules.

## MANDATORY TASK LOOP

```txt
PRE-TASK:
  [1] RUN: python tools/qa/pre_task_check.py (STOP if FAIL)
  [2] READ: docs/CURRENT_TASK.md, docs/NEXT_TASK.md, docs/CURRENT_THINKING.md
  [3] READ: sprint packet for the task
  [4] READ: docs/TRACEABILITY_MATRIX.md for relevant FR IDs
  [5] DO THE WORK (small files ≤300 lines)

POST-TASK:
  [6] RUN: validate_docs.py, validate_json_examples.py, scan_secrets.py (STOP if any FAIL)
  [7] UPDATE: CURRENT_TASK, NEXT_TASK, CURRENT_THINKING, TASK_LOG, BACKLOG, BUGS_AND_RISKS, TECH_DEBT
  [8] UPDATE ADR/OKF if architecture decision changed
  [9] COMMIT: semantic message + AI-Agent, AI-Work-Mode, AI-Commit-Time, Work-Package, Requirements, Process-Docs-Updated
```

## Verification Loop

After every completed task:
1. Re-run `pre_task_check.py`
2. Re-run all 3 validation scripts
3. Update `docs/SESSION_CHECKLIST.md`
