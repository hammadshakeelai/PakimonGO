# Sprint 14 Plan: Real Google Vision Provider

## Sprint Goal

Replace the GoogleVisionProvider placeholder with actual Google Cloud Vision REST API calls. Parse label and object annotations to detect species, confidence, and context (wild/zoo/pet).

## Sprint Status

**Complete.** 49 scoring-rules tests + 54 API tests all passing (103 Python + 14 Flutter = 117 total).

## Sprint Backlog

| ID | Status | Task | Acceptance | Verification |
|---|---|---|---|---|
| S14-001 | ✅ DONE | Implement real `analyze()` with REST API | Reads image, base64 encodes, POSTs to `vision.googleapis.com/v1/images:annotate` | All tests pass |
| S14-002 | ✅ DONE | Parse response for species, confidence, context | Extracts best label/object, classifies context via keyword matching | Zoo/wild/pet parsed correctly |
| S14-003 | ✅ DONE | Add `requests` dependency | `requirements.txt` includes `requests` | `pip install -r requirements.txt` works |
| S14-004 | ✅ DONE | Mock API tests (6 scenarios) | Zoo, wild, pet, empty, error, HTTP error, file-not-found | 49 scoring-rules tests pass |
| S14-005 | ✅ DONE | Update state docs | CURRENT_TASK, NEXT_TASK, CURRENT_THINKING, session checklist, sprint plan | QA validations pass |

## Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `GOOGLE_VISION_API_KEY` | Yes | — | Google Cloud Vision REST API key |
| `VISION_PROVIDER` | No | `dummy` | Set to `google`/`gcp` to use GoogleVisionProvider |

## API Details

- **Endpoint:** `POST https://vision.googleapis.com/v1/images:annotate?key={GOOGLE_VISION_API_KEY}`
- **Features requested:** `LABEL_DETECTION` (10 results) + `OBJECT_LOCALIZATION` (5 results)
- **Context classification:**
  - `zoo` keywords: zoo, aviary, enclosure, captivity, exhibit, menagerie
  - `pet` keywords: pet, domestic, dog, cat, indoor, kitten, puppy
  - Default: `wild` (or `unknown` if no labels at all)

## File Ownership

| Area | Owner |
|---|---|
| `packages/scoring-rules/src/google_vision_provider.py` | GoogleVisionProvider implementation |
| `packages/scoring-rules/tests/test_vision_provider.py` | Mock API tests |
| `services/api/requirements.txt` | Runtime dependencies |
