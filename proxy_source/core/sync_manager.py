from typing import Set

from . import proxies
from . import sources


async def get_and_save_proxies() -> int:
    active_proxies: Set[proxies.Proxy] = set(await proxies.get_active_proxies())
    sources_proxies: Set[proxies.Proxy] = set(await sources.service.get_proxies())
    new_proxies = sources_proxies - active_proxies
    await proxies.save_proxies(*new_proxies)
    return len(new_proxies)
