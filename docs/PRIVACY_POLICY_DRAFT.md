# PakimonGO — Privacy Policy (DRAFT)

**Status: DRAFT — not published.** This draft was written directly against
the app's actual data-handling code (not boilerplate) so that every claim
below is something the app genuinely does today. Two things still need to
come from you before this can be published, marked `[TODO]` below:

1. Your **legal entity name** (individual developer name or company name).
2. A **support/privacy contact** (email address or physical address, as
   required by your jurisdiction and by Google Play's Data Safety form).

**This draft has not had a legal review.** Treat it as an accurate
first draft of *what the app does*, not as legal advice or a
store-submission-ready document. Have it reviewed before publishing,
particularly the Children's Privacy and Data Retention sections.

---

## Last updated

`[TODO: date of publication]`

## Who we are

PakimonGO ("we", "us", "the app") is a wildlife-discovery mobile app
operated by `[TODO: legal entity name]`. Contact us at `[TODO: contact
email/address]` with any privacy questions or requests.

## Information we collect

**Account information.** When you sign in with Google, we receive your
email address and a unique account identifier from Firebase Authentication
to create your account. We do not separately store your name or profile
photo in our own database.

**Profile information you provide.** An age band (a bucket, not your exact
birthdate — see "Children's Privacy" below) and an optional free-text home
region you type in yourself (e.g. "Punjab") — this is not derived from your
device's location.

**Photos you submit.** When you capture a wildlife sighting, we store the
photo you upload. A resized, re-encoded copy (with embedded metadata such
as camera EXIF data removed) is what's shown publicly on your profile, in
the feed, and to other users; the original file you uploaded is kept on
our servers for scoring and moderation purposes but is not publicly
accessible.

**Location information.** If you allow location access, we record the
precise GPS coordinates of a capture at the moment you submit it, so we
can verify submissions and support future features. However, **the public
API and app never expose your exact location** — only a coarse,
rounded-off location (roughly 100–150 meters, not your exact spot) is ever
shown to you or to other users, and sensitive-species sightings can be
suppressed from public display entirely.

**Content and social activity.** If you use social features, we store
what you'd expect: who you follow, comments you post, reactions
(emoji-style responses) you leave on captures, and any 24-hour "stories"
you post. This content is visible to other users per the feature's normal
behavior (e.g. a comment you post is visible to people who can see that
capture).

**Moderation reports.** If you report a submission or another user, we
store the report (reason, and any details you provide) and keep an audit
log of moderation actions, so patterns of abuse can be investigated.

**We do not collect:** your exact street address, payment information (the
app has no in-app purchases today), device advertising identifiers, or
browsing history outside the app.

## How we use your information

- To operate your account, show your profile and captures, and let you use
  social features (following, commenting, reacting, stories).
- To score your wildlife submissions — this includes automated image
  classification (see "AI processing" below).
- To keep the community safe — investigating reports, applying
  moderation actions, and maintaining an audit trail of those actions.
- To communicate with you about your account and submissions, via
  in-app notifications. **We do not currently send push notifications**;
  notifications only appear when you open the app.

## AI processing of your photos

When you submit a wildlife photo, its image data is sent to a third-party
AI vision service to identify the species and context (e.g. wild vs. a
zoo/pet setting) and to help detect duplicate or manipulated images. The
app currently uses **Groq** for this; **Google Cloud Vision** is
available as an alternative provider. These providers process the image
to return a classification result — refer to their own privacy policies
for how they handle data submitted to their APIs.

## Third-party service providers

We share limited data with the following providers, each for a specific
purpose:

| Provider | What it receives | Why |
|---|---|---|
| **Firebase (Google)** | Email address, sign-in identifier | Account authentication |
| **Groq** (or Google Cloud Vision) | The photo you submit | Automated species/context classification |
| **Mapbox** | Map viewport/tile requests | Rendering the in-app map |
| **Render / cloud hosting** | All app data, in transit and at rest | Running the backend service |

We do not sell your personal information to third parties, and we do not
use your data for third-party advertising.

## Children's privacy

The app is intended for users **13 and older**. New accounts pass through
an age check before using the app; users who indicate they are under 13
are not permitted to create an account. Users aged 13–17 are recorded in
a "teen" age band, distinct from adults, for future age-appropriate
handling — `[TODO: describe any additional protections applied to teen
accounts today, or state that none currently differ, before publishing]`.

## Data retention and account deletion

You can permanently delete your account at any time from Profile →
"Delete My Account." When you do:

- Your account is deactivated and your profile information (age band,
  home region) is erased.
- If you signed in with Google, we make a best-effort attempt to revoke
  that sign-in method so it can't be reused.
- **Your past captures, comments, and reactions are not deleted** — they
  remain attached to a deactivated account rather than being removed
  outright. We do this because your content may be visible in other
  users' comment threads or reaction history, and outright deletion could
  break or misrepresent that shared context. If you would like your past
  content removed as well, contact us at `[TODO: contact email]`.
- **Uploaded photos are not automatically deleted from server storage**
  when you delete your account. `[TODO: decide and disclose the actual
  retention/deletion timeline for photo storage before publishing —
  this is a real gap, not yet built, see docs/BUGS_AND_RISKS.md.]`

Account deletion is immediate and cannot be undone through the app itself.

## Your rights

Depending on where you live, you may have rights to access, correct, or
request deletion of your personal data beyond what the in-app deletion
flow covers. Contact us at `[TODO: contact email]` to make such a request.

## Security

We take reasonable measures to protect your information, including
validating uploads (file type and size checks), and restricting sensitive
data (exact location, original photo files) from public API access. No
online service can guarantee perfect security.

## Moderation and safety

Users can report submissions or other users, and can block users they
don't want to interact with. Reports are reviewed and audited; repeated
or severe violations may result in account restrictions. A full
moderator review console and formal appeals process is planned but not
yet built — see our public roadmap for status.

## Changes to this policy

We may update this policy as the app changes. `[TODO: describe how you'll
notify users of material changes before publishing.]`

## Contact us

`[TODO: contact email/address]`
