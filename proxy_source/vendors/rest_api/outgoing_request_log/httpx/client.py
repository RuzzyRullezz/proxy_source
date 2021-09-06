import datetime
import traceback
from typing import cast

from httpx import Client, Response, Request, AsyncClient

from ..context import LogContextOutgoing, OutgoingLogSaverProtocol, AsyncOutgoingLogSaverProtocol


def utc_now():
    return datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)


class ContextMixin:
    encoding = 'utf-8'

    def create_context(self, request: Request) -> LogContextOutgoing:
        context = LogContextOutgoing(
            request_datetime=utc_now(),
            request_url=str(request.url),
            request_method=request.method,
            request_headers={name.decode(self.encoding): value.decode(self.encoding)
                             for name, value in request.headers.raw},
            request_body=request.content,
        )
        return context

    def update_context(self, context: LogContextOutgoing, response: Response):
        context.response_datetime = utc_now()
        context.response_status_code = response.status_code
        context.response_headers = {name.decode(self.encoding): value.decode(self.encoding)
                                    for name, value in response.headers.raw}
        context.response_body = response.content
        context.elapsed_time = cast(datetime.datetime, context.response_datetime) - context.request_datetime

    @staticmethod
    def set_exception_context(context: LogContextOutgoing, exception_log: str):
        context.exception = exception_log


class TraceClient(Client, ContextMixin):
    log_save: OutgoingLogSaverProtocol

    def __init__(self, log_save: OutgoingLogSaverProtocol, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.log_save = log_save

    def send(self, request: Request, *args, **kwarg) -> Response:
        context = self.create_context(request)
        try:
            response = super(TraceClient, self).send(request, *args, **kwarg)
            self.update_context(context, response)
            return response
        except Exception as exc:
            self.set_exception_context(context, traceback.format_exc())
            raise exc from exc
        finally:
            self.log_save(context)


class AsyncTraceClient(AsyncClient, ContextMixin):
    log_save: AsyncOutgoingLogSaverProtocol

    def __init__(self, log_save: AsyncOutgoingLogSaverProtocol, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.log_save = log_save

    async def send(self, request: Request, *args, **kwarg) -> Response:
        context = self.create_context(request)
        try:
            response = await super(AsyncTraceClient, self).send(request, *args, **kwarg)
            self.update_context(context, response)
            return response
        except Exception as exc:
            self.set_exception_context(context, traceback.format_exc())
            raise exc from exc
        finally:
            await self.log_save(context)
