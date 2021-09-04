from pydantic import BaseModel


class BooleanResponse(BaseModel):
    value: bool


class OkResponse(BaseModel):
    status: str = 'ok'


ok_response = OkResponse()
