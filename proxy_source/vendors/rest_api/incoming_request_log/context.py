from __future__ import annotations

import copy
import datetime
from typing import Dict, Optional, cast

from fastapi import Request, Response
from starlette import status


class LogContextIncoming:
    request_datetime: datetime.datetime
    request_url: str
    request_method: str
    request_headers: Dict[str, str]
    request_body: bytes

    response_datetime: datetime.datetime
    response_status_code: int
    response_headers: Optional[Dict[str, str]]
    response_body: Optional[bytes]

    elapsed_time: datetime.timedelta
    exception: Optional[str]

    @staticmethod
    async def retrieve_response_body(response: Response) -> bytes:
        class async_iterator_wrapper:
            def __init__(self, obj):
                self._it = iter(obj)

            def __aiter__(self):
                return self

            async def __anext__(self):
                try:
                    value = next(self._it)
                except StopIteration:
                    raise StopAsyncIteration
                return value

        resp_body = [section async for section in response.__dict__['body_iterator']]
        response.__setattr__('body_iterator', async_iterator_wrapper(resp_body))
        return cast(bytes, resp_body[0])

    @staticmethod
    async def create(
            request_datetime: datetime.datetime,
            request: Request,
            response_datetime: datetime.datetime,
            response: Optional[Response] = None,
            exception_traceback: Optional[str] = None,
    ) -> LogContextIncoming:
        log_context = LogContextIncoming()
        log_context.request_datetime = request_datetime
        log_context.request_url = str(request.url)
        log_context.request_method = request.method
        log_context.request_headers = {}
        for k, v in request.headers.items():
            log_context.request_headers[k] = v
        log_context.request_body = await getattr(request, 'stream_full')() if hasattr(request, 'stream_full') else None
        log_context.response_datetime = response_datetime
        log_context.elapsed_time = response_datetime - request_datetime
        if response is not None:
            log_context.exception = None
            log_context.response_status_code = response.status_code
            log_context.response_body = await log_context.retrieve_response_body(response)
            log_context.response_headers = {}
            for k, v in response.headers.items():
                log_context.response_headers[k] = v
        elif exception_traceback is not None:
            log_context.exception = exception_traceback
            log_context.response_status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            log_context.response_body = None
            log_context.response_headers = None
        return log_context

    def as_dict(self) -> Dict:
        return copy.copy(self.__dict__)
