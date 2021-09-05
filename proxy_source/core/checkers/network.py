import datetime
from abc import abstractmethod, ABC
from typing import Optional, Callable, List, Awaitable

import httpx
from mypy_extensions import DefaultNamedArg
from pydantic import BaseModel
from starlette import status

from ..proxies import Proxy
from . import exceptions


IpAddressServiceClientFactoryType = Callable[[DefaultNamedArg(Optional[str], name='proxies')], httpx.Client]


class IpAddressService(ABC):
    client_factory: IpAddressServiceClientFactoryType

    def __init__(self, client_factory: Optional[IpAddressServiceClientFactoryType] = None):
        if client_factory is None:
            client_factory = httpx.AsyncClient
        self.client_factory = client_factory

    async def get_ip(self, proxy: Optional[Proxy] = None) -> str:
        timeout = datetime.timedelta(seconds=3)
        request = self.get_request(proxy=proxy)
        proxies: Optional[str] = None
        if proxy is not None:
            proxies = proxy.httpx_format
        async with self.client_factory(proxies=proxies) as client:
            response = await client.send(request, timeout=timeout.total_seconds())
        if response.status_code != status.HTTP_200_OK:
            raise exceptions.IpServiceNot200Exception(response.status_code)
        return self.parse_response(response)

    @abstractmethod
    def get_request(self, proxy: Optional[Proxy] = None) -> httpx.Request:
        raise NotImplementedError()

    @abstractmethod
    def parse_response(self, response: httpx.Response) -> str:
        raise NotImplementedError()


class IpifyService(IpAddressService):

    class IpifyResponse(BaseModel):
        ip: str

    def get_request(self, proxy: Optional[Proxy] = None) -> httpx.Request:
        url: str = 'https://api.ipify.org?format=json'
        if proxy is not None:
            if proxy.protocol == Proxy.ProtocolEnum.http:
                url = 'http://api.ipify.org?format=json'
            elif proxy.protocol == Proxy.ProtocolEnum.https:
                url = 'https://api.ipify.org?format=json'
            else:
                raise NotImplementedError(f"Unsupported proxy protocol: {proxy.protocol.value}")
        return httpx.Request('GET', url)

    def parse_response(self, response: httpx.Response) -> str:
        ipify_response = self.IpifyResponse.parse_raw(response.content)
        return ipify_response.ip


class IpConfigService(IpAddressService):
    def get_request(self, proxy: Optional[Proxy] = None) -> httpx.Request:
        url: str = 'https://ifconfig.io'
        if proxy is not None:
            if proxy.protocol == Proxy.ProtocolEnum.http:
                url = 'http://ifconfig.io'
            elif proxy.protocol == Proxy.ProtocolEnum.https:
                url = 'https://ifconfig.io'
            else:
                raise NotImplementedError(f"Unsupported proxy protocol: {proxy.protocol.value}")
        return httpx.Request('GET', url)

    def parse_response(self, response: httpx.Response) -> str:
        encoding = 'utf-8'
        return response.content.decode(encoding)


async def get_proxy_ip(proxy: Proxy) -> str:
    ip_services: List[IpAddressService] = [
        IpifyService(),
        IpConfigService(),
    ]
    last_exc: Optional[Exception] = None
    for service in ip_services:
        try:
            return await service.get_ip(proxy=proxy)
        except httpx.HTTPError as exc:
            last_exc = exc
    raise exceptions.IpServiceNetworkException() from last_exc


GetRealIpFuncType = Callable[[DefaultNamedArg(bool, name='use_cache')], Awaitable[str]]  # noqa: F821


# nonlocal-based cache
def get_real_ip_func() -> GetRealIpFuncType:
    ip_cached: Optional[str] = None

    async def _get_real_ip() -> str:
        return await IpifyService().get_ip(proxy=None)

    async def _get_real_ip_wrapper(use_cache: bool = True) -> str:
        nonlocal ip_cached
        if not use_cache:
            ip_cached = None
        if ip_cached is None:
            ip_cached = await _get_real_ip()
        return ip_cached

    return _get_real_ip_wrapper


get_real_ip: GetRealIpFuncType = get_real_ip_func()
