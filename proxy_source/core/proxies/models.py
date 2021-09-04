import datetime
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class ProxyProtocolEnum(str, Enum):
    http = 'http'
    https = 'https'


@dataclass
class Proxy:
    protocol: ProxyProtocolEnum
    ip: str
    port: int
    user: Optional[str]
    password: Optional[str]
    source: str
    created_at: datetime.datetime
