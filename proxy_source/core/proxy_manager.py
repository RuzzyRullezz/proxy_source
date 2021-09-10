from typing import Set, List, Tuple

from . import proxies
from . import sources
from . import checkers


async def get_and_save_proxies() -> int:
    active_proxies_set: Set[proxies.Proxy] = set(await get_active_proxies())
    sources_proxies_set: Set[proxies.Proxy] = set(await sources.service.get_proxies())
    new_proxies_set = sources_proxies_set - active_proxies_set
    await proxies.save_proxies(*new_proxies_set)
    return len(new_proxies_set)


async def check_saved_proxies() -> Tuple[int, int]:
    active_proxies: List[proxies.Proxy] = await get_active_proxies()
    filtered_active_proxies_set: Set[proxies.Proxy] = set(
        await checkers.filter_alive_anon_proxies(active_proxies)
    )
    active_proxies_set = set(active_proxies)
    not_active_proxies = active_proxies_set - filtered_active_proxies_set
    await proxies.mark_proxies_as_deleted(*not_active_proxies)
    return len(active_proxies), len(not_active_proxies)


async def get_active_proxies() -> List[proxies.Proxy]:
    active_proxies_list: List[proxies.Proxy] = await proxies.get_active_proxies()
    return active_proxies_list
