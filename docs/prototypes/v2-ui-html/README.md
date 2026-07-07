# PakimonGO V2 HTML/CSS Prototype

This folder contains a static planning prototype for PakimonGO V2.

Open `index.html` in a browser to review the canonical clickable prototype.
It is a single phone app shell that renders real HTML/CSS screens from dummy
JavaScript state:

- Map Home
- Capture Review
- Score Reveal
- Social Feed
- Player Profile
- Field Guide Collection
- Rank Hub
- Group Page
- Notifications
- Empty/Error State

The prototype is based on the generated concept panels in
`docs/assets/V2 UI CONCEPT PANELS/`, but it does not place those screenshots as
full-screen images. It rebuilds the look with cards, chips, forms, tabs,
bottom navigation, modals, toasts, and dummy data.

The current polish pass makes the dummy app feel more like a real V2 shell:
map HUD, mission card, nearby activity sheet, capture safety review, score
reveal, feed reactions, profile/grid surfaces, group tabs, notification
filters, collection filters, rank scopes, and empty/offline recovery are all
represented as hardcoded interactions.

It is intentionally not wired to the Flutter app, the API, authentication,
scoring, or persistence.

Use this prototype to choose the V2 product direction before promoting any
screen into requirements, traceability rows, Flutter work packages, or backend
social feature scope.

## Files

| File | Purpose |
|---|---|
| `index.html` | Canonical prototype entry point. |
| `style.css` | V2 visual system, phone frame, cards, map, forms, grids, modals, and responsive layout. |
| `app.js` | Dummy state, route rendering, button actions, tabs, chips, modals, and toasts. |

Older saved HTML experiments in this folder are not the canonical prototype.
Use `index.html`.

## Design Guardrails

- Treat the UI as concept-only until product review accepts the scope.
- Keep exact location privacy visible in map, feed, score, and profile surfaces.
- Keep report/block/moderation controls visible anywhere user-generated social
  content appears.
- Do not use this prototype as proof that V2 social features are implemented.
- Treat cropped concept-panel textures as temporary visual references. Replace
  them with real approved app assets before production design or Flutter work.
