# Sprint 16 Plan: Goldset Integration

## Sprint Goal

Create goldset manifests for duplicate-detection and zoo-detection, build a goldset runner to benchmark precheck logic against them, and wire goldset smoke tests into CI.

## Sprint Status

**Complete.** 12 goldset tests + 49 existing scoring-rules tests = 61 total, all passing. CI job added.

## Sprint Backlog

| ID | Status | Task | Acceptance | Verification |
|---|---|---|---|---|
| S16-001 | ✅ DONE | Create duplicate-detection manifest | 9 scenarios: exact dup, new sha, empty set, null/empty current, dup overrides zoo/pet, zoo/pet no dup | `data/goldsets/duplicate-detection/manifest.yaml` exists |
| S16-002 | ✅ DONE | Create zoo-detection manifest | 9 scenarios: zoo/pet/wild/unknown/empty/null context, mixed case, dup overrides zoo, zoo with unrelated sha | `data/goldsets/zoo-detection/manifest.yaml` exists |
| S16-003 | ✅ DONE | Goldset runner module | `load_manifest`, `validate_manifest`, `run_scenario`, `run_manifest`, `run_manifest_path` | `packages/scoring-rules/src/goldset_runner.py` |
| S16-004 | ✅ DONE | Goldset tests | 12 tests: manifest existence, load, run single, run full (dup+zoo), invalid manifests, not found | `tests/test_goldset_runner.py` |
| S16-005 | ✅ DONE | CI goldset-smoke job | New GitHub Actions job runs goldset tests on PR/push | `.github/workflows/docs-validation.yml` |

## Goldset Manifests

### Duplicate Detection (`data/goldsets/duplicate-detection/manifest.yaml`)

9 scenarios covering:
- Exact duplicate caught (dup-001)
- Different SHA256 not duplicate (dup-002)
- Empty existing set (dup-003)
- Null current SHA256 (dup-004)
- Empty string current SHA256 (dup-005)
- Duplicate overrides zoo context (dup-006)
- Duplicate overrides pet context (dup-007)
- Zoo without duplicate (dup-008)
- Pet without duplicate (dup-009)

### Zoo Detection (`data/goldsets/zoo-detection/manifest.yaml`)

9 scenarios covering:
- Zoo context flagged (zoo-001)
- Pet context flagged (zoo-002)
- Wild passes to AI (zoo-003)
- Unknown defaults to AI (zoo-004)
- Empty context defaults to AI (zoo-005)
- Null context defaults to AI (zoo-006)
- Mixed case zoo detected (zoo-007)
- Duplicate overrides zoo (zoo-008)
- Zoo with unrelated existing SHA (zoo-009)

## Runner Interface

```python
from goldset_runner import load_manifest, run_manifest, run_manifest_path, validate_manifest

# Load and validate
manifest = load_manifest("path/to/manifest.yaml")

# Run full benchmark
report = run_manifest(manifest)
# GoldsetReport(dataset_id, dataset_type, total=9, passed=9, failed=0, failures=[])

# Or run single path
report = run_manifest_path("path/to/manifest.yaml")
```

## CI Job

```yaml
goldset-smoke:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-python@v5
    - run: pip install PyYAML
    - run: pytest tests/test_goldset_runner.py -v
      working-directory: packages/scoring-rules
```

## File Ownership

| Area | Owner |
|---|---|
| `data/goldsets/duplicate-detection/manifest.yaml` | Duplicate goldset |
| `data/goldsets/zoo-detection/manifest.yaml` | Zoo goldset |
| `packages/scoring-rules/src/goldset_runner.py` | Benchmark runner |
| `packages/scoring-rules/tests/test_goldset_runner.py` | Goldset tests |
| `.github/workflows/docs-validation.yml` | CI config |