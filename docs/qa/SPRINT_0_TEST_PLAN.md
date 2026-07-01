# Sprint 0 Test Plan

## Scope

Sprint 0 creates scaffold code only. Tests must prove the repo is buildable, importable, contract-aware, and privacy-safe enough to start Alpha-0 feature work.

## Required Commands

Run these from the repo root whenever the relevant folders exist:

```powershell
python tools\qa\validate_docs.py
powershell -ExecutionPolicy Bypass -File tools\qa\check_toolchain.ps1
```

After scaffold tasks land, add:

```powershell
cd services\api; python -m pytest
cd services\workers; python -m pytest
cd packages\contracts; python -m pytest
cd apps\mobile\pakimon_go_app; flutter test
```

## Task-Level Expectations

| Task | Required Tests | Must Prove |
|---|---|---|
| `S0-001` Flutter shell | `flutter pub get`, `flutter test` | app package resolves and empty widget/unit tests run |
| `S0-002` FastAPI shell | `python -m pytest`, import smoke | API app imports and `/health/live`, `/health/ready` contracts exist |
| `S0-003` worker shell | `python -m pytest`, import smoke | worker runner imports and no-op job exits safely |
| `S0-004` local config | secret scan/manual check | examples use dummy values only |
| `S0-005` contracts | OpenAPI parse/lint | draft contract is valid and package documents generation path |
| `S0-006` privacy DTO tests | pytest contract tests | public DTO schemas omit exact coordinates and private URLs |
| `S0-007` score state | unit tests | valid transitions and invalid transitions are enforced |
| `S0-008` capture draft | Dart unit tests | draft metadata serializes without real camera/storage |
| `S0-009` CI validation | workflow local parity | CI runs same commands documented here |
| `S0-010` state closeout | docs validator | state docs and traceability stay coherent |

## Launch-Blocking Sprint 0 Tests

| ID | Description | Owner |
|---|---|---|
| `TC-S0-DOCS-001` | docs validator passes | lead agent |
| `TC-S0-SEC-001` | no secrets in examples, docs, or scaffold config | DevOps/security agent |
| `TC-S0-PRIV-001` | public DTOs cannot contain exact lat/lng fields | contract/backend agent |
| `TC-S0-SCORE-001` | score state enum/model has a closed transition table | scoring agent |
| `TC-S0-CAP-001` | capture draft model does not require camera provider | mobile agent |

## Failure Policy

- If a tool is missing, record the exact blocker in `docs/TECH_DEBT.md` and `docs/NEXT_TASK.md`.
- If a privacy test fails, stop feature work and fix the contract first.
- If generated scaffold files exceed file-size guardrails, document the generated exception.
- Do not proceed from Sprint 0 to capture implementation until all P0 Sprint 0 tests pass or have approved blockers.
