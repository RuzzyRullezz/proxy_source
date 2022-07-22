import datetime
import typing

from ..utils.date_time import utc_now
from . import proxies
from . import sources
from . import checkers
from . import storage


proxy_interval: datetime.timedelta = datetime.timedelta(days=3)


async def fetch_and_save_proxies() -> int:
    proxy_set: typing.Set[proxies.Proxy] = await sources.service.get_proxies()
    proxy_list_not_in_db = await storage.filter_proxy_list(proxy_set)
    await storage.create_list(proxy_list_not_in_db)
    return len(proxy_list_not_in_db)


async def filter_proxies(interval: datetime.timedelta = proxy_interval) -> int:
    end = utc_now()
    begin = end - interval
    get_proxy_list_query = storage.GetListQuery(
        created_from=begin,
        created_to=end,
    )
    proxy_list: typing.List[proxies.Proxy] = await storage.get_list(get_proxy_list_query)
    active_proxy_list = await checkers.filter_alive_anon_proxies(proxy_list)
    for proxy in active_proxy_list:
        proxy.is_active = True
    await storage.mark_all_as_inactive()
    await storage.update_list(active_proxy_list)
    return len(active_proxy_list)


async def get_active_proxy_list() -> typing.List[proxies.Proxy]:
    get_proxy_list_query = storage.GetListQuery(
        is_active=True,
    )
    proxy_list = await storage.get_list(get_proxy_list_query)
    proxy_list = sorted(proxy_list, key=lambda proxy: proxy.created_at, reverse=True)
    return proxy_list
