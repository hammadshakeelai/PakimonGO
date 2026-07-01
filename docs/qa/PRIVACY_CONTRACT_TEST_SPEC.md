# Privacy Contract Test Spec

## Purpose

Public API contracts must prove that exact location, private media, and moderation evidence cannot leak through normal user-facing responses.

## Forbidden Public Fields

Public DTOs must not expose these fields unless the endpoint is explicitly private/admin and authorized:

| Field Pattern | Reason |
|---|---|
| `latitude`, `longitude`, `lat`, `lng`, `gps_*` | exact capture location |
| `exif`, `raw_exif`, `metadata.gps` | photo privacy leak |
| `original_url`, `storage_path`, `bucket`, `gcs_uri` | private media access |
| `signed_url` outside upload intent flow | media access bypass |
| `device_id`, `ip_address`, `app_check_token` | security telemetry exposure |
| `moderation_evidence`, `review_notes` | restricted safety evidence |
| `sensitive_species_exact_location` | wildlife safety exposure |

## Allowed Public Location Shapes

| DTO | Allowed Location Data |
|---|---|
| public map cell | cell ID, coarse centroid, radius/precision label, delayed activity count |
| public post | optional coarse place label, country/region, hidden-location reason |
| friends post | same as public unless explicit private sharing policy changes |
| private owner view | exact coordinates allowed only for owner/authenticated private endpoint |
| moderator view | exact coordinates allowed only with audited case access |

## Required Test Cases

| ID | Test | Requirement |
|---|---|---|
| `TC-PRIV-DTO-001` | public submission response rejects exact coordinate fields | `FR-MAP-004`, `NFR-PRIV-001` |
| `TC-PRIV-DTO-002` | public map activity uses cells/clusters, not pins | `FR-MAP-003`, `FR-MAP-004` |
| `TC-PRIV-DTO-003` | public media DTO exposes derivative URL only | `FR-CAP-014`, `FR-CAP-015` |
| `TC-PRIV-DTO-004` | public derivatives never include EXIF GPS fields | `FR-CAP-015`, `NFR-PRIV-004` |
| `TC-PRIV-DTO-005` | sensitive species suppress or coarsen location | `FR-TAX-007`, `FR-MAP-005` |
| `TC-PRIV-DTO-006` | blocked users cannot infer restricted post data | `FR-SOC-006`, `FR-SOC-009` |
| `TC-PRIV-DTO-007` | notifications do not include exact locations | `FR-NOTIF-005` |
| `TC-PRIV-DTO-008` | owner private detail can include exact data only with owner auth | `FR-COL-006`, `NFR-SEC-002` |
| `TC-PRIV-DTO-009` | moderator exact-data access is audited | `FR-MOD-018`, `NFR-AUDIT-002` |

## Contract Implementation Pattern

Keep private and public schemas separate. Do not use one broad DTO and hide fields ad hoc.

```txt
PrivateSubmissionDetail
PublicPostSummary
PublicMapActivityCell
ModeratorSubmissionEvidence
```

Tests should recursively scan serialized public DTOs for forbidden field names and sample forbidden values. A test should fail even if the field is present with `null`.

## Review Rule

Any new public endpoint must add or update one privacy contract test before it can be merged. If exact data is needed for an owner or moderator endpoint, the test must prove both authorization and audit behavior.
