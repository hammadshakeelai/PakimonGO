from dataclasses import dataclass
from typing import Protocol


@dataclass
class UserContext:
    user_id: str
    email: str | None = None
    auth_provider: str | None = None


class AuthAdapter(Protocol):
    def verify_token(self, token: str) -> UserContext:
        ...
