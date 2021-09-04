import datetime
from abc import abstractmethod, ABC
from typing import Optional, Callable, List, Dict, Literal

import requests
from mypy_extensions import DefaultNamedArg
from pydantic import BaseModel
from requests import Session, RequestException
from starlette import status

from ..proxies import Proxy
from . import exceptions


class IpAddressService(ABC):
    session: Session

    def __init__(self, session: Optional[Session] = None):
        if session is None:
            session = requests.Session()
        self.session = session

    def get_ip(self, proxy: Optional[Proxy] = None) -> str:
        timeout = datetime.timedelta(seconds=5)
        request = self.get_request(proxy=proxy)
        proxies: Optional[Dict[Literal['http', 'https'], str]] = None
        if proxy is not None:
            proxies = proxy.requests_format
        response = self.session.send(request.prepare(), timeout=timeout.total_seconds(), proxies=proxies)
        if response.status_code != status.HTTP_200_OK:
            raise exceptions.IpServiceNot200Exception(response.status_code)
        return self.parse_response(response)

    @abstractmethod
    def get_request(self, proxy: Optional[Proxy] = None) -> requests.Request:
        raise NotImplementedError()

    @abstractmethod
    def parse_response(self, response: requests.Response) -> str:
        raise NotImplementedError()


class IpifyService(IpAddressService):

    class IpifyResponse(BaseModel):
        ip: str

    def get_request(self, proxy: Optional[Proxy] = None) -> requests.Request:
        url: str = 'https://api.ipify.org?format=json'
        if proxy is not None:
            if proxy.protocol == Proxy.ProtocolEnum.http:
                url = 'http://api.ipify.org?format=json'
            elif proxy.protocol == Proxy.ProtocolEnum.https:
                url = 'https://api.ipify.org?format=json'
            else:
                raise NotImplementedError(f"Unsupported proxy protocol: {proxy.protocol.value}")
        return requests.Request('GET', url)

    def parse_response(self, response: requests.Response) -> str:
        ipify_response = self.IpifyResponse.parse_raw(response.content)
        return ipify_response.ip


class IpConfigService(IpAddressService):
    def get_request(self, proxy: Optional[Proxy] = None) -> requests.Request:
        url: str = 'https://ifconfig.io'
        if proxy is not None:
            if proxy.protocol == Proxy.ProtocolEnum.http:
                url = 'http://ifconfig.io'
            elif proxy.protocol == Proxy.ProtocolEnum.https:
                url = 'https://ifconfig.io'
            else:
                raise NotImplementedError(f"Unsupported proxy protocol: {proxy.protocol.value}")
        return requests.Request('GET', url)

    def parse_response(self, response: requests.Response) -> str:
        encoding = 'utf-8'
        return response.content.decode(encoding)


def get_proxy_ip(proxy: Proxy) -> str:
    session = requests.Session()
    ip_services: List[IpAddressService] = [
        IpifyService(session),
        IpConfigService(session),
    ]
    last_exc: Optional[Exception] = None
    for service in ip_services:
        try:
            return service.get_ip(proxy=proxy)
        except RequestException as exc:
            last_exc = exc
    raise exceptions.IpServiceNetworkException() from last_exc


GetRealIpFuncType = Callable[[DefaultNamedArg(bool, name='use_cache')], str]  # noqa: F821


# nonlocal-based cache
def get_real_ip_func() -> GetRealIpFuncType:
    ip_cached: Optional[str] = None

    def _get_real_ip() -> str:
        return IpifyService().get_ip(proxy=None)

    def _get_real_ip_wrapper(use_cache: bool = True) -> str:
        nonlocal ip_cached
        if not use_cache:
            ip_cached = None
        if ip_cached is None:
            ip_cached = _get_real_ip()
        return ip_cached

    return _get_real_ip_wrapper


get_real_ip: GetRealIpFuncType = get_real_ip_func()
