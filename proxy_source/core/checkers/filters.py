from typing import List, Generator

from ..proxies import Proxy
from . import worker


async def filter_alive_anon_proxies(proxies_list: List[Proxy]) -> Generator[Proxy, None, None]:
    async for report in worker.get_proxy_reports_gen(proxies_list):
        if not report.is_alive or not report.is_anon:
            continue
        yield report.proxy
