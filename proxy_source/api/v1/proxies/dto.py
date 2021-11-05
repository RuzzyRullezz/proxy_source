import datetime
import ipaddress
from typing import Optional

from pydantic.main import BaseModel

from proxy_source.core import manager


class ProxyDTO(BaseModel):
    protocol: manager.proxies.Proxy.ProtocolEnum
    ip: ipaddress.IPv4Address
    port: int
    user: Optional[str]
    password: Optional[str]
    created_at: datetime.datetime
