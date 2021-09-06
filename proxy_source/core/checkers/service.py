from dataclasses import dataclass
from typing import Optional

from proxy_source.utils.date_time import utc_now

from ..proxies import Proxy
from . import network
from . import exceptions


@dataclass
class Report:
    proxy: Proxy
    is_alive: bool
    is_anon: Optional[bool]
    elapsed_time_seconds: Optional[float]
    exception: Optional[BaseException]


async def check_proxy(proxy: Proxy) -> Report:
    real_ip = await network.get_real_ip(use_cache=True)
    start = utc_now()
    is_alive: bool = False
    is_anon: Optional[bool] = None
    exception: Optional[BaseException] = None
    elapsed_time_seconds: Optional[float]
    try:
        proxy_ip = await network.get_proxy_ip(proxy)
        elapsed_time_seconds = (utc_now() - start).total_seconds()
        is_alive = True
        is_anon = proxy_ip != real_ip
    except exceptions.IpServiceException as exc:
        elapsed_time_seconds = (utc_now() - start).total_seconds()
        exception = exc.__cause__
    return Report(
        proxy=proxy,
        is_alive=is_alive,
        is_anon=is_anon,
        elapsed_time_seconds=elapsed_time_seconds,
        exception=exception,
    )
