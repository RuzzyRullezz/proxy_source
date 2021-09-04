import datetime
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Dict, Literal


@dataclass
class Proxy:

    class ProtocolEnum(str, Enum):
        http = 'http'
        https = 'https'

    class SourceEnum(str, Enum):
        best_proxies = 'best_proxies'

    protocol: ProtocolEnum
    ip: str
    port: int
    user: Optional[str]
    password: Optional[str]
    source: SourceEnum
    created_at: datetime.datetime

    @property
    def requests_format(self) -> Dict[Literal['http', 'https'], str]:
        scheme: str = f'{self.protocol}'
        auth_prefix: str
        if self.user is not None and self.password is not None:
            auth_prefix = f'{self.user}:{self.password}@'
        else:
            auth_prefix = ''
        uri: str = f'{scheme}://{auth_prefix}{self.ip}:{self.port}'
        return {
            'http': uri,
            'https': uri,
        }
