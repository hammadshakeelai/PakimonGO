# Session Summary: Social Game UI Concept

## Date

2026-07-06

## User Request

The user asked to read the archived chats, bring out what they originally
thought for the game, add more Instagram/Facebook-like social feature ideas, and
design a high-level UI direction before implementation. The user then clarified
that the work is **V2 design**, and the V1 screenshots live under
`docs/assets/COMPLETE UI SCREENSHOTS - V1/`.

## Archive-Grounded Intent

- Real-animal discovery game inspired by location-based creature games.
- Android APK first, iOS later.
- Camera plus map as core phone features.
- Surprise server-side scoring based on species, rarity, safety, context,
  aesthetics, names/captions, duplicate checks, zoo/captive handling, and pet
  ownership.
- Social features: friends, groups, captions, likes, comments, reposts, shares,
  hashtags, collection pages, and four leaderboard scopes.
- Strong requirement that public map/social features must not expose exact risky
  animal or user locations.
- Full SDLC, QA, handoff docs, and traceability before major implementation.

## Work Completed

- Added and expanded `docs/ux/SOCIAL_GAME_UI_CONCEPT.md` as the V2 concept.
- Audited all 10 V1 screenshots in `docs/assets/COMPLETE UI SCREENSHOTS - V1/`.
- Linked the concept from `docs/ux/UX_FLOW_SPEC.md`.
- Updated state docs to mark the concept as high-level design backlog, not
  accepted implementation scope.
- Added backlog/risk/debt notes for the new social/game UI direction.

## Key Decision

The concept preserves the ambitious full-social target but keeps implementation
behind moderation, privacy, safety, and traceability gates.

## Next Task

Review the V2 concept and choose the first wireframe pack: Map Home, Capture
Review, Score Reveal, Feed Card, Profile, Collection Card/Grid, Rank Hub, Group
Page, Empty/Error states, and moderation surfaces.
