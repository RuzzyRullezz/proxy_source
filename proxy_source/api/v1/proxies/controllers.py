from typing import List

from fastapi import APIRouter

from proxy_source.core import manager

from . import dto

router = APIRouter(tags=["proxies"])


def proxy_to_dto(proxy: manager.proxies.Proxy) -> dto.ProxyDTO:
    return dto.ProxyDTO(
        protocol=proxy.protocol,
        ip=proxy.ip,
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
    active_proxies: List[manager.proxies.Proxy] = await manager.get_active_proxy_list()
    return list(map(proxy_to_dto, active_proxies))
