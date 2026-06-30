# Mobile Apps

Mobile code lives here. The first target is a Flutter app that can produce an Android APK for internal testing and later an Android App Bundle and iOS/TestFlight build.

Primary constraints:

- Camera and location permissions are just-in-time.
- Final score and leaderboard writes are never client-side.
- Exact capture coordinates are not exposed through UI or logs.
- Feature folders should stay small and testable.
