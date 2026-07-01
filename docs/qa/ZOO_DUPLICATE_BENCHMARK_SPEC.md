# Zoo And Duplicate Benchmark Spec

## Purpose

Zoo/captive detection and duplicate detection are launch-blocking because they protect leaderboard fairness and stop low-effort farming.

## Benchmark Suites

| Suite | Test IDs | Main Signal |
|---|---|---|
| exact duplicate | `TC-DUP-EXACT-*` | cryptographic hash |
| perceptual duplicate | `TC-DUP-PHASH-*` | perceptual hash and near-image similarity |
| crop/variant duplicate | `TC-DUP-CROP-*` | crop, compression, screenshot, filter variants |
| semantic encounter | `TC-DUP-SEM-*` | embedding, time, user, location, species |
| zoo geofence | `TC-ZOO-GEOFENCE-*` | point/polygon and uncertainty intersection |
| zoo context | `TC-ZOO-CONTEXT-*` | visual/caption/context evidence |
| pet/wild/captive | `TC-ZOO-PET-*` | species and user-provided context |

## Required Duplicate Cases

| ID | Case | Expected Behavior |
|---|---|---|
| `TC-DUP-EXACT-001` | identical file upload by same user | no second normal score |
| `TC-DUP-EXACT-002` | identical file upload by another user | review/repost suspicion, not silent deletion |
| `TC-DUP-PHASH-001` | compressed image | duplicate candidate edge |
| `TC-DUP-CROP-001` | cropped animal center | duplicate or same-encounter candidate |
| `TC-DUP-CROP-002` | screenshot of prior post | repost suspicion and score cap/reject |
| `TC-DUP-SEM-001` | same animal same time/place, different angle | same encounter group, bounded score |
| `TC-DUP-SEM-002` | similar species, different animal | not duplicate; may need review |
| `TC-DUP-SEM-003` | material visual change over time | eligible only if change threshold passes |

## Required Zoo/Captive Cases

| ID | Case | Expected Behavior |
|---|---|---|
| `TC-ZOO-GEOFENCE-001` | point clearly inside zoo polygon | zoo/captive cap, save to collection |
| `TC-ZOO-GEOFENCE-002` | point clearly outside zoo polygon | no zoo cap from geofence alone |
| `TC-ZOO-GEOFENCE-003` | GPS accuracy overlaps boundary | review or cap, not confident penalty |
| `TC-ZOO-CONTEXT-001` | enclosure bars/signage visible | zoo/captive evidence recorded |
| `TC-ZOO-CONTEXT-002` | honest user marks zoo | tiny bounded participation credit |
| `TC-ZOO-CONTEXT-003` | user hides zoo context but geofence says zoo | trust decrease and review/cap |
| `TC-ZOO-PET-001` | dog/cat with owner tag | pet/social score only, owner credit after acceptance |
| `TC-ZOO-PET-002` | livestock/farm context | captive/pet-like review by default |
| `TC-ZOO-PET-003` | feral/domestic species in wild setting | review or limited wild eligibility by policy |

## Metrics

Track these per benchmark run:

| Metric | Meaning |
|---|---|
| duplicate precision | percent of duplicate flags that are correct |
| duplicate recall | percent of true duplicates caught |
| zoo precision | percent of zoo/captive flags that are correct |
| zoo recall | percent of true zoo/captive cases caught |
| review rate | percent routed to review instead of automatic decision |
| false penalty rate | wild/valid submissions incorrectly capped/rejected |
| farming miss rate | duplicate/zoo farming that receives normal score |
| latency p95 | time to complete checks |

## Gate Targets

Exact targets must be calibrated with real goldsets. Until then, use these planning gates:

- false public ranking for known exact duplicate: zero in test suite
- exact duplicate detection recall: 100% on controlled exact fixtures
- zoo geofence deterministic cases: 100% correct for clear inside/outside fixtures
- boundary uncertainty: never hard reject solely from uncertain GPS
- every uncertain case: explainable `review` or `capped` reason

## Anti-Gaming Rules

- Store duplicate decisions as graph edges.
- Keep threshold versions on every decision.
- Do not delete duplicate submissions silently.
- Do not reveal exact thresholds to clients.
- Use diminishing returns for repeated zoo/captive uploads.
- Record trust changes separately from user-visible score.
