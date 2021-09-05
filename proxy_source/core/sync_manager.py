from typing import List

from . import proxies
from . import sources


async def get_and_save_proxies() -> int:
    active_proxies = await proxies.get_active_proxies()
    source_proxies: List[proxies.Proxy] = await sources.service.get_proxies()
    new_proxies = set(source_proxies) - set(active_proxies)
    await proxies.save_proxies(*new_proxies)
    return len(new_proxies)
