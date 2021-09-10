import ipaddress
from typing import List

from fastapi import APIRouter

from proxy_source.core import proxy_manager

from . import dto

router = APIRouter(tags=["proxies"])


def proxy_to_dto(proxy: proxy_manager.proxies.Proxy) -> dto.ProxyDTO:
    return dto.ProxyDTO(
        protocol=proxy.protocol,
        ip=ipaddress.ip_address(proxy.ip),
        port=proxy.port,
        user=proxy.user,
        password=proxy.password,
    )


@router.get(
    "/",
    response_model=List[dto.ProxyDTO],
    operation_id='get_proxies',
    name='get_proxies',
)
async def get_proxies() -> List[dto.ProxyDTO]:
    active_proxies: List[proxy_manager.proxies.Proxy] = await proxy_manager.get_active_proxies()
    return list(map(proxy_to_dto, active_proxies))
