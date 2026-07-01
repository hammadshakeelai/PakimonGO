# Test Plan Template

## Purpose

Describe how this change will be verified before implementation starts.

## Scope

- Feature/module:
- Requirement IDs:
- Test IDs:
- Work package:

## Test Levels

| Level | Required? | Cases | Command/Evidence |
|---|---|---|---|
| unit | yes/no |  |  |
| contract | yes/no |  |  |
| integration | yes/no |  |  |
| E2E | yes/no |  |  |
| manual device | yes/no |  |  |
| abuse/security | yes/no |  |  |
| goldset/benchmark | yes/no |  |  |

## Fixtures

- Existing:
- New:
- Forbidden data:

## Privacy / Security Checks

- [ ] no exact public coordinates
- [ ] no private media or original URLs in public DTOs
- [ ] no raw EXIF in public derivatives
- [ ] authz negative test exists where applicable
- [ ] score finalization remains server-authoritative
- [ ] no secrets in config/examples

## Commands

```powershell
python tools\qa\validate_docs.py
python tools\qa\validate_json_examples.py
python tools\qa\scan_secrets.py
```

## Skipped Tests

| Test | Reason | Follow-up |
|---|---|---|

## Exit Criteria

-
