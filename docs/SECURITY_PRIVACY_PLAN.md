# Security And Privacy Plan

## Security Goals

- Protect accounts, photos, exact locations, social graph, and scoring integrity.
- Prevent client-side score manipulation.
- Limit abuse from bots, GPS spoofing, duplicate farming, and social brigading.
- Meet Android and iOS privacy expectations before launch.

## Sensitive Data

- Photos and thumbnails.
- Exact capture coordinates.
- EXIF metadata.
- User identity and auth providers.
- Email and phone number.
- Contacts-derived friend matches, if ever enabled.
- Friend graph and groups.
- Comments, captions, reports, blocks, moderation history.
- AI outputs and scoring evidence.

## Privacy Defaults

- Exact location private by default.
- Public map uses blurred cells, clusters, or delayed locations.
- Contacts access is not part of MVP; prefer invite links.
- Background location is not part of MVP.
- EXIF GPS is stripped from public media derivatives.
- Private captures remain private unless user explicitly publishes.

## Authentication

- Firebase Authentication handles identity providers.
- Backend verifies auth tokens on every protected request.
- Link providers safely to prevent duplicate accounts.
- Support account deletion and data deletion workflow.
- Add Sign in with Apple before iOS release if required by Apple rules.

## App Integrity

- Use Firebase App Check or platform attestation where available.
- Use Play Integrity signals for Android abuse resistance.
- Apply rate limits per account, device, IP range, and behavior pattern.
- Quarantine suspicious score events instead of immediately ranking them.

## API Security

- HTTPS only.
- No secrets in mobile app.
- Authorization checks at service boundaries.
- Idempotency keys for uploads and submissions.
- Audit logs for score changes, moderation actions, account deletion, and admin actions.
- Strict file type and size validation.

## Media Security

- Originals are private.
- Public derivatives are generated after validation/moderation rules.
- Signed upload URLs are short-lived and scoped.
- Storage paths are immutable and non-guessable.
- Malware/content safety scanning should be added before broad public launch.

## Location Security

- Store exact coordinates with restricted access.
- Use PostGIS to derive privacy-safe regions.
- Avoid exact public pins for homes, rare animals, or sensitive areas.
- Apply GPS accuracy thresholds.
- Detect impossible travel speed and mock-location signals.
- Treat spoofing signals as risk evidence, not automatic bans.

## UGC Safety

Required before public launch:

- Report content.
- Report user.
- Block user.
- Hide/delete own content.
- Moderator review queue.
- Community guidelines.
- Terms of service.
- Privacy policy.
- Appeals or support contact.

## Children And Minors

The app may attract children because of game-like mechanics and animals. The project must decide whether it targets children.

If targeting children:

- COPPA/Families/Kids Category obligations become major scope.
- Location, contacts, social sharing, ads, analytics, and UGC need stricter limits.

If not targeting children:

- Avoid child-directed marketing.
- Add age gate if legal review requires it.
- Keep safety and privacy strong regardless.

## Threat Model Backlog

- Account takeover.
- Fake uploads.
- GPS spoofing.
- Duplicate/repost farming.
- Zoo farming.
- Collusive likes.
- Harassment in comments/groups.
- Location stalking.
- Pet owner privacy issues.
- Rare animal location exposure.
- AI prompt/output manipulation.
- Admin account compromise.
