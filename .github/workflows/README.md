# GitHub Workflows

## Current Workflow

- `docs-validation.yml`: runs planning docs validation, JSON example validation, and lightweight secret scanning.

## Planned Future Checks

- Flutter format/analyze/test after mobile scaffold exists.
- Backend lint/type/test after API/worker scaffold exists.
- Contract schema validation after contract tooling exists.
- Dedicated secret scanning such as gitleaks before external collaboration.
- Goldset benchmark smoke tests after fixtures and runners exist.

## Branch Protection

Repository settings should later require the docs validation workflow before merge. This cannot be enforced from the local repo alone.
