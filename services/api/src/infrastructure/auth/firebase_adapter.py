from __future__ import annotations

from collections.abc import Callable

from .adapter import UserContext


class FirebaseAuthAdapter:
    """Verifies Firebase ID tokens via the Firebase Admin SDK.

    Activated with ``AUTH_PROVIDER=firebase``. The Admin SDK reads service-account
    credentials from ``GOOGLE_APPLICATION_CREDENTIALS``. A custom ``verifier`` can be
    injected (returns a claims dict) so the adapter is unit-testable without the
    ``firebase-admin`` dependency or live credentials.
    """

    def __init__(self, verifier: Callable[[str], dict] | None = None) -> None:
        self._verifier = verifier

    def _default_verifier(self, token: str) -> dict:
        import firebase_admin
        from firebase_admin import auth as fb_auth

        try:
            firebase_admin.get_app()
        except ValueError:
            firebase_admin.initialize_app()
        return fb_auth.verify_id_token(token)

    def verify_token(self, token: str) -> UserContext:
        verify = self._verifier or self._default_verifier
        try:
            claims = verify(token)
        except Exception as exc:  # invalid/expired token, SDK/network error
            raise PermissionError("Invalid or expired Firebase token") from exc

        uid = claims.get("uid") or claims.get("user_id") or claims.get("sub")
        if not uid:
            raise PermissionError("Firebase token missing uid claim")
        return UserContext(
            user_id=uid,
            email=claims.get("email"),
            auth_provider="firebase",
        )
