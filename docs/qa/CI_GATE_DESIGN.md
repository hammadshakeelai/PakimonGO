# CI Gate Design

## Purpose

CI should enforce the same quality gates agents run locally. Early CI stays lightweight, then expands as code appears.

## Phase 1: Docs And Planning CI

Required now:

```powershell
python tools\qa\validate_docs.py
python tools\qa\validate_json_examples.py
python tools\qa\scan_secrets.py
```

Checks:

- requirement IDs appear in traceability
- OpenAPI YAML parses
- Markdown and Obsidian local links resolve
- Mermaid diagram files contain Mermaid blocks
- source files do not exceed hard file-size limits
- API examples and QA fixtures parse as JSON
- obvious committed secrets are blocked

Configured workflow:

- `.github/workflows/docs-validation.yml`

## Phase 2: Scaffold CI

Add when Sprint 0 code lands:

```powershell
cd services\api; python -m pytest
cd services\workers; python -m pytest
cd packages\contracts; python -m pytest
cd apps\mobile\pakimon_go_app; flutter test
```

Required checks:

- FastAPI app imports
- worker imports
- OpenAPI/schema package validates
- Flutter shell tests pass
- privacy DTO tests pass
- score state tests pass

## Phase 3: Security And Contract CI

Add before public endpoints:

- secret scan
- dependency audit
- public DTO forbidden-field scan
- OpenAPI lint
- authz negative tests
- upload idempotency tests
- EXIF stripping tests

## Phase 4: Benchmark CI

Add before AI/scoring exposure:

- small duplicate goldset smoke
- small zoo/captive goldset smoke
- score state snapshot tests
- scoring cost counter smoke
- model/prompt/schema structured-output validation

## Phase 5: Release CI

Add before Android alpha/beta:

- Android debug APK build
- Android release signing dry run without committing secrets
- low-end device manual QA checklist link
- crash reporting configuration smoke
- privacy manifest/store disclosure checklist

## Branch And Merge Policy

- P0 CI failures block merge.
- P1 failures block alpha builds unless a blocker is recorded.
- Flaky tests must be fixed or quarantined with owner and expiry.
- Benchmark threshold changes require report artifacts and state-doc updates.
- CI configuration changes must include local command parity in docs.

## Output Artifacts

Each CI run should publish or preserve:

- command logs
- test report
- OpenAPI validation result
- benchmark report when applicable
- APK/build artifact only in controlled release workflows
