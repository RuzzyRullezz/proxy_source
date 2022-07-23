import asyncio

from proxy_source.utils.date_time import utc_now
from proxy_source.core import manager


async def run_once():
    start = utc_now()
    print(f'Start time: {start}')
    new_proxies_cnt = await manager.fetch_and_save_proxies()
    print(f'New proxies count: {new_proxies_cnt}.')
    active_proxies_cnt = await manager.filter_proxies()
    print(f'Active proxies count: {active_proxies_cnt}.')
    end = utc_now()
    print(f'End time: {end}.')
    elapsed_time_seconds = int((end - start).total_seconds())
    print(f'Elapsed time: {elapsed_time_seconds} seconds.')


async def run_forever():
    while True:
        await run_once()


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        run_forever()
    )


if __name__ == '__main__':
    main()
