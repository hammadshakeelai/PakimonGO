"""Version negotiation middleware for API versioning."""

from __future__ import annotations

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

SUPPORTED_VERSIONS = frozenset({"v1", "v2"})
DEFAULT_VERSION = "v1"


class VersionNegotiationMiddleware(BaseHTTPMiddleware):
    """Parse Accept-Version header and add to request state."""

    async def dispatch(self, request: Request, call_next):
        version = request.headers.get("Accept-Version", DEFAULT_VERSION)
        if version not in SUPPORTED_VERSIONS:
            version = DEFAULT_VERSION
        request.state.api_version = version
        response = await call_next(request)
        response.headers["API-Version"] = version
        return response
