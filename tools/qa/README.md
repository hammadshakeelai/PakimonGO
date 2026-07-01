# QA Tools

This folder holds lightweight repository validation tools. These are pre-code guardrails, not production app logic.

## Available Checks

```powershell
python tools/qa/validate_docs.py
python tools/qa/validate_json_examples.py
python tools/qa/scan_secrets.py
powershell -ExecutionPolicy Bypass -File tools/qa/check_toolchain.ps1
```

## Current Validation Coverage

- Requirement IDs in `docs/REQUIREMENTS.md` are present in `docs/TRACEABILITY_MATRIX.md`.
- OpenAPI draft YAML parses and contains core sections.
- Local Markdown links resolve where they use normal Markdown link syntax.
- Mermaid diagram files contain Mermaid blocks.
- Future source files over 300/500 lines are reported.
- API examples and QA fixtures parse as JSON.
- Obvious committed secrets are reported.

## Notes

The validator intentionally avoids network calls and provider logins. It should be safe to run before and after every planning or scaffold task.
