import dataclasses
import datetime
import ipaddress
from enum import Enum
from typing import Optional, Dict, Literal


@dataclasses.dataclass
class Proxy:

    class ProtocolEnum(str, Enum):
        http = 'http'
        https = 'https'

    class SourceEnum(str, Enum):
        best_proxies = 'best_proxies'

    protocol: ProtocolEnum = dataclasses.field(hash=False, compare=False)
    ip: ipaddress.IPv4Address = dataclasses.field(hash=True, compare=True)
    port: int = dataclasses.field(hash=True, compare=True)
    user: Optional[str] = dataclasses.field(hash=False, compare=False)
    password: Optional[str] = dataclasses.field(hash=False, compare=False)
    source: SourceEnum = dataclasses.field(hash=False, compare=False)
    created_at: datetime.datetime = dataclasses.field(hash=False, compare=False)
    is_active: bool = dataclasses.field(hash=False, compare=False)

    def __str__(self) -> str:
        scheme: str = f'{self.protocol}'
        auth_prefix: str
        if self.user is not None and self.password is not None:
            auth_prefix = f'{self.user}:{self.password}@'
        else:
            auth_prefix = ''
        uri: str = f'{scheme}://{auth_prefix}{self.ip}:{self.port}'
        return uri

    @property
    def requests_format(self) -> Dict[Literal['http', 'https'], str]:
        uri: str = str(self)
        return {
            'http': uri,
            'https': uri,
        }

    @property
    def httpx_format(self) -> str:
        uri: str = str(self)
        return uri

    @property
    def aiohttp_format(self) -> str:
        uri: str = str(self)
        uri = uri.replace('https:', 'http:')
        return uri
