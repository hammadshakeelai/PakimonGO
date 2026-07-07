# Current Thinking

## Working Thesis

PakimonGO has moved from "code-complete prototype" to **demoable alpha
candidate**, but it is not production-ready.

The strongest current evidence is practical, not theoretical: the backend has
been deployed to Render, Postgres migrations apply there, `/health/*` and
`/v1/users/me` were smoke-verified, and a full Android emulator walkthrough
found and fixed real UI crashes that the mock-heavy tests missed.

## Honest Assessment

**What is real now:** local dev works, the Render backend is live, Render
Postgres has been exercised, Firebase Google sign-in has been live-verified on
a real phone, Groq vision has been live-verified, Mapbox renders in the emulator,
age gate/onboarding exist, user-facing report/block flows exist, and the app has
basic dark mode and improved map/profile navigation.

**What is not real yet:** there is no iOS build, no automated real-device E2E
suite, no durable production object storage, no moderator console or appeals
workflow, no privacy policy/terms, no app-store package, no production release
Firebase SHA-1, no push notifications, and no persistent scoring queue.

**Testing posture:** the latest task log records 145 backend tests, 69 scoring
tests, 162 Flutter tests, and clean Flutter analysis. Treat those as the last
recorded full-suite counts unless you re-run the suites in the current turn.
This repo can still hide issues behind mocks; the emulator walkthrough already
proved that.

## Key Insight

The main risk is no longer "the prototype is secretly only fake providers."
Some real providers are wired and live-verified. The sharper risk now is
overstating alpha/demo readiness as store readiness.

Future agents should distinguish carefully between:

- **Demoable:** yes, with known config and current caveats.
- **Alpha candidate:** close, if release auth and device checks are handled.
- **Beta/production:** no, because moderation operations, E2E, storage,
  legal/store materials, and iOS remain incomplete.

## Near-Term Bias

Prefer grounded hardening over new features:

- Treat `docs/ux/SOCIAL_GAME_UI_CONCEPT.md` as a high-level design concept,
  not implementation scope, until the user approves which parts become
  requirements.
- Accessibility pass before cosmetic expansion.
- Loading states after accessibility basics.
- Real-device E2E before any claim of beta readiness.
- Moderator console/appeals before wider UGC exposure.
- Durable storage before treating deployed media as production-safe.

## Product Direction Note

Archived chats make the target experience bigger than the current prototype:
map-first animal discovery, camera capture, surprise scoring, collections,
friends, groups, feeds, likes, comments, reposts, hashtags, leaderboards, and
social identity. The right path is not to bolt these onto the app blindly. The
right path is to design the social/game UI first, then promote approved pieces
into traceable requirements behind moderation, privacy, and safety gates.

## V2 Design Note

The project is now in a V2 design brainstorm, using
`docs/assets/COMPLETE UI SCREENSHOTS - V1/` as the visual baseline. V1 proves
the flows; V2 should define the experience: map adventure, photo-first capture,
score reveal, social feed, profile identity, collection cards, quests, groups,
and seasonal competition.

The downloaded V2 concept panels are organized in
`docs/assets/V2 UI CONCEPT PANELS/`, and the clickable HTML/CSS/JS planning
prototype is in `docs/prototypes/v2-ui-html/index.html`. Treat both as design
materials only until specific V2 ideas are promoted into requirements and
traceability.

The prototype now has a richer dummy app shell: map HUD, nearby activity sheet,
capture safety review, score reveal, social feed reactions, profile and
collection grids, group quests, notification filters, rank scopes, modals, and
offline/error recovery. These interactions are intentionally fake so the team
can judge the V2 feeling before committing to Flutter/backend scope.
