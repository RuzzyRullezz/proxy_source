from typing import List, AsyncGenerator

from proxy_source import config

from .. import proxies
from . import worker


async def filter_alive_anon_proxies(proxies_list: List[proxies.Proxy]) -> AsyncGenerator[proxies.Proxy, None]:
    parallels_cnt = config.PROXY_CHECK_MAX_WORKERS
    async for report in worker.get_proxy_reports_gen(proxies_list, parallels_cnt):
        if not report.is_alive or not report.is_anon:
            continue
        yield report.proxy
