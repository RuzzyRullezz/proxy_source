from __future__ import annotations

import datetime
from typing import Dict, Optional

from sqlalchemy import Column, BigInteger, DateTime, Unicode, JSON, LargeBinary, Integer, Interval

from .context import LogContextOutgoing


class OutgoingRequestBase:
    id = Column(BigInteger(), primary_key=True)
    # request
    request_datetime = Column(DateTime(timezone=True), index=True, nullable=False)
    request_url = Column(Unicode(), index=True, nullable=False)
    request_method = Column(Unicode(), index=True, nullable=False)
    request_headers = Column(JSON(none_as_null=True), nullable=True)
    request_body = Column(LargeBinary(), nullable=True)
    # response
    response_datetime = Column(DateTime(timezone=True), index=True, nullable=True)
    response_status_code = Column(Integer(), index=True, nullable=True)
    response_headers = Column(JSON(none_as_null=True), nullable=True)
    response_body = Column(LargeBinary(), nullable=True)
    # add
    elapsed_time = Column(Interval(), nullable=True)
    exception = Column(Unicode(), nullable=True)

    @classmethod
    def from_log_context(cls, log_context: LogContextOutgoing) -> OutgoingRequestBase:
        return cls.create(
            request_datetime=log_context.request_datetime,
            request_url=log_context.request_url,
            request_method=log_context.request_method,
            request_headers=log_context.request_headers,
            request_body=log_context.request_body,
            response_datetime=log_context.response_datetime,
            response_status_code=log_context.response_status_code,
            response_headers=log_context.response_headers,
            response_body=log_context.response_body,
            elapsed_time=log_context.elapsed_time,
            exception=log_context.exception,
        )

    @classmethod
    def create(
            cls,
            request_datetime: datetime.datetime,
            request_url: str,
            request_method: str,
            request_headers: Optional[Dict[str, str]],
            request_body: bytes,
            response_datetime: Optional[datetime.datetime],
            response_status_code: Optional[int],
            response_headers: Optional[Dict[str, str]],
            response_body: Optional[bytes],
            elapsed_time: Optional[datetime.timedelta],
            exception: Optional[str],
    ) -> OutgoingRequestBase:
        obj = cls()
        obj.request_datetime = request_datetime
        obj.request_url = request_url
        obj.request_method = request_method
        obj.request_headers = request_headers
        obj.request_body = request_body
        obj.response_datetime = response_datetime
        obj.response_status_code = response_status_code
        obj.response_headers = response_headers
        obj.request_body = response_body
        obj.elapsed_time = elapsed_time
        obj.exception = exception
        return obj
