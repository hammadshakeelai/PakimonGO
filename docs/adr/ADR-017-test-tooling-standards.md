# ADR-017: Test Tooling Standards

## Status

Accepted for Sprint 0.

## Context

PakimonGO now has a large requirements and QA catalogue. Before scaffold code starts, implementation agents need a default testing stack so they do not invent incompatible tools per module.

## Options

### Python/FastAPI Testing Stack

- `pytest` for unit, integration, and contract tests.
- `pytest-asyncio` for async service tests.
- `httpx` with ASGI transport for API tests.
- `coverage.py` for backend coverage.
- `ruff` for lint and formatting.
- `mypy` for static typing once package boundaries exist.
- `openapi-spec-validator` or equivalent for OpenAPI validation.

### Flutter Testing Stack

- `flutter_test` for unit and widget tests.
- `integration_test` for app-level flows.
- `mocktail` for mocks/fakes.
- `patrol` can be evaluated later for richer device E2E.
- Native `flutter analyze` and `dart format` are required once the app exists.

### Security And Contract Tools

- `tools/qa/scan_secrets.py` is the current lightweight local scanner.
- Add `gitleaks` or equivalent before external collaboration.
- Add generated-client/schema validation after contract package tooling exists.

## Internal Challenge

Too many tools too early can slow scaffold work. Too few tools allows drift and makes privacy/scoring regressions easier.

## Decision

Use the Python/FastAPI and Flutter defaults above for Sprint 0. Keep CI dependency-light until real code exists, then add tooling per scaffold packet.

## Consequences

- Sprint 0 backend packages should include pytest-ready layout.
- Flutter shell should include `flutter_test` from the default template and add `mocktail` only when mocks exist.
- Contract tests should start with JSON and OpenAPI parse checks, then graduate to schema validation.
- Security scanning starts lightweight and later upgrades to a dedicated scanner.

## Reversal Conditions

- A tool conflicts with generated project templates.
- CI runtime or local setup becomes too slow for short-burst commits.
- A provider SDK or framework requires a different standard testing tool.

## References

- Requirements: NFR-MAINT-002, NFR-MAINT-003, NFR-SEC-005
- Related docs: `docs/qa/CI_GATE_DESIGN.md`, `docs/qa/TEST_HARNESS_ARCHITECTURE.md`
