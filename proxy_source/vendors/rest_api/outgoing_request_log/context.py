from __future__ import annotations

import datetime
from dataclasses import dataclass
from typing import Dict, Optional, Protocol


@dataclass
class LogContextOutgoing:
    request_datetime: datetime.datetime
    request_url: str
    request_method: str
    request_headers: Dict[str, str]
    request_body: bytes

    response_datetime: Optional[datetime.datetime] = None
    response_status_code: Optional[int] = None
    response_headers: Optional[Dict[str, str]] = None
    response_body: Optional[bytes] = None

    elapsed_time: Optional[datetime.timedelta] = None
    exception: Optional[str] = None


class OutgoingLogSaverProtocol(Protocol):
    def __call__(self, log_context_outgoing: LogContextOutgoing):
        pass


class AsyncOutgoingLogSaverProtocol(Protocol):
    async def __call__(self, log_context_outgoing: LogContextOutgoing):
        pass
