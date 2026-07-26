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
        import os

        # Credential-free path for hosts without a service-account file
        # (e.g. Render): ID tokens are verified against Google's public
        # certs — only the Firebase project id is needed, and that is
        # not a secret.
        project_id = os.getenv("FIREBASE_PROJECT_ID")
        if project_id and not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
            from google.auth.transport import requests as g_requests
            from google.oauth2 import id_token as g_id_token

            return g_id_token.verify_firebase_token(
                token, g_requests.Request(), audience=project_id
            )

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


def revoke_firebase_user(user_id: str) -> None:
    """Best-effort: delete the Firebase Auth account on account deletion, so
    the same sign-in can't be reused and Firebase-side profile data (email,
    display name, photo) is removed too.

    No-op unless AUTH_PROVIDER=firebase *and* a service account is
    configured - the credential-free verifier path above (project-id-only,
    used on hosts like Render without GOOGLE_APPLICATION_CREDENTIALS) has no
    admin privileges to delete a user with, so there is nothing to call.
    Never raises: this must not block the DB-side deletion that already
    happened by the time this runs.
    """
    import os

    if os.environ.get("AUTH_PROVIDER", "fake").lower() != "firebase":
        return
    if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
        return
    try:
        import firebase_admin
        from firebase_admin import auth as fb_auth

        try:
            firebase_admin.get_app()
        except ValueError:
            firebase_admin.initialize_app()
        fb_auth.delete_user(user_id)
    except Exception:  # noqa: BLE001
        pass
