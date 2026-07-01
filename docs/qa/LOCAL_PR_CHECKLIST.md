# Local PR Checklist

## Purpose

Run these checks before every commit or pull request. Add module-specific commands once code exists.

## Always Run

```powershell
python tools\qa\validate_docs.py
python tools\qa\validate_json_examples.py
python tools\qa\scan_secrets.py
git status --short
```

## Toolchain Check

Run when changing build, mobile, Android, Python, CI, or setup docs:

```powershell
powershell -ExecutionPolicy Bypass -File tools\qa\check_toolchain.ps1
```

## Backend Checks

After `services/api/` is scaffolded:

```powershell
cd services\api
python -m pytest
ruff check .
mypy src
```

After `services/workers/` is scaffolded:

```powershell
cd services\workers
python -m pytest
ruff check .
mypy src
```

## Flutter Checks

After `apps/mobile/pakimon_go_app/` is scaffolded:

```powershell
cd apps\mobile\pakimon_go_app
dart format --set-exit-if-changed .
flutter analyze
flutter test
```

## Contract Checks

After contract package tooling exists:

```powershell
cd packages\contracts
python -m pytest
```

## PR Evidence

Every PR or agent handoff should include:

- requirement/work-package IDs
- commands run and results
- tests not run with reason
- privacy/security notes
- screenshots or recordings for UI work
- rollback plan
- state docs updated
