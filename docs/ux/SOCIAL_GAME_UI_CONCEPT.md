# V2 Social Game UI Concept

## Purpose

This is a high-level product and UI concept pass for **PakimonGO V2**, grounded
in the archived project conversations and the V1 screenshot set under
`docs/assets/COMPLETE UI SCREENSHOTS - V1/`.

The generated V2 concept panels are organized in
`docs/assets/V2 UI CONCEPT PANELS/README.md`.

A hardcoded HTML/CSS planning prototype is available at
`docs/prototypes/v2-ui-html/index.html`.

It is not yet an implementation spec and does not replace
`docs/REQUIREMENTS.md` or `docs/TRACEABILITY_MATRIX.md`. Treat this as the
brainstorming bridge between V1 prototype screens and a future V2 design system.

The goal is to bring back the original game feeling: a real-animal discovery
game with the energy of a map adventure, the collection satisfaction of a field
guide, and the social loop of modern photo apps, while keeping animal safety,
privacy, moderation, and score fairness as hard limits.

## V2 Framing

V1 proves the app can run and the core flows exist. V2 should make the same
product feel like a real game:

- More alive on first open.
- More photo-forward.
- More social.
- More rewarding after each capture.
- More legible outdoors.
- More expressive without becoming unsafe or spammy.

V2 is not "add more screens." V2 is a redesign around the core loop:

```txt
Explore map -> capture animal -> submit context -> reveal score -> collect card
-> share safely -> compete with friends/groups -> get next mission
```

## Archive-Derived Product Intent

The original idea was not just "take animal photos." It was:

- Android first, iOS later.
- Phone camera plus game-like live map.
- Real-life animal photos become scored discoveries.
- Score is a surprise after submit, not client-controlled.
- Rarity, image quality, aesthetic/artistic value, names, captions, context,
  duplicate checks, zoo/captive handling, and pet ownership all matter.
- Zoo photos save to the collection, but do not earn normal wild score.
- Honest zoo disclosure can earn tiny capped participation credit.
- Same animal should not be farmed repeatedly unless it materially changes.
- Friends, contacts/invites, groups, captions, likes, comments, reposts,
  shares, hashtags, collection pages, and social competition are part of the
  long-term game.
- Leaderboards should support global, country, local, and friends scopes.
- New users should not feel hopeless; high-score users should need better,
  safer, rarer, or more creative discoveries.
- Public map activity must never expose risky exact animal or home locations.
- The project must stay agent-friendly: state docs, backlog, QA gates, and
  handoff notes are part of the product workflow.

## V1 Screenshot Audit

Visual baseline reviewed from:

- `docs/assets/COMPLETE UI SCREENSHOTS - V1/Screenshot 2026-07-06 041459.png`
- `docs/assets/COMPLETE UI SCREENSHOTS - V1/Screenshot 2026-07-06 041511.png`
- `docs/assets/COMPLETE UI SCREENSHOTS - V1/Screenshot 2026-07-06 041542.png`
- `docs/assets/COMPLETE UI SCREENSHOTS - V1/Screenshot 2026-07-06 041555.png`
- `docs/assets/COMPLETE UI SCREENSHOTS - V1/Screenshot 2026-07-06 041611.png`
- `docs/assets/COMPLETE UI SCREENSHOTS - V1/Screenshot 2026-07-06 041639.png`
- `docs/assets/COMPLETE UI SCREENSHOTS - V1/Screenshot 2026-07-06 041649.png`
- `docs/assets/COMPLETE UI SCREENSHOTS - V1/Screenshot 2026-07-06 041704.png`
- `docs/assets/COMPLETE UI SCREENSHOTS - V1/Screenshot 2026-07-06 041820.png`
- `docs/assets/COMPLETE UI SCREENSHOTS - V1/Screenshot 2026-07-06 041834.png`

### What V1 Already Has

- Strong map-first foundation.
- Bottom navigation that makes the app understandable.
- A large camera action on the map.
- Dark theme and green brand direction.
- Notifications, profile, capture, history, leaderboard, moderation entry points.
- A basic field-guide direction through collection/profile.

### What V1 Feels Like

V1 feels like a working technical prototype: functional, dark, sparse, and
form-heavy. It proves the architecture, but it does not yet feel like a
high-retention game or social app.

