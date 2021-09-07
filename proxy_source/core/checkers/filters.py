from typing import List

from proxy_source import config

from .. import proxies
from . import worker


async def filter_alive_anon_proxies(proxies_list: List[proxies.Proxy]) -> List[proxies.Proxy]:
    parallels_cnt = config.PROXY_CHECK_MAX_WORKERS
    filtered_proxies: List[proxies.Proxy] = []
    async for report in worker.get_proxy_reports_gen(proxies_list, parallels_cnt):
        if not report.is_alive or not report.is_anon:
            continue
        filtered_proxies.append(report.proxy)
    return filtered_proxies
