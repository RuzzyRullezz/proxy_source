from __future__ import annotations

from sqlalchemy import Column, BigInteger, DateTime, Unicode, JSON, LargeBinary, Integer, Interval


class IncomingRequestBase:
    id = Column(BigInteger(), primary_key=True, index=True)
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