### V1 Gaps V2 Should Fix

- Map has sightings, but little sense of quests, habitats, seasons, or social
  life.
- Capture screen is a plain form instead of a dramatic capture/review flow.
- Photo picker result appears as a raw file preview, not a polished capture card.
- History is a list, not a story of discoveries.
- Leaderboard is useful but not competitive enough: no seasons, friend context,
  rank movement, leagues, badges, or comeback goals.
- Notifications are plain rows; V2 can use richer activity cards.
- Profile is mostly settings; V2 profile should be a player identity page.
- Blocked Users error state is functional but visually dead.
- There is no social feed, group surface, story/reel surface, challenge hub, or
  score reveal ceremony.

## External Inspiration Directions

These are inspiration sources, not features to copy directly:

- Pokemon GO: routes, party play, showcases, limited-time competition, map-first
  exploration, and reward loops.
- Instagram: feed, stories, reels, explore recommendations, profile grid,
  hashtags, reactions, comments, and share/repost habits.
- Facebook: groups, group profiles, admin/moderation patterns, community
  identity, and event-style interaction.
- Strava: private group challenges, leaderboards, progress streams, clubs,
  segments, and "compete with friends" loops.
- iNaturalist and Seek: camera identification, observations, community
  identification, species learning, badges, monthly challenges, and nature-first
  credibility.

V2 should combine those directions into something specific to PakimonGO:

```txt
Pokemon GO map energy
+ Instagram photo/social language
+ Strava challenge/club competition
+ iNaturalist/Seek nature learning and badges
+ PakimonGO safety/privacy/scoring rules
```

## V2 North Star

**PakimonGO should feel like a social wildlife adventure app, not a generic
database of photos.**

The first screen should be the game world:

- A close, street-level map.
- Nearby discovery energy.
- A camera action always within reach.
- Social activity visible without revealing exact animal locations.
- Player progress, quests, and rank status clear at a glance.

## Experience Pillars

### 1. Discover

The map is the home screen. It shows privacy-safe activity cells, not exact
public pins. It should feel alive through habitat pulses, recent-safe activity,
season events, and area summaries.

### 2. Capture

The camera flow should feel like catching a moment. The user takes a photo,
adds context, names/captions/tags it, chooses visibility, and submits without
knowing the final score yet.

### 3. Reveal

Scoring should feel like opening a pack or completing a field mission:

- Species guess.
- Wild/pet/zoo/captive status.
- Safety/readability notes.
- Rarity and novelty.
- Aesthetic bonus.
- Name/caption bonus.
- Duplicate or cooldown result.
- Final score reveal with explanation.

### 4. Collect

The collection should feel like a living field guide:

- Species cards.
- Regions/habitats.
- Rarity bands.
- Best photo per species.
- First seen, latest seen, streaks, and variants.
- Private, friends-only, and public shelves.

### 5. Socialize

Social should use familiar photo-app patterns, but with wildlife safety:

- Feed.
- Profile grid.
- Likes/reactions.
- Comments.
- Reposts/shares.
- Hashtags.
- Groups.
- Friend leaderboards.
- Report/block everywhere.

### 6. Compete

Competition should reward safe discovery, not spam:

- Global, country, local, friends leaderboards.
- Seasonal leagues.
- Weekly missions.
- Habitat challenges.
- First-safe-find bonuses.
- Catch-up boosts for new players.
- Diminishing returns for repeated/common/zoo/spam patterns.

## Proposed App Shell

Use a bottom navigation built around the actual game loop:

| Tab | Purpose | Notes |
|---|---|---|
| Map | Live game world | Default first screen. Close street-level map, activity cells, area sheet, waypoint, local missions. |
| Feed | Social discovery stream | Friends, groups, local safe highlights, stories, tags, gated public content. |
| Capture | Camera and draft review | Center tab or floating action. Fastest path in the app. |
| Collection | Personal field guide | Cards, shelves, private/public visibility, species detail, set progress. |
| Rank | Competition hub | Global/country/local/friends, seasons, quests, showcases, rewards. |

Profile should be reachable from avatar in the app bar and from social surfaces,
not consume one of the five primary game tabs unless the tab count must be
reduced for mobile ergonomics.

