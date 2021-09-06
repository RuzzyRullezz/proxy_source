import asyncio
import datetime
from abc import abstractmethod, ABC
from typing import Optional, Callable, List, Awaitable

import aiohttp
import asyncio.exceptions
from httpcore import ConnectTimeout
from mypy_extensions import DefaultNamedArg
from pydantic import BaseModel, ValidationError
from starlette import status

from proxy_source import config

from .. import proxies
from . import exceptions


class IpAddressService(ABC):
    async def get_ip(self, proxy: Optional[proxies.Proxy] = None) -> str:
        timeout: datetime.timedelta = datetime.timedelta(seconds=10)
        url: str = self.get_url(proxy=proxy)
        aiohttp_proxy: Optional[str] = None
        if proxy is not None:
            aiohttp_proxy = proxy.aiohttp_format
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    url,
                    proxy=aiohttp_proxy,
                    allow_redirects=False,
                    timeout=timeout.total_seconds()
            ) as resp:
                status_code = resp.status
                response = await resp.read()
        if status_code != status.HTTP_200_OK:
            raise exceptions.IpServiceNot200Exception(status_code)
        return self.parse_response(response)

    @abstractmethod
    def get_url(self, proxy: Optional[proxies.Proxy] = None) -> str:
        raise NotImplementedError()

    @abstractmethod
    def parse_response(self, response: bytes) -> str:
        raise NotImplementedError()


class IpifyService(IpAddressService):

    class IpifyResponse(BaseModel):
        ip: str

    def get_url(self, proxy: Optional[proxies.Proxy] = None) -> str:
        url: str = 'https://api.ipify.org?format=json'
        if proxy is not None:
            if proxy.protocol == proxies.Proxy.ProtocolEnum.http:
                url = 'http://api.ipify.org?format=json'
            elif proxy.protocol == proxies.Proxy.ProtocolEnum.https:
                url = 'https://api.ipify.org?format=json'
            else:
                raise NotImplementedError(f"Unsupported proxy protocol: {proxy.protocol.value}")
        return url

    def parse_response(self, response: bytes) -> str:
        try:
            ipify_response = self.IpifyResponse.parse_raw(response)
        except ValidationError:
            raise exceptions.IpServiceParseResponseException(response)
        return ipify_response.ip


async def get_proxy_ip(proxy: proxies.Proxy) -> str:
    ip_services: List[IpAddressService] = [
        IpifyService(),
    ]
    last_exc: Optional[Exception] = None
    for service in ip_services:
        try:
            return await service.get_ip(proxy=proxy)
        except (aiohttp.ClientError, asyncio.exceptions.TimeoutError, ConnectTimeout, ConnectionResetError) as exc:
            last_exc = exc
    raise exceptions.IpServiceNetworkException() from last_exc


GetRealIpFuncType = Callable[[DefaultNamedArg(bool, name='use_cache')], Awaitable[str]]  # noqa: F821


# nonlocal-based cache
def get_real_ip_func() -> GetRealIpFuncType:
    ip_cached: Optional[str] = None
    lock = asyncio.Lock()

    async def _get_real_ip() -> str:
        return config.REAL_IP or await IpifyService().get_ip(proxy=None)

    async def _get_real_ip_wrapper(use_cache: bool = True) -> str:
        nonlocal ip_cached
        if not use_cache:
            ip_cached = None
        async with lock:
            if ip_cached is None:
                ip_cached = await _get_real_ip()
        return ip_cached

    return _get_real_ip_wrapper


get_real_ip: GetRealIpFuncType = get_real_ip_func()
