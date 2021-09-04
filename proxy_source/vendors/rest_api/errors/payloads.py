from pydantic import BaseModel


class ValidationErrorPayload(BaseModel):
    field: str
    message: str