V2 should consider making Capture the center tab visually, even if Map remains
the first screen. The user should always know: "I can capture something now."

## High-Level Screen Concepts

### Map Home

What it shows:

- 3D/street-biased map.
- Player location only with permission.
- Coarse nearby activity cells.
- Area summary sheet: species seen, activity level, safety notes, top habitats.
- Waypoint to general area, never exact animal pin.
- Floating camera button.
- Quick mission strip: "Find a bird", "Try a night-safe capture", "Complete a local habitat set".

Interesting upgrade ideas:

- Habitat heat rings: park, water, urban, garden, forest.
- "Quiet zones" where sensitive species/location data is hidden.
- Seasonal overlays such as rainy-day sightings or migration week.
- Local event bubbles for safe public parks.
- Route cards: safe walking paths to general habitat areas.
- Squad presence: show nearby friends only in explicit party mode.
- Showcase spots: area-based photo competitions, never exact animal spots.

V2 direction:

- Replace the plain top title area with a compact game HUD: avatar, level,
  streak, current mission, notifications.
- Turn "3 sightings" into an interactive area sheet with species previews,
  habitat type, recent activity, and privacy explanation.
- Keep the large camera button, but make it feel like the primary game action.

### Capture Review

What it shows:

- Photo preview.
- Required context: wild, pet, zoo/captive, unsure.
- Optional name: real name or cute name.
- Caption.
- Hashtags.
- Visibility: private, selected friends, friends, public.
- Location privacy note.
- Submit button with "score reveal pending" behavior.

Interesting upgrade ideas:

- "Respect check" before submit: no chasing, no touching wild animals, no trespass.
- AI hint after photo: "looks like a cat/bird/dog; confirm context."
- Draft streak: "3 safe captures this week."
- Photo-first card: image dominates, fields collapse into guided steps.
- One-thumb submit flow for outdoor use.
- "Private by default" visibility pill.
- Optional "story post" toggle after safe review.

V2 direction:

- Move from form-first to card-first.
- Start with image, then context chips, then name/caption/hashtags, then
  visibility.
- Show disabled submit reasons clearly instead of a quiet disabled button.

### Score Reveal

What it shows:

- Animated result card.
- Species and confidence.
- Context: wild, pet, zoo/captive, unknown, review.
- Score breakdown.
- Collection impact.
- Leaderboard impact.
- Share card action.
- Appeal/report problem action.

Interesting upgrade ideas:

- Reveal tiers: Common, Nice Find, Rare Moment, Legendary Safe Shot.
- "Why this scored" plain-language explanation.
- "Try next" mission generated from result.
- Shareable result card for Feed/Story.
- Collection animation when a new species or personal best is added.
- Friend comparison: "better than your last bird photo" or "new local top 10."
- Fairness banner when zoo/pet/social points are capped.

### Feed

What it shows:

- Mixed social feed of friends, groups, local safe highlights, and followed tags.
- Photo/video-style cards.
- Like/reaction, comment, repost/share, save to inspiration, report/block.
- Visibility label on every post.
- Score/result chip only if allowed by privacy settings.

Instagram/Facebook-like features adapted for PakimonGO:

- Stories: short-lived "Field Stories" from safe captures, hidden exact location.
- Reels-style clips: "Wild Moment" short videos later, only after moderation is ready.
- Reactions: wow, cute, rare, helpful ID, safe shot.
- Comments with safety filters and comment limiting.
- Reposts with original attribution and visibility checks.
- Hashtag pages for species, habitats, challenges, and events.
- Follow/friend activity with invite links before contacts import.
- Group feeds for schools, local nature clubs, families, city teams, or friend squads.
- Explore feed: personalized but explainable discovery recommendations.
- Friends feed: only people the user chose.
- Local highlights feed: coarse-region safe activity.
- Saved/inspiration shelf: captures the user wants to learn from.

Safety gates:

- Public feed stays feature-flagged.
- Every post/comment/profile/group has report/block.
- Comments can be limited or disabled.
- Social score is capped and fraud-damped.
- No social action reveals exact location or sensitive species data.

V2 direction:

