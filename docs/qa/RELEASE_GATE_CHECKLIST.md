# Release Gate Checklist

## Purpose

Each release ring must prove the right level of quality before exposure expands. A gate can pass, fail, or pass with documented blocker and owner only when the blocker is not P0.

## Ring 0: Local Developer/Staging

- [ ] `python tools\qa\validate_docs.py` passes.
- [ ] `python tools\qa\scan_secrets.py` passes.
- [ ] Flutter shell tests pass when mobile scaffold exists.
- [ ] API/worker pytest suites pass when backend scaffold exists.
- [ ] Public DTO privacy tests exist before public endpoints.
- [ ] Score state tests exist before score finalization.
- [ ] State docs identify next task and blockers.

## Ring 1: Internal APK

- [ ] APK installs on clean Android device.
- [ ] App launches cold and warm.
- [ ] Age gate works.
- [ ] Camera permission is just-in-time.
- [ ] Location permission is foreground-only.
- [ ] Contacts permission is not requested.
- [ ] Capture draft can be created.
- [ ] Upload retry does not duplicate.
- [ ] Private collection shows pending/scored/capped/review state.
- [ ] No exact public location surface exists.
- [ ] Crash reporting/dev diagnostics are configured without secrets.
- [ ] Manual Android QA checklist is attached to release notes.

## Ring 2: Invited Android Alpha

- [ ] Firebase Auth/App Check/integrity posture is validated.
- [ ] Privacy DTO suite passes.
- [ ] Upload suite passes.
- [ ] Score state suite passes.
- [ ] Basic duplicate and zoo cap/review checks exist.
- [ ] Report/block/hide/delete exist if social is exposed.
- [ ] Feature flags can disable map/social/leaderboard quickly.
- [ ] P0/P1 bugs have owners and SLAs.

## Ring 3: Closed Play Testing

- [ ] Play Console data safety draft is consistent with implemented data flows.
- [ ] Signed AAB build process is documented.
- [ ] Dependency audit and secret scan pass.
- [ ] Accessibility smoke test passes.
- [ ] Low-end Android manual QA passes.
- [ ] Battery smoke test is recorded.
- [ ] Store-review demo path exists if needed.

## Ring 4: Open Beta With Limited Public Social

- [ ] Moderation queue is operational.
- [ ] Reports, blocks, appeals, takedowns, and restoration are audited.
- [ ] Public feed is gated and can be disabled.
- [ ] Sensitive species policy is enforced.
- [ ] Local map/leaderboard privacy thresholds are enforced.
- [ ] Abuse test suite covers bot uploads, collusive likes, reposts, GPS spoofing.
- [ ] Incident response runbooks exist.

## Ring 5: Android Production

- [ ] P0 and P1 tests pass.
- [ ] Load test meets beta/production targets.
- [ ] Backup/restore and deletion/export workflows are tested.
- [ ] Observability alerts exist for API errors, queue backlog, scoring latency, upload failures, location leak class.
- [ ] Legal/privacy review is complete for enabled regions.
- [ ] App-store privacy labels and UGC policy are complete.
- [ ] Rollback plan for each feature flag and release artifact is documented.

## Ring 6: iOS TestFlight

- [ ] iOS compile spike passes.
- [ ] Sign in with Apple exists if Google login is offered.
- [ ] iOS permission copy and Info.plist strings are reviewed.
- [ ] Camera/location/manual QA is repeated on iOS.
- [ ] Apple privacy nutrition details match data flows.

## Ring 7: iOS Production

- [ ] TestFlight feedback is resolved or triaged.
- [ ] iOS crash-free and performance targets pass.
- [ ] iOS moderation/privacy/social gates match Android.
- [ ] Production support and rollback are ready.

## Gate Evidence Template

```txt
Release Ring:
Build/Commit:
Date:
Owner:
Gate Result:
P0 Failures:
P1 Failures:
Tests Run:
Manual QA Evidence:
Risks Accepted:
Rollback Plan:
Next Ring Approval:
```
