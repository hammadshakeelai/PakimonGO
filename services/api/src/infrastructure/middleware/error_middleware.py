from __future__ import annotations

import logging
import traceback

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("pakimongo.api")

ERROR_CODES: dict[int, str] = {
    400: "bad_request",
    401: "unauthorized",
    403: "forbidden",
    404: "not_found",
    409: "conflict",
    422: "validation_error",
    429: "too_many_requests",
    500: "internal_error",
}


def _error_code(status: int) -> str:
    return ERROR_CODES.get(status, "unknown_error")


def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": _error_code(exc.status_code),
                "message": exc.detail if isinstance(exc.detail, str) else str(exc.detail),
                "details": {},
            }
        },
    )


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """Catches unhandled non-HTTP exceptions and returns structured JSON errors."""

    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except ValueError as exc:
            return _build_error(status=400, message=str(exc))
        except KeyError as exc:
            return _build_error(status=400, message=f"Missing required field: {exc}")
        except PermissionError as exc:
            return _build_error(status=403, message=str(exc))
        except FileNotFoundError as exc:
            return _build_error(status=404, message=str(exc))
        except Exception as exc:
            logger.error(
                "Unhandled exception: %s\n%s",
                exc,
                traceback.format_exc(),
            )
            return _build_error(
                status=500,
                message="An unexpected error occurred. Please try again later.",
            )


def _build_error(status: int, message: str, details: dict | None = None) -> JSONResponse:
    return JSONResponse(
        status_code=status,
        content={
            "error": {
                "code": _error_code(status),
                "message": message,
                "details": details or {},
            }
        },
    )