- Feed card hierarchy: photo, species/context, score/reveal state, caption,
  safety/location pill, reactions, comment/share/report.
- Give every post a visible privacy label.
- Make "Safe Shot" and "Helpful ID" first-class reactions so social energy
  reinforces good behavior.

### Profile

What it shows:

- Identity header.
- Level, score ledgers, streaks, safe-capture badge.
- Photo grid.
- Collection shelves.
- Public stats toggles.
- Friends/groups.
- Reports/blocked users/settings.

Interesting upgrade ideas:

- "Explorer style" badges: Bird Watcher, Night Listener, Garden Guardian.
- Top 3 captures pinned.
- Best safe shot of the month.
- Friend comparison strip.
- Profile story ring for Field Stories.
- Public shelves: Best Wild, Best Pet, Zoo Journal, Rare Finds, Art Shots.
- Trust/safety badge only when meaningful and not gameable.

V2 direction:

- Profile becomes player identity, not settings.
- Settings move lower or behind a gear icon.
- First viewport: avatar, level, streak, rank, pinned captures, badges.

### Collection

What it shows:

- Field-guide card grid.
- Sort by species, rarity, score, region, date, context.
- Private/public/friends shelves.
- Missing species silhouettes.
- Habitat sets and region sets.

Interesting upgrade ideas:

- "PakiDex" style completion pages, but with original branding.
- Album pages: Pets, Zoo Visits, Backyard Finds, Rare Wild, Best Art Shots.
- Collection quests: complete 5 common safe birds, 3 park animals, 1 water habitat.
- Species card evolution: first seen -> best shot -> rare variant -> region set.
- Completion rings by habitat and region.
- Compare with friends without exposing private captures.

V2 direction:

- Use a photo grid/cards instead of only list rows.
- Let each species feel like a collectible card with score, rarity, context, and
  privacy.
- Empty state should push the player back to Map/Capture with a mission.

### Rank

What it shows:

- Scope switcher: global, country, local, friends.
- Season and all-time tabs.
- Score ledgers: wild discovery, pet/social, participation.
- Rank movement.
- Fairness notes: capped zoo/pet/social score.

Interesting upgrade ideas:

- Weekly leagues with promotion/demotion.
- Friend squad ranking.
- City habitat challenges.
- "Comeback missions" for new/low-score users.
- High-score mastery quests instead of endless common-animal farming.
- Showcases: time-boxed "best safe sparrow", "cutest pet", "best zoo journal",
  "best night-safe photo."
- Score tabs: Wild, Pet/Social, Participation, Overall.
- Rank movement: up/down since yesterday or this week.

V2 direction:

- Rank should feel seasonal and alive.
- Give users a near-term goal even if they cannot touch global top ranks.
- Keep social score visible but bounded so it cannot overpower wild discovery.

### Groups

What it shows:

- Group feed.
- Group quests.
- Member leaderboard.
- Shared collection board.
- Moderators and rules.

Interesting upgrade ideas:

- Park cleanup photo events.
- School/nature club challenges for 13+ users.
- Private family/friend groups.
- Local city teams.
- Group albums.
- Group story ring.
- Group-only leaderboard.
- Admin prompts for rules and moderation.

V2 direction:

- Groups should be the safe way to make PakimonGO social before public feed is
  broad.
- Start with private/invite groups, group quests, and group leaderboards.

## Social Features To Consider Adding

These are candidate features, not accepted requirements yet:

- Field Stories: temporary story posts from recent captures.
- Discovery Reels: short clips from animal moments, later only.
- Challenge cards: weekly missions with clear safe behavior.
- Squad quests: friend group goals.
- Trade-free collection showcases: users can admire, not trade animals.
- Species hashtag hubs.
- Habitat hashtag hubs.
- "Helpful ID" reaction for community learning.
- "Safe Shot" reaction that rewards respectful distance.
- Public profile shelves.
- Post templates for score reveal cards.
- Local event pages for parks or regions.
- Creator-style capture stats, without turning wildlife into clout farming.
- Optional mentor/helper role for trusted wildlife-aware users.
- Party mode: temporary near-friend session with explicit opt-in and privacy
  copy.
