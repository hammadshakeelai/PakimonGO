# Remaining Work — Honest Assessment

## Quick Summary

The app is a **working technical prototype** (291 tests, 46 sprints, 92 commits). It is **not production-ready**. Getting to a Play Store release requires an estimated **2-3 months** of additional work, mostly in operations, hardening, and missing features.

---

## Tier 1 — Required For Alpha APK (demo to real users)

These must be done before any real user touches the app.

| # | Task | What's Needed | Effort | Depends On |
|---|------|---------------|--------|------------|
| 1 | **Mapbox token** ✅ DONE | Wired for local dev: `pk.` token via `--dart-define`, `sk.` download token in `~/.gradle/gradle.properties`. Production token/CI injection still needed. | 10 min | — |
| 2 | **Firebase Auth** ✅ DONE (live-verified) | Backend `FirebaseAuthAdapter` (`AUTH_PROVIDER=firebase`) + Flutter Google sign-in (google_sign_in 7.x → Firebase ID token). **Live-verified on a real phone**: Google → Firebase ID token → backend `/v1/users/me` 200 (fake token → 401). Prod still needs the release keystore SHA-1 registered. | 1-2 days | — |
| 3 | **AI vision scoring** ✅ DONE (Groq) | Free-tier `GroqVisionProvider` wired (`VISION_PROVIDER=groq` + `GROQ_API_KEY`, no billing). Live-verified: bear photo → `Ursus arctos`/wild/0.99. Google Vision path also intact. | 1 day | — |
| 4 | **Rate limiting** ✅ DONE | Per-user cooldown on POST /v1/submissions via `SUBMISSION_COOLDOWN_SECONDS` (default 30s) → 429 `too_many_requests`. | 0.5 day | — |
| 5 | **APK size optimization** ✅ DONE | R8 minify + shrinkResources + split-per-ABI. arm64 105.8MB→39.8MB (−62%); `proguard-rules.pro` keeps Mapbox/Google/Flutter. Verify map render on a physical arm64 release build. | 1 day | — |

## Tier 2 — Required For Beta (wider test audience)

| # | Task | Effort | Details |
|---|------|--------|---------|
| 6 | **PostgreSQL migration** ✅ DONE | Verified the API end-to-end on the pgvector container. Fixed a broken index in migration 002 + added the missing `sensitive_species` table (003); `env.py` now honors `SYNC_DATABASE_URL`; compose host port is overridable (`DB_HOST_PORT`) to dodge a native Postgres. Full CRUD confirmed on Postgres. |
| 7 | **Error handling in Flutter** ✅ DONE | `ApiClient`: 15s timeout, transport errors → `ApiException(isNetworkError)`, correct backend/422 message extraction. All 5 data screens (Map/History/Leaderboard/Profile/Collection) use the shared `ErrorRetryView` (offline vs error + real message + Retry) via `isOffline` on the viewmodels. 129 tests. |
| 8 | **Onboarding screens** ✅ DONE | 4-page first-run flow (FR-ONB-001..005): welcome, wildlife safety, location privacy + permission context, scoring honesty. Persisted via `OnboardingGate` (after the age gate, before auth). 6 tests. |
| 9 | **Age gate (13+)** ✅ DONE | Neutral birth-year gate (FR-AGE-001..003): blocks <13, records a teen/adult band, persisted so it asks once. `AgeGate` wraps the whole app before auth. 11 tests (logic + widget). |
| 10 | **End-to-end tests on real device** | 2-3 days | All 291 tests are unit/widget. No real-device E2E testing for camera, map, upload, scoring flow. |
| 11 | **CI secrets setup** | 0.5 day | Deploy workflow references `RENDER_API_KEY` GitHub secret — not configured. |

## Tier 3 — Required For Production (Play Store)

| # | Task | Effort | Details |
|---|------|--------|---------|
| 12 | **iOS build** | 1-2 weeks | Not started. Needs macOS + Xcode, iOS adaptation, camera/map permissions rework, TestFlight. |
| 13 | **Privacy policy + terms** | 1 week | Required for store submission. Must cover data collection, location use, AI processing, minors, account deletion. |
| 14 | **Moderation tools** | 2-3 weeks | FR-MOD requirements: report/block flows, content moderation queue, appeal system. None built. |
| 15 | **App store review prep** | 1 week | Screenshots, descriptions, age rating, privacy questionnaire, test accounts for reviewers. |

## Tier 4 — Social Features (post-launch)

| Feature | Effort | Priority |
|---------|--------|----------|
| Friends & groups | 2-3 weeks | Medium |
| Comments & likes | 1-2 weeks | Medium |
| Public feed | 2 weeks | Medium |
| Sharing & reposts | 1 week | Low |
| Hashtags & captions | 1 week | Low |
| Leaderboard scopes (global, country, local, friends) | 1 week | Low |

## Tier 5 — Polish & Quality

| Task | Effort | Notes |
|------|--------|-------|
| Loading shimmer animations | 1-2 days | Currently `CircularProgressIndicator` everywhere |
| Dark mode | 1-2 days | Not implemented |
| Accessibility | 2-3 days | No semantic labels, no screen reader testing |
| API docs cleanup | 0.5 day | OpenAPI has placeholder v2 entries |
| Release APK optimization | 1 day | 105.8MB → target <60MB |
| Error analytics | 1 day | Crashlytics or Sentry integration |
| Flutter analyze warnings | 1 day | 8 info-level issues remain |

## Key Architectural Gaps (non-obvious)

| Gap | Risk |
|-----|------|
| **No auth token expiry** | FakeAuthAdapter accepts any `test_user_*` token forever. Firebase will fix this, but currently there's no session management. |
| ~~No file size enforcement in upload~~ ✅ FIXED | `PUT /media/upload` now caps the *actual* bytes at 10MB (413) and rejects empty files. Also added an ownership check (403 — was a BOLA hole). |
| ~~No image validation~~ ✅ FIXED | `PUT /media/upload` validates JPEG/PNG/WebP magic bytes and rejects non-images (400). |
| **Scoring worker is in-process** | InMemoryJobQueue and worker thread die with the server. No persistence, no retries, no DLQ. |
| **No background location** | FR-PERM-003 forbids it, but no map features work without at least foreground location. |
| **Notifications are fire-and-forget** | No push notifications. Only in-app polling via GET /v1/notifications. |
| ~~DB migrations broken/incomplete on Postgres~~ 🟡 improved | Migrations now apply cleanly on Postgres and cover all 12 model tables (fixed a broken partial index + the missing `sensitive_species` table). Still not auto-run at API startup — run `alembic upgrade head` on deploy. |

## Effort Totals

| Tier | Tasks | Estimated Effort |
|------|-------|-----------------|
| Tier 1 (Alpha) | 5 | ~3-4 days |
| Tier 2 (Beta) | 6 | ~7-10 days |
| Tier 3 (Production) | 4 | ~12-18 days |
| Tier 4 (Social) | 6 | ~8-12 weeks |
| Tier 5 (Polish) | 7 | ~7-10 days |

**To Production (Tiers 1+2+3): ~22-32 days of focused work.**
**To Social Launch (Tiers 1-5): ~3-5 months.**
