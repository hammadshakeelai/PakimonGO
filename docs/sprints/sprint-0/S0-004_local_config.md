# S0-004: Add Local Development Config Examples

## Goal

Add safe local configuration examples for future API, worker, Flutter, database, and provider adapters.

## Requirements

- `NFR-SEC-005`
- `NFR-PORT-002`

## Owned Files

- `.env.example`
- `infrastructure/docker/`
- relevant README files

## Forbidden Files

- `.env`
- real secrets
- cloud credentials
- private datasets

## Acceptance Criteria

- Example values are dummy placeholders only.
- Required environment variables are documented.
- `.gitignore` protects real local secrets.
- No provider calls are configured live.

## Verification

```powershell
git status --short
rg "AIza|sk-|BEGIN PRIVATE KEY|password=.*[^_]" .
```

Review any matches manually; placeholder strings are allowed only when clearly fake.

## Rollback

Revert `chore(dev): add local config examples`.

## Commit Target

`chore(dev): add local config examples`
