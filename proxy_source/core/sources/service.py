from typing import List, Set

from .. import proxies, checkers
from . import data_repository


def get_data_repository_list() -> List[data_repository.DataRepository]:
    from . import bestproxies
    from . import hidemyname
    return [
        bestproxies.DataRepository.create(),
        hidemyname.DataRepository.create(),
    ]


async def get_proxies() -> Set[proxies.Proxy]:
    proxy_list: List[proxies.Proxy] = []
    data_repository_list: List[data_repository.DataRepository] = get_data_repository_list()
    for source in data_repository_list:
        proxy_list.extend(await source.get_proxy_list())
    alive_anon_proxy_list = await checkers.filter_alive_anon_proxies(proxy_list)
    return set(alive_anon_proxy_list)
