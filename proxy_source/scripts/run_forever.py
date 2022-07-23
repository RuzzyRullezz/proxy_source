import asyncio

from proxy_source.utils.date_time import utc_now
from proxy_source.core import manager


async def run_once():
    start = utc_now()
    print(f'Start time: {start}')
    new_proxies_cnt = await manager.fetch_and_save_proxies()
    active_proxies_cnt = await manager.filter_proxies()
    end = utc_now()
    elapsed_time_seconds = int((end - start).total_seconds())
    print(
        f'End time: {end}'
        f'\nElapsed time: {elapsed_time_seconds} seconds'
        f'\nNew proxies count: {new_proxies_cnt}.'
        f'\nActive proxies count: {active_proxies_cnt}.'
    )


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
