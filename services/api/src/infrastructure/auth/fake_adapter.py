
from .adapter import AuthAdapter, UserContext


class FakeAuthAdapter(AuthAdapter):
    def __init__(self, test_user_id: str | None = None):
        self._test_user_id = test_user_id

    def verify_token(self, token: str) -> UserContext:
        if token == "test_token_valid":
            uid = self._test_user_id or "test_user_default"
            return UserContext(user_id=uid, email="test@pakimongo.example", auth_provider="fake")
        if token.startswith("test_user_"):
            uid = token[len("test_user_"):]
            return UserContext(user_id=uid, email=f"{uid}@pakimongo.example", auth_provider="fake")
        raise PermissionError("Invalid token")
