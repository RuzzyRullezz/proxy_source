from __future__ import annotations

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
        return cls(
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
