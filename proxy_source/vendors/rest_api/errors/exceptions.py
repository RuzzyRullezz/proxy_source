from typing import Optional, Any

from .base import ApiError


class ApiException(Exception):
    status_code: int
    api_error: ApiError

    def __init__(self, status_code: int, code: str, message: Optional[str] = None, payload: Any = None) -> object:
        self.status_code = status_code
        self.api_error = ApiError(
            code=code,
            message=message,
            payload=payload,
        )
