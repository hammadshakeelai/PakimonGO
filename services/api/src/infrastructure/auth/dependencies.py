
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from .adapter import AuthAdapter, UserContext
from .fake_adapter import FakeAuthAdapter

_bearer = HTTPBearer(auto_error=False)


def _build_adapter() -> AuthAdapter:
    """Select the auth adapter from AUTH_PROVIDER (default: fake dev adapter)."""
    import os

    provider = os.environ.get("AUTH_PROVIDER", "fake").lower()
    if provider == "firebase":
        from .firebase_adapter import FirebaseAuthAdapter

        return FirebaseAuthAdapter()
    return FakeAuthAdapter()


_adapter: AuthAdapter = _build_adapter()


def get_auth_adapter() -> AuthAdapter:
    return _adapter


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer),
) -> UserContext:
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authorization header",
        )
    try:
        return _adapter.verify_token(credentials.credentials)
    except PermissionError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )


def get_optional_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer),
) -> UserContext | None:
    if credentials is None:
        return None
    try:
        return _adapter.verify_token(credentials.credentials)
    except PermissionError:
        return None
