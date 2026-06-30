# Research Baseline

Last updated: 2026-07-01

This file records source-backed constraints and baseline decisions. Keep it current when major platform or policy docs change.

## Mobile Platform

### Current Recommendation

Use Flutter as the primary mobile framework. Build Android first, but keep iOS portability from day one.

### Why

- Flutter supports Android and iOS from one codebase.
- It is a strong fit for custom camera, map, animation, and game-like UI.
- Android can produce APKs for local/internal testing and Android App Bundles for Google Play distribution.

### Watchouts

- Validate camera performance, map rendering, background lifecycle, and upload reliability on low-end Android devices.
- For Google Play production, treat Android App Bundle as the main release artifact; APK is mainly for testing/direct distribution.

Sources:

- Flutter Android deployment: https://docs.flutter.dev/deployment/android
- Flutter iOS deployment: https://docs.flutter.dev/deployment/ios
- Android App Bundle: https://developer.android.com/guide/app-bundle

## Authentication And Accounts

### Current Recommendation

Use Firebase Authentication for Google sign-in, email/password, phone verification/recovery, account linking, and future Apple sign-in.

### Required Product Constraints

- Account deletion must be supported in-app before store launch.
- iOS must support Sign in with Apple if the app offers third-party login options that trigger Apple parity rules.
- Phone verification needs abuse controls, quotas, region policy, and test numbers.
- Contacts should not be uploaded in MVP; prefer share links and invitations first.

Sources:

- Firebase Auth: https://firebase.google.com/docs/auth
- Firebase Apple Auth: https://firebase.google.com/docs/auth/ios/apple
- Firebase phone auth: https://firebase.google.com/docs/auth/android/phone-auth
- Apple account deletion: https://developer.apple.com/support/offering-account-deletion-in-your-app/
- Apple App Review Guidelines: https://developer.apple.com/app-store/review/guidelines/

## Permissions, Privacy, And UGC

### Current Recommendation

Request the smallest permissions possible, just in time. Use foreground location only for MVP. Public map data should use fuzzy geohashes, clustering, delays, or opt-in exact sharing.

### Launch-Blocking Requirements

- Privacy policy and data deletion policy.
- Google Play Data Safety and Apple App Privacy labels.
- Camera, location, photo, and contact permission purpose strings.
- UGC report, block, hide/delete, moderation review, community guidelines, and abuse response process.
- EXIF handling policy; strip exact GPS EXIF from public images unless explicitly needed and consented.

Sources:

- Android permissions minimization: https://developer.android.com/privacy-and-security/minimize-permission-requests
- Android location permissions: https://developer.android.com/develop/sensors-and-location/location/permissions
- Google Play UGC policy: https://support.google.com/googleplay/android-developer/answer/9876937
- Google Play user data policy: https://support.google.com/googleplay/android-developer/answer/10144311
- Apple App Privacy Details: https://developer.apple.com/app-store/app-privacy-details/

## Maps And Geospatial

### Current Recommendation

Prototype Mapbox and Google Maps Platform before final commitment. Use PostgreSQL/PostGIS for backend geospatial truth regardless of client map provider.

### Decision Pressure

- Mapbox may fit custom game-like map styling well.
- Google Maps Platform may offer strong place, route, and realistic map data.
- Public animal maps should show clustered/blurred activity, not exact coordinates by default.
- Use Places/OSM/curated geofences for zoo detection, but do not rely on one source only.

Sources:

- Mapbox Flutter Maps: https://docs.mapbox.com/flutter/maps/guides/
- Google Routes API: https://developers.google.com/maps/documentation/routes
- Google Map Tiles API: https://developers.google.com/maps/documentation/tile
- PostGIS: https://postgis.net/
- OpenStreetMap zoo tagging: https://wiki.openstreetmap.org/wiki/Tag:tourism%3Dzoo

## Database, Storage, And Search

### Current Recommendation

Use PostgreSQL as the core transactional database, with PostGIS for geospatial queries and pgvector for similarity matching. Use object storage for photos and generated media derivatives.

### Why

- Leaderboards, friendships, groups, posts, comments, privacy, audits, and score events are relational.
- Animal sightings need geospatial indexes and privacy-safe region aggregation.
- Duplicate matching needs perceptual hashes, embeddings, and approximate similarity search.
- Photos should not live in the relational database.

Sources:

- Firebase Data Connect: https://firebase.google.com/docs/data-connect
- Cloud SQL PostgreSQL extensions: https://cloud.google.com/sql/docs/postgres/extensions
- pgvector: https://github.com/pgvector/pgvector
- Cloud Storage for Firebase: https://firebase.google.com/docs/storage

## AI And Animal Knowledge

### Current Recommendation

Use a hybrid scoring pipeline: deterministic prechecks, duplicate matching, zoo/geofence matching, species candidates, image embeddings, then LLM vision structured scoring. Human review handles uncertain or high-impact cases.

### Candidate Knowledge Sources

- LLM vision for flexible interpretation and aesthetics.
- Google Cloud Vision for baseline labels/object signals.
- iNaturalist/GBIF-style species data for taxonomy and rarity support.
- Internal scoring rules and benchmark datasets for consistency.

Sources:

- OpenAI vision/image inputs: https://platform.openai.com/docs/guides/images-vision
- OpenAI structured outputs: https://platform.openai.com/docs/guides/structured-outputs
- Google Cloud Vision: https://cloud.google.com/vision/docs
- GBIF API: https://techdocs.gbif.org/en/openapi/
- iNaturalist API: https://api.inaturalist.org/v1/docs/

## Knowledge Workflow

### Current Recommendation

Use `docs/` for human-readable planning and governance. Use `knowledge/okf/` for structured machine-readable summaries. Treat the repository as an Obsidian vault by keeping Markdown links and indexes. Add Graphify/code-graph generation after code exists.

Sources:

- Open Knowledge Format article: https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing
- Obsidian Help: https://help.obsidian.md/
- Graphify: https://graphify.net/
