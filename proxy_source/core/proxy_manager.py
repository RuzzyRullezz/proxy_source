from typing import Set, List, Tuple

from . import proxies
from . import sources
from . import checkers


async def get_and_save_proxies() -> int:
    active_proxies: Set[proxies.Proxy] = set(await proxies.get_active_proxies())
    sources_proxies: Set[proxies.Proxy] = set(await sources.service.get_proxies())
    new_proxies = sources_proxies - active_proxies
    await proxies.save_proxies(*new_proxies)
    return len(new_proxies)


async def check_saved_proxies() -> Tuple[int, int]:
    active_proxies_list: List[proxies.Proxy] = await proxies.get_active_proxies()
    filtered_active_proxies: Set[proxies.Proxy] = set(
        await checkers.filter_alive_anon_proxies(list(active_proxies_list))
    )
    active_proxies = set(active_proxies_list)
    not_active_proxies = active_proxies - filtered_active_proxies
    await proxies.mark_proxies_as_deleted(*not_active_proxies)
    return len(active_proxies_list), len(not_active_proxies)
