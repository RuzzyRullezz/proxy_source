import asyncio
from proxy_source.core.sources import BestProxiesSource
from proxy_source.core.checkers import service as checkers_service


async def main():
    bestproxies_source = BestProxiesSource()
    proxies_list = bestproxies_source.get_proxies()
    for proxy in proxies_list:
        print(await checkers_service.check_proxy(proxy))


loop = asyncio.get_event_loop()
loop.run_until_complete(
    main()
)








