import ipaddress
from typing import Optional

from pydantic.main import BaseModel

from proxy_source.core import proxy_manager


class ProxyDTO(BaseModel):
    protocol: proxy_manager.proxies.Proxy.ProtocolEnum
    ip: ipaddress.IPv4Address
    port: int
    user: Optional[str]
    password: Optional[str]
