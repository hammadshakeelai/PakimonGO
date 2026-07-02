
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from .adapter import AuthAdapter, UserContext
from .fake_adapter import FakeAuthAdapter

_bearer = HTTPBearer(auto_error=False)

_adapter: AuthAdapter = FakeAuthAdapter()


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
