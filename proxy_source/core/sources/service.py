from typing import List, Set, Iterable, Type, Tuple

from .. import proxies, checkers
from . import data_repository


def get_data_repository_list() -> Iterable[data_repository.DataRepository]:
    from . import bestproxies
    repository_class_list: Tuple[Type[data_repository.DataRepository], ...] = (
        bestproxies.DataRepository,
    )
    return map(lambda repository_cls: repository_cls.create(), repository_class_list)


async def get_proxies() -> Set[proxies.Proxy]:
    proxy_list: List[proxies.Proxy] = []
    data_repository_list: Iterable[data_repository.DataRepository] = get_data_repository_list()
    for source in data_repository_list:
        proxy_list.extend(await source.get_proxy_list())
    alive_anon_proxy_list = await checkers.filter_alive_anon_proxies(proxy_list)
    return set(alive_anon_proxy_list)
