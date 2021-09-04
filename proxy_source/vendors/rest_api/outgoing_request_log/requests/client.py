import datetime
import traceback
from typing import Callable

from requests import PreparedRequest, Response, Session

from ..context import LogContextOutgoing


OutgoingLogSaver = Callable[[LogContextOutgoing], None]


def utc_now():
    return datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)


class SessionLoggable(Session):
    encoding = 'utf-8'
    log_save: OutgoingLogSaver

    def __init__(self, log_save: OutgoingLogSaver):
        super().__init__()
        self.log_save = log_save

    @staticmethod
    def create_context(request: PreparedRequest) -> LogContextOutgoing:
        context = LogContextOutgoing(
            request_datetime=utc_now(),
            request_url=request.url,
            request_method=request.method,
            request_headers=dict(request.headers),
            request_body=request.body,
        )
        return context

    @staticmethod
    def update_context(context: LogContextOutgoing, response: Response):
        context.response_datetime = utc_now()
        context.response_status_code = response.status_code
        context.response_headers = dict(response.headers)
        context.response_body = response.content
        context.elapsed_time = context.response_datetime - context.request_datetime

    @staticmethod
    def set_exception_context(context: LogContextOutgoing, exception_log: str):
        context.exception = exception_log

    def send(self, request: PreparedRequest, **kwargs) -> Response:
        context = self.create_context(request)
        try:
            response = super().send(request, **kwargs)
            self.update_context(context, response)
            return response
        except Exception as exc:
            self.set_exception_context(context, traceback.format_exc())
            raise exc from exc
        finally:
            self.log_save(context)
