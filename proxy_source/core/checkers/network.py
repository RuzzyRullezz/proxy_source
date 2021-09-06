import asyncio
import datetime
from abc import abstractmethod, ABC
from typing import Optional, Callable, List, Awaitable, Protocol

import httpx
from httpcore import ConnectTimeout
from mypy_extensions import DefaultNamedArg
from pydantic import BaseModel, ValidationError
from starlette import status

from proxy_source import config

from .. import proxies
from . import exceptions


class IpAddressServiceClientFactoryProtocol(Protocol):
    def __call__(self, proxies: Optional[str] = None) -> httpx.AsyncClient:
        pass


class IpAddressService(ABC):
    client_factory: IpAddressServiceClientFactoryProtocol

    def __init__(self, client_factory: Optional[IpAddressServiceClientFactoryProtocol] = None):
        if client_factory is None:
            client_factory = httpx.AsyncClient.__call__
        self.client_factory = client_factory

    async def get_ip(self, proxy: Optional[proxies.Proxy] = None) -> str:
        timeout: datetime.timedelta = datetime.timedelta(seconds=3)
        request: httpx.Request = self.get_request(proxy=proxy)
        httpx_proxies: Optional[str] = None
        if proxy is not None:
            httpx_proxies = proxy.httpx_format
        async with self.client_factory(proxies=httpx_proxies) as client:
            response = await client.send(request, timeout=timeout.total_seconds(), allow_redirects=False)
        if response.status_code != status.HTTP_200_OK:
            raise exceptions.IpServiceNot200Exception(response.status_code)
        return self.parse_response(response)

    @abstractmethod
    def get_request(self, proxy: Optional[proxies.Proxy] = None) -> httpx.Request:
        raise NotImplementedError()

    @abstractmethod
    def parse_response(self, response: httpx.Response) -> str:
        raise NotImplementedError()


class IpifyService(IpAddressService):

    class IpifyResponse(BaseModel):
        ip: str

    def get_request(self, proxy: Optional[proxies.Proxy] = None) -> httpx.Request:
        url: str = 'https://api.ipify.org?format=json'
        if proxy is not None:
            if proxy.protocol == proxies.Proxy.ProtocolEnum.http:
                url = 'http://api.ipify.org?format=json'
            elif proxy.protocol == proxies.Proxy.ProtocolEnum.https:
                url = 'https://api.ipify.org?format=json'
            else:
                raise NotImplementedError(f"Unsupported proxy protocol: {proxy.protocol.value}")
        return httpx.Request('GET', url)

    def parse_response(self, response: httpx.Response) -> str:
        try:
            ipify_response = self.IpifyResponse.parse_raw(response.content)
        except ValidationError:
            raise exceptions.IpServiceParseResponseException(response.content)
        return ipify_response.ip


class IpConfigService(IpAddressService):
    def get_request(self, proxy: Optional[proxies.Proxy] = None) -> httpx.Request:
        url: str = 'https://ifconfig.io'
        if proxy is not None:
            if proxy.protocol == proxies.Proxy.ProtocolEnum.http:
                url = 'http://ifconfig.io'
            elif proxy.protocol == proxies.Proxy.ProtocolEnum.https:
                url = 'https://ifconfig.io'
            else:
                raise NotImplementedError(f"Unsupported proxy protocol: {proxy.protocol.value}")
        return httpx.Request('GET', url)

    def parse_response(self, response: httpx.Response) -> str:
        encoding = 'utf-8'
        return response.content.decode(encoding)


async def get_proxy_ip(proxy: proxies.Proxy) -> str:
    ip_services: List[IpAddressService] = [
        IpifyService(),
        IpConfigService(),
    ]
    last_exc: Optional[Exception] = None
    for service in ip_services:
        try:
            return await service.get_ip(proxy=proxy)
        except (httpx.HTTPError, ConnectTimeout, ConnectionResetError) as exc:
            last_exc = exc
    raise exceptions.IpServiceNetworkException() from last_exc


GetRealIpFuncType = Callable[[DefaultNamedArg(bool, name='use_cache')], Awaitable[str]]  # noqa: F821


# nonlocal-based cache
def get_real_ip_func() -> GetRealIpFuncType:
    ip_cached: Optional[str] = None
    lock = asyncio.Lock()

    async def _get_real_ip() -> str:
        return await IpifyService().get_ip(proxy=None)

    async def _get_real_ip_wrapper(use_cache: bool = True) -> str:
        nonlocal ip_cached
        if not use_cache:
            ip_cached = None
        async with lock:
            if ip_cached is None:
                ip_cached = await _get_real_ip()
        return ip_cached

    return _get_real_ip_wrapper


if config.REAL_IP is None:
    get_real_ip: GetRealIpFuncType = get_real_ip_func()
else:
    def get_real_ip(use_cache: bool = True) -> str:
        return config.REAL_IP