- Showcase entries: submit one capture to a time-boxed competition.
- Route missions: safe general-area walks, not exact animal chasing.
- "Ask for ID help" post type where social comments focus on identification.
- "Then vs now" repeated-animal post type only when materially changed.
- Offline field draft queue with later reveal.
- City season pages: Islamabad, Rawalpindi, etc. with privacy-safe stats.
- "Do not disturb" achievement track for respectful-distance captures.

## What Not To Add Yet

Avoid these until moderation, privacy, and operations are mature:

- Direct messages.
- Open public comments for all users by default.
- Public exact map pins.
- Background location.
- Contacts upload as a required growth feature.
- Unbounded social points.
- Any reward for touching, chasing, feeding, baiting, or cornering animals.
- Trading/selling animals or photos as game assets.
- Monetized boosts that affect score fairness.
- Public party location sharing beyond explicit short-lived opt-in.
- Leaderboard mechanics that make players chase animals or trespass.
- AI-generated fake animal posts.
- Infinite algorithmic feed as the first open experience.

## V2 Design Directions To Explore

### Direction A: Map Adventure

Best if the game wants to feel closest to a location adventure.

- First screen is full map.
- Bottom sheet shows current mission and nearby safe activity.
- Capture button floats center-bottom.
- Feed is secondary.
- Strongest for outdoor play and local discovery.

Risk: social features may feel hidden.

### Direction B: Social Wildlife Network

Best if retention should come from friends and posts.

- First screen is Feed with story ring and capture button.
- Map is one tab away.
- Profile grid and reactions matter more.
- Strongest for Instagram/Facebook-like familiarity.

Risk: it can become generic social media and weaken the game identity.

### Direction C: Collection RPG

Best if the fantasy is completing a living field guide.

- First screen shows collection progress, quests, and next missing species.
- Map and capture support the collection journey.
- Cards, badges, rarity, and score reveal become central.

Risk: less immediate "go outside now" energy.

### Recommended V2 Blend

Use **Map Adventure** as the app home, but make Feed and Collection much richer:

```txt
Home = Map Adventure
Retention = Feed + Friends + Groups
Progression = Collection + Rank + Quests
Moment of delight = Score Reveal
Safety = Privacy/moderation gates everywhere
```

## V2 First Wireframe Pack

Before implementation, design these in order:

1. V2 Map Home: HUD, mission strip, activity sheet, capture button.
2. V2 Capture Review: photo-first, context chips, visibility, submit state.
3. V2 Score Reveal: animated card, breakdown, collection/rank impact, share.
4. V2 Feed Card: photo, caption, score chip, location privacy, reactions,
   comments, repost/share, report/block.
5. V2 Profile: player identity, grid, badges, shelves, friends/groups.
6. V2 Collection Card/Grid: species cards, sets, rarity, privacy.
7. V2 Rank Hub: seasons, scopes, quests, showcases.
8. V2 Group Page: feed, quests, member leaderboard, rules.
9. V2 Empty/Error states: visually alive, still accessible.
10. V2 Moderation surfaces: report, block, appeal, content hidden states.

## UI Direction

The UI should feel:

- Field-adventure first.
- Social-photo familiar.
- Bright and energetic, but not childish.
- Fast to scan outdoors.
- Built around camera/map/collection, not settings pages.
- Trustworthy about privacy and scoring.

Visual language:

- Map-first home.
- Large photo cards in feed and collection.
- Strong capture button.
- Compact score chips.
- Rarity/score badges that do not rely only on color.
- Bottom sheets over map for nearby activity.
- Profile grid and shelves for social identity.
- Rank cards with clear scope and season.

## Suggested First UI Design Pass

Do this before building new social code:

1. Wireframe the five-tab V2 shell: Map, Feed, Capture, Collection, Rank.
2. Design one post card with visibility, score, location privacy, reactions,
   comments, repost, share, report, and block.
3. Design one score reveal card.
4. Design one profile page with grid, badges, shelves, friends, and settings.
5. Design one group page.
6. Run a safety review against each screen.
7. Convert approved pieces into requirements and traceability rows.

## Product Rule

Make it super interesting by giving players more reasons to discover, collect,
share, and compete. Keep it safe by making the best strategy also the most
respectful strategy: observe well, do not disturb animals, do not leak exact
locations, and do not farm the system.
