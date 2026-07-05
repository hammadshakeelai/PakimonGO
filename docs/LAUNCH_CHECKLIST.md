# PakimonGO — Launch Checklist

Everything the **code** needs is done; what remains needs **you** (accounts,
secrets, a Mac, store paperwork). This is the single source of truth for
finishing the app, ordered by goal. Check items off as you go.

---

## ✅ Already done (code-complete + verified this build)

- Age gate (13+) → onboarding → auth → home startup flow
- **Real Google Sign-In** via Firebase — verified end-to-end on a physical phone
- **Real AI scoring** via Groq (free tier, no billing) — live-verified (bear → *Ursus arctos*)
- Mapbox map (local dev token), submission rate limiting, offline/error + Retry on every screen, dark mode
- Upload security (size + image-type + ownership), APK optimization (arm64 ≈ 40 MB, −62%)
- Runs on **real PostgreSQL** (migrations fixed + verified); 151 Flutter tests, 112 API tests, `flutter analyze` clean

You have already provisioned: **Mapbox token**, **Groq key**, **Firebase project** (`pakimongo`, debug SHA-1 registered), **Docker**.

---

## 🎯 Goal 1 — Give a testable APK to other people (Alpha/Beta)

- [ ] **Create a real release keystore** (release currently signs with the *debug* key — fine for you, not for the store):
  ```
  keytool -genkey -v -keystore pakimongo-release.jks -keyalg RSA -keysize 2048 -validity 10000 -alias pakimongo
  ```
  Keep this file + passwords safe and **out of git**. Wire it into `android/app/build.gradle.kts` (`signingConfigs`) and `key.properties`.
- [ ] **Register the release keystore's SHA-1** in Firebase → Project settings → Android app → *Add fingerprint* (get it via `keytool -list -v -keystore pakimongo-release.jks -alias pakimongo`), then **re-download `google-services.json`**. (Google Sign-In in a release build needs the release key's SHA-1, just like the debug one did.)
- [ ] Build the release APK/AAB and share it (or use **Firebase App Distribution** for testers).

## 🎯 Goal 2 — Deploy the backend (so testers don't need your PC)

- [ ] Create a **Render** account (render.com) and connect this GitHub repo (`render.yaml` is already here).
- [ ] Provision a **PostgreSQL** database (Render Postgres or Cloud SQL) → copy its connection string.
- [ ] Set these **environment variables / secrets** on the API service:

  | Var | Value |
  |-----|-------|
  | `SYNC_DATABASE_URL` | your Postgres connection string |
  | `AUTH_PROVIDER` | `firebase` |
  | `GOOGLE_APPLICATION_CREDENTIALS` | path to the Firebase **service-account JSON** (upload it as a secret file) |
  | `VISION_PROVIDER` | `groq` |
  | `GROQ_API_KEY` | your Groq key |
  | `STORAGE_PROVIDER` | `local` for now (see Goal 3) |
  | `CORS_ORIGINS` | your app's origins |

- [ ] **Run migrations on first deploy**: `alembic upgrade head` (now works — the migration bugs are fixed).
- [ ] Point the app at the deployed API: build with `--dart-define=API_BASE_URL=https://<your-render-url>`.
- [ ] (Optional) Add a **`RENDER_API_KEY`** GitHub secret to enable the auto-deploy workflow.

## 🎯 Goal 3 — Production hardening (before real users at scale)

- [ ] **Cloud storage**: create an **S3 or GCS** bucket + credentials; set `STORAGE_PROVIDER=s3`/`gcs`. (Local disk works for testing but not across servers.)
- [ ] Consider moving the **scoring worker** off in-process (Redis / Cloud Tasks) — currently it dies with the server (no retries).
- [ ] Multi-instance **rate limiting** would need a shared store (Redis) — today it's a single-instance DB cooldown.

## 🎯 Goal 4 — Google Play submission (production)

- [ ] **Privacy policy + Terms** (required). Must cover data collection, location use, AI processing, **minors**, and account deletion. (Your onboarding/age-gate copy is a starting point.)
- [ ] **Moderation tools** — report / block / appeal flows are **not built yet**; Play requires UGC moderation. This is real dev work (say the word and I'll build the report/block flow — it's no-credential).
- [ ] Play Console ($25 one-time): create the app, store listing, screenshots, feature graphic, **content/age rating**, and the **Data Safety** form.
- [ ] Upload the signed **AAB** (Goal 1 keystore) with Play App Signing; add reviewer test accounts.

## 🎯 Goal 5 — iOS (separate track — needs a Mac; I can't do this remotely)

- [ ] A **Mac + Xcode** and an **Apple Developer** account ($99/yr).
- [ ] Add an **iOS app in Firebase** → `GoogleService-Info.plist`; add camera/location usage strings to `Info.plist`.
- [ ] Build, test via **TestFlight**, submit to App Store review.

---

## 💰 Cost summary

| Service | Cost |
|---------|------|
| Mapbox, Groq, Firebase (Spark), Render (hobby) | **Free tiers** |
| Google Play Console | **$25 one-time** |
| Apple Developer | **$99/year** |
| Production DB / storage / compute | pay-as-you-scale |

## 🔧 Nothing needed from you to keep *developing*

The app builds, tests, and runs locally today (`.\run_local.ps1` + `flutter run`). The list above is only for **shipping to other people / the stores**.

The single biggest remaining **code** item for the store is **moderation (report/block)** — everything else on your side is accounts, keys, and paperwork.
