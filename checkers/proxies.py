import asyncio

from proxy_source.utils.date_time import utc_now
from proxy_source.core import proxy_manager


async def main():
    start = utc_now()
    await proxy_manager.get_and_save_proxies()
    end = utc_now()
    elapsed_time = end - start
    print(elapsed_time.total_seconds())


loop = asyncio.get_event_loop()
loop.run_until_complete(
    main()
)
