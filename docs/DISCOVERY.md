# Discovery Notes

## Product Shape

PakimonGO is a location-aware animal photography game and social network. The fun loop is: discover animals, take a real photo, submit attributes, receive a surprise score, grow a collection, and compare progress with friends and wider leaderboards.

The product must avoid encouraging unsafe animal behavior. The game should reward respectful observation, accurate identification, honest context, artistic capture, and community value. It should not reward chasing, disturbing, baiting, unsafe petting, or exploiting captive animals.

## Primary Users

- Casual players who want a playful outdoor photo game.
- Animal lovers who want collections and cute names.
- Competitive users who care about score, rarity, streaks, and leaderboards.
- Social users who want friends, groups, captions, likes, reposts, and comments.
- Explorers who want map discovery and waypoint navigation.

## Core Product Questions

- How can the app score animal photos without being unfair, unsafe, or easy to abuse?
- How can the app identify the same animal without punishing legitimate new encounters?
- How can zoo photos be saved but not farmed for leaderboard advantage?
- How can public map discovery stay useful without exposing sensitive locations?
- How can new users catch up while high-score users still feel challenged?
- How can AI agents continue the project later without losing decisions and context?

## Major Constraints

- Android installable package is first priority, but iOS must not require a full rewrite later.
- All scoring, moderation, duplicate checks, and leaderboard writes must happen server-side.
- Public location sharing must be privacy-preserving by default.
- The codebase must be modular and small-file oriented for human and AI maintainability.
- Product, process, and technical knowledge must be stored in Markdown and structured OKF-style files.

## Initial Technology Direction

- Mobile: Flutter for Android-first delivery and later iOS reuse.
- Auth: Firebase Authentication for Google, email/password, phone-based flows, and future Apple sign-in.
- Backend: API service plus Firebase/App Check integration.
- Database: PostgreSQL with PostGIS and pgvector for relational, geospatial, and similarity matching.
- Storage: object storage for original photos, thumbnails, moderation crops, and AI artifacts.
- Maps: Mapbox or Google Maps Platform, validated by prototype and cost analysis.
- AI: hybrid scoring with deterministic prechecks, embeddings, species tools, and LLM vision structured outputs.

## Discovery Exit Criteria

- Purified prompt stored.
- Major assumptions recorded.
- Key external constraints researched.
- Requirements derived and traceable.
- SRS drafted before implementation starts.
