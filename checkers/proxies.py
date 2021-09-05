import asyncio

from proxy_source.utils.date_time import utc_now
from proxy_source.core.sources import service as sources_service


async def main():
    start = utc_now()
    proxies = await sources_service.get_proxies()
    end = utc_now()
    elapsed_time = end - start
    print(len(proxies))
    print(elapsed_time.total_seconds())


loop = asyncio.get_event_loop()
loop.run_until_complete(
    main()
)
