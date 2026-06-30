# Technical Debt Register

## Current Known Debt

No production code exists yet. Current debt is planning debt and decision debt.

## Decision Debt

- Exact Flutter package structure is not selected yet.
- Backend framework is not selected yet.
- Map provider decision needs cost and SDK prototype validation.
- Firebase Data Connect vs direct Cloud SQL access needs current pricing, limits, and local development validation.
- AI provider mix needs cost, latency, accuracy, and privacy testing.
- Species rarity source of truth needs a clear taxonomy and update workflow.
- Location privacy model needs legal and app-store review.
- Scoring point ranges and economy formulas are intentionally undefined until product review.
- Moderation staffing/tooling is undefined.
- Graphify integration is planned but not validated because no code exists yet.
- Actual Flutter and FastAPI project toolchains are not scaffolded yet; only repo boundaries exist.
- CI workflows are placeholders until runnable app/backend tooling exists.
- Conversation archive contains a summary and paste target, but not yet the complete full visible chat export.
- OpenAPI, ERD, threat model, UX, QA, and methodology diagrams are draft docs, not validated against executable code yet.
- Mermaid diagrams are source diagrams; final report rendering/figure QA is not done yet.

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
