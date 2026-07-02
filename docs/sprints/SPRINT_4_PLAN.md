# Sprint 4 Plan: Real Upload Handler

## Sprint Goal

Replace signed URL placeholders with local filesystem storage. Uploads write files to disk, derivatives are generated as stubs, and files are served via a static endpoint.

## Sprint Status

**Complete.** All 5 tasks done and verified.

## Sprint Inputs

- Sprint 3 complete: auth on all protected endpoints
- Current upload flow: returns fake `https://uploads.pakimongo.example/signed/{id}` URL
- No actual file storage or serving exists

## In Scope

- Local file storage service (save/read paths on disk under `data/uploads/`)
- Real PUT `/v1/media/upload/{media_asset_id}` endpoint accepting raw file bytes
- Derivative stub generation on disk (copy original as thumbnail + public)
- Static file serving via `/v1/media/files/{path}`
- `uploadUrl` in upload-intent response points to real local endpoint

## Out Of Scope

- Real image processing (Pillow, thumbnail sizing)
- Cloud storage (S3, GCS)
- CDN integration
- Client-side upload progress/resume

## Sprint Backlog

| ID | Status | Task | Acceptance | Verification |
|---|---|---|---|---|
| S4-001 | ✅ DONE | Local file storage service | `LocalFileStorage` saves/reads under `data/uploads/` | unit test |
| S4-002 | ✅ DONE | File upload endpoint | PUT `/v1/media/upload/{id}` accepts file via UploadFile, saves to disk | test_upload_file_roundtrip |
| S4-003 | ✅ DONE | Derivative stubs on complete | complete-upload generates files in thumb/ and public/ | derivative tests pass |
| S4-004 | ✅ DONE | Static file serving | GET `/v1/media/files/{path}` serves stored files | FileResponse stream |
| S4-005 | ✅ DONE | Tests + clean up | All 47 API tests pass | tests pass |

## File Ownership

| Area | Owner |
|---|---|
| `services/api/src/infrastructure/storage/` | Backend agent |
| `services/api/src/modules/media/` | Backend agent |
| `data/uploads/` | Created at runtime |

## Security

- Upload endpoint requires auth (inherited from Sprint 3)
- File serving is public (derivatives are meant to be public)
- No executable uploads allowed (MIME sniffing prevention)
