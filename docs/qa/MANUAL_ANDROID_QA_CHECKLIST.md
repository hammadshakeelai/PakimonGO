# Manual Android QA Checklist

## Purpose

Manual Android QA proves real phone behavior that unit tests cannot cover: install, permissions, camera, network loss, battery, accessibility, and low-end performance.

## Device Matrix

Test at least:

| Device Class | Example Target |
|---|---|
| low-end Android | older 4-6 GB RAM device |
| mid-range Android | common current device |
| emulator | API level used by CI/dev |
| tablet/foldable smoke | layout sanity only |

Record Android version, device model, app build, commit, and tester.

## Install And Launch

- Install APK from a clean device.
- Upgrade over previous APK.
- Launch cold after force-stop.
- Launch without network.
- Launch after clearing app data.
- Confirm no debug secrets or internal endpoints are visible.

## Permissions

- Camera permission granted.
- Camera permission denied.
- Location permission granted while in use.
- Location permission denied.
- Permission changed from system settings while app is backgrounded.
- Contacts permission is not requested in Alpha-0.
- Background location is not requested in Alpha-0.

## Capture Flow

- Open capture screen.
- Take photo.
- Cancel capture.
- Create local draft.
- Kill and restart app; draft remains or failure is explained.
- Submit draft with network.
- Submit draft during network loss; retry works.
- Submit with location denied; app follows limited/private policy.
- Oversized/corrupt media shows clear error.

## Privacy Checks

- Public preview does not show exact GPS.
- EXIF GPS is stripped from public derivative.
- Private capture remains private by default.
- Zoo/pet/private state label is visible where expected.
- Sensitive-location explanation appears without leaking exact data.

## Accessibility

- Screen reader can reach primary controls.
- Touch targets are usable.
- Text scale does not overlap key controls.
- Color is not the only state indicator.
- Reduced motion does not break navigation.
- Map has list fallback or accessible alternative.

## Performance And Battery

- Cold start target: p95 <= 3s mid-range, block if >4s.
- Capture-to-draft creation feels immediate.
- Upload retry does not create duplicates.
- 15-minute map/capture smoke drains <=5% target on mid-range.
- Camera and GPS stop when leaving flow.

## Evidence

For every manual run, save:

- build ID and commit hash
- device info
- pass/fail checklist
- screenshots for failures
- crash logs if any
- exact reproduction steps
