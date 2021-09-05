from typing import List

from .. import proxies
from . import base
from . import bestproxies_source


async def get_proxies() -> List[proxies.Proxy]:
    proxy_sources: List[base.ProxySource] = [
        bestproxies_source.BestProxiesSource(),
    ]
    proxies_list: List[proxies.Proxy] = []
    for source in proxy_sources:
        proxies_list.extend(await source.get_proxies())
    return proxies_list
