# Agile Backlog

## Backlog Rules

Stories must reference requirement IDs from `docs/REQUIREMENTS.md`. Do not implement a story until it meets Definition of Ready in `docs/SRS.md`.

## Epic: Planning And Architecture

### STORY-0001: Approve SRS Baseline

- Requirements: all current requirements
- As a product owner, I want to review and approve the SRS so implementation starts from shared scope.
- Acceptance: SRS reviewed, open questions logged, and approval/changes recorded.

### STORY-0002: Write Initial ADR Set

- Requirements: NFR-MAINT-003
- As an engineer, I want ADRs for core platform choices so future agents know why decisions exist.
- Acceptance: ADRs exist for mobile, database, maps, auth, AI, storage, privacy, and moderation.

## Epic: Identity

### STORY-0101: Google Sign-In

- Requirements: FR-AUTH-001
- Acceptance: user can sign in with Google and backend verifies token.

### STORY-0102: Email And Password

- Requirements: FR-AUTH-002, FR-AUTH-003
- Acceptance: user can register, sign in, sign out, and reset password.

### STORY-0103: Account Deletion

- Requirements: FR-AUTH-006
- Acceptance: user can request account deletion and system starts deletion workflow.

## Epic: Capture

### STORY-0201: Camera Draft Capture

- Requirements: FR-CAP-001, FR-CAP-002
- Acceptance: user can take a photo, save draft metadata, and retry after app restart.

### STORY-0202: Location At Capture

- Requirements: FR-CAP-002, NFR-PRIV-001
- Acceptance: foreground location is requested just in time and stored privately.

### STORY-0203: Signed Upload

- Requirements: FR-CAP-002, NFR-SEC-002
- Acceptance: photo uploads through scoped signed URL and creates media record.

## Epic: Scoring

### STORY-0301: Score Event Model

- Requirements: FR-SCORE-001, FR-SCORE-002
- Acceptance: score events store formula version and explanation.

### STORY-0302: Zoo Score Cap

- Requirements: FR-SCORE-003, FR-SCORE-004
- Acceptance: zoo-likely submissions save but skip normal leaderboard scoring.

### STORY-0303: Duplicate Edge Detection

- Requirements: FR-SCORE-005
- Acceptance: exact and near-duplicate images create duplicate edges and score caps.

## Epic: Map

### STORY-0401: Privacy-Safe Animal Activity Map

- Requirements: FR-MAP-001, FR-MAP-002, FR-MAP-003
- Acceptance: map shows clustered/fuzzed activity by viewport.

### STORY-0402: Waypoint Route

- Requirements: FR-MAP-004
- Acceptance: user can set a simple waypoint without background location.

## Epic: Social And Moderation

### STORY-0501: Post Visibility

- Requirements: FR-SOC-003
- Acceptance: post can be private, public, friends, or selected friends.

### STORY-0502: Report And Block

- Requirements: FR-SOC-006, FR-MOD-001
- Acceptance: user can report content/user and block another user.

## Epic: Leaderboards

### STORY-0601: Friends Leaderboard

- Requirements: FR-LB-001, FR-LB-005
- Acceptance: user can compare score with accepted friends.

### STORY-0602: Global/Country/Local Leaderboards

- Requirements: FR-LB-002, FR-LB-003, FR-LB-004
- Acceptance: rankings are computed from valid score events and privacy-safe regions.

## Backlog Refinement Needed

- Add story points after architecture decisions.
- Split each story into tasks once code scaffold exists.
- Add UI wireframe links when available.
- Add test cases to each story before sprint commitment.
