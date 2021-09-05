from __future__ import annotations

import datetime
from dataclasses import dataclass
from typing import Dict, Optional, Callable, Awaitable


@dataclass
class LogContextOutgoing:
    request_datetime: datetime
    request_url: str
    request_method: str
    request_headers: Dict[str, str]
    request_body: bytes

    response_datetime: Optional[datetime] = None
    response_status_code: Optional[int] = None
    response_headers: Optional[Dict[str, str]] = None
    response_body: Optional[bytes] = None

    elapsed_time: Optional[datetime.timedelta] = None
    exception: Optional[str] = None


OutgoingLogSaver = Callable[[LogContextOutgoing], None]
AsyncOutgoingLogSaver = Callable[[LogContextOutgoing], Awaitable[None]]
