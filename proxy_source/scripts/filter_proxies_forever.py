import asyncio

from proxy_source.utils.date_time import utc_now
from proxy_source.core import manager


async def filter_proxies_once():
    start = utc_now()
    active_proxies_cnt = await manager.filter_proxies()
    end = utc_now()
    elapsed_time_seconds = int((end - start).total_seconds())
    print(
        f'Start time: {start}'
        f'\nEnd time: {end}'
        f'\nElapsed time: {elapsed_time_seconds} seconds'
        f'\nActive proxies count: {active_proxies_cnt}.'
    )


async def filter_proxies_forever():
    while True:
        await filter_proxies_once()


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        filter_proxies_forever()
    )


if __name__ == '__main__':
    main()
