from typing import Optional, Any

from pydantic import BaseModel


class ApiError(BaseModel):
    code: str
    message: Optional[str] = None
    payload: Any = None
