# Sprint 30 Plan: Auth/Onboarding UI

## Sprint Goal

Create a login/onboarding screen that stores auth tokens and wires them to the API client, so users can sign in before capturing wildlife.

## Sprint Status

Complete.

## Sprint Backlog

| ID | Status | Task | Acceptance | Verification |
|---|---|---|---|---|---|
| S30-001 | Done | Create `AuthService` (token storage/retrieval) | ChangeNotifier with loginWithUserId, loginWithToken, logout, isAuthenticated, listener notification | 8 unit tests pass |
| S30-002 | Done | Update `ApiClient` to use dynamic token provider | Accepts `String Function()` token provider instead of fixed string; all endpoints use runtime token | Existing 10 client/repo tests pass |
| S30-003 | Done | Create `LoginScreen` UI | User ID entry + token paste mode; Sign In button; calls AuthService; verifies with getProfile | 5 widget tests pass |
| S30-004 | Done | Create `AuthGate` + update main.dart routing | Shows LoginScreen when unauthenticated, HomeScreen after login; logout button in app bar | App navigates correctly |
| S30-005 | Done | Write tests for auth flow | AuthService unit tests (8) + LoginScreen widget tests (5) | 13 new auth tests, 42 total Flutter tests pass |

## File Ownership

| Area | Owner | Notes |
|---|---|---|
| `lib/core/auth/auth_service.dart` | Mobile agent | ChangeNotifier for token state |
| `lib/core/network/api_client.dart` | Mobile agent | Updated to tokenProvider pattern |
| `lib/features/auth/presentation/login_screen.dart` | Mobile agent | Login UI with user ID / token modes |
| `lib/main.dart` | Mobile agent | AuthGate routing, API client wiring |
| `test/core/auth/auth_service_test.dart` | Mobile agent | 8 unit tests |
| `test/features/auth/login_screen_test.dart` | Mobile agent | 5 widget tests |
