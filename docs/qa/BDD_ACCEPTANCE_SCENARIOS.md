# BDD Acceptance Scenarios

## Purpose

These scenarios describe user-visible behavior in plain language. They should become E2E, integration, manual QA, or acceptance tests as the app grows.

## Capture And Upload

```gherkin
Feature: Private animal capture

  Scenario: First-time user captures a private animal draft
    Given a signed-in 13+ user has accepted current policies
    And camera permission is granted
    When the user opens capture and takes a photo
    Then a local draft is created before upload
    And the default visibility is private
    And no final score is shown yet

  Scenario: Draft survives app restart
    Given a user has an unsubmitted capture draft
    When the app is killed and restarted
    Then the draft is still available or a clear recovery message is shown

  Scenario: Upload retry does not duplicate submission
    Given a user has a capture draft
    And the first upload completion request times out
    When the app retries with the same idempotency key
    Then only one media asset is completed
    And only one submission can be created from that upload intent
```

## Location And Privacy

```gherkin
Feature: Privacy-safe location handling

  Scenario: Public map never exposes exact capture coordinates
    Given a public animal post has exact private coordinates
    When another user requests map activity for the viewport
    Then the response contains only a privacy-safe cell
    And the response does not contain latitude or longitude fields

  Scenario: Location permission denied still allows private capture
    Given a user denies foreground location
    When the user submits a private animal photo
    Then the submission is saved
    And scoring is limited or marked policy-dependent
    And the user sees a plain-language explanation

  Scenario: Sensitive species location is suppressed
    Given an identified taxon is sensitive in the region
    When public map activity is generated
    Then the exact location is suppressed or coarsened
    And the public response includes only a safe reason label
```

## Zoo, Pet, Duplicate, And Score

```gherkin
Feature: Score eligibility

  Scenario: Honest zoo disclosure saves the image but caps score
    Given a user marks the animal context as zoo/captive
    When the submission is scored
    Then the photo appears in the user's collection
    And normal wild leaderboard score is not awarded
    And tiny bounded participation credit may be awarded

  Scenario: Same file duplicate cannot farm score
    Given a user has already submitted a photo
    When the same file is uploaded again
    Then the duplicate relationship is stored
    And the second submission does not earn normal score

  Scenario: Unsafe animal interaction triggers review
    Given the submitted media or caption suggests chasing, feeding, touching, or disturbing a wild animal
    When prechecks complete
    Then the score state becomes review or rejected
    And the submission is not eligible for leaderboard ranking
```

## Social And Moderation

```gherkin
Feature: Gated social exposure

  Scenario: Blocked user cannot see restricted content
    Given Alice blocks Bob
    And Alice has a friends-only post
    When Bob requests Alice's feed or post detail
    Then the response does not reveal the restricted post

  Scenario: Public feed remains off until moderation gate passes
    Given public feed feature flag is disabled
    When a user requests public feed
    Then the API returns unavailable or empty gated state
    And no unmoderated public content is exposed

  Scenario: Report creates auditable moderation case
    Given a user can view a post
    When the user reports the post
    Then a moderation case is created
    And the report action is auditable
```

## Leaderboards And Rollback

```gherkin
Feature: Fair leaderboard ranking

  Scenario: Quarantined score does not rank
    Given a submission score is quarantined for risk review
    When leaderboard projection runs
    Then the score is excluded from all leaderboard scopes

  Scenario: Score rollback updates projections
    Given a scored submission appears on a leaderboard
    When a moderator rolls back the score
    Then an immutable adjustment event is recorded
    And all affected leaderboard projections remove or adjust the points
```

## Account And Consent

```gherkin
Feature: Account safety

  Scenario: Under-13 user cannot continue into normal account creation
    Given the app displays a neutral age gate
    When the user selects an under-13 age band
    Then normal account creation is blocked or diverted

  Scenario: Policy update blocks posting until accepted
    Given a user accepted an older policy version
    And a newer policy version requires acknowledgement
    When the user tries to post
    Then the app requires policy acknowledgement before posting
```
