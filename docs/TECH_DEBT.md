# Technical Debt Register

## Current Known Debt

No production code exists yet. Current debt is planning debt and decision debt.

## Decision Debt

- Exact Flutter generated package structure will be locked during S0-001, using the feature-first direction already documented.
- Backend framework is selected for Sprint 0: FastAPI modular monolith. Revisit only if ADR-007 reversal conditions appear.
- Map provider decision needs cost and SDK prototype validation.
- Firebase Data Connect vs direct Cloud SQL access needs current pricing, limits, and local development validation.
- AI provider mix needs cost, latency, accuracy, and privacy testing.
- Species rarity source of truth needs a clear taxonomy and update workflow.
- Location privacy model needs legal and app-store review.
- Scoring point ranges and economy formulas are intentionally undefined until product review.
- Moderation staffing/tooling is undefined.
- Graphify integration is planned but not validated because no code exists yet.
- Actual Flutter and FastAPI project code is not scaffolded yet; only repo boundaries and tooling standards exist.
- CI covers docs, JSON examples, secret scan, API tests (26), worker tests, scoring-rules tests (18), and Flutter tests (14). Phase 2 scaffold CI is complete. Phase 3-5 CI gates (security, benchmark, release) remain for future sprints.
- Conversation archive contains summaries and a paste target; the complete full visible chat export depends on a user-provided paste/export.
- OpenAPI, ERD, threat model, UX, QA, and methodology diagrams are draft docs, not validated against executable code yet.
- Mermaid diagrams are source diagrams; final report rendering/figure QA is not done yet.
- Data dictionary is a planning dictionary, not final migrations.
- GitHub Actions workflow exists for docs validation, JSON example validation, and lightweight secret scanning; branch protection must be enabled later in GitHub repository settings.
- Direct `adb` is not on PATH; use the SDK path or add platform-tools to PATH when direct device commands are needed.
- QA specs are now detailed, but the actual pytest/Dart/benchmark tests do not exist until Sprint 0 code scaffolds the modules.
- Exact pass thresholds for zoo/duplicate/species goldsets are planning gates only until licensed fixtures and benchmark reports exist.
- API examples and QA fixtures are syntax-validated only; schema validation should be added after contract tooling/generation exists.
- GitHub CODEOWNERS uses placeholder teams until real repository users/teams exist.

## Future Debt Controls

- Files should usually stay near 200-300 lines. If a file grows larger, split by responsibility or document why not.
- Every module needs a local README or module overview once it becomes non-trivial.
- Every shortcut must be logged here with owner, reason, and removal condition.
- No generated code should be hand-edited unless the generator workflow is documented.
- Any temporary scoring or moderation rule must include an expiry review date.

## Debt Entry Template

```md
## TD-000: Title

- Area:
- Introduced:
- Reason:
- Risk:
- Removal plan:
- Owner:
- Review date:
```
