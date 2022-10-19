from typing import List

from .. import proxies
from . import worker


async def filter_alive_anon_proxies(
        proxies_list: List[proxies.Proxy],
        parallels_cnt: int = 10,
) -> List[proxies.Proxy]:
    filtered_proxies: List[proxies.Proxy] = []
    async for report in worker.get_proxy_reports_gen(proxies_list, parallels_cnt):
        if not report.is_alive or not report.is_anon:
            continue
        filtered_proxies.append(report.proxy)
    return filtered_proxies
