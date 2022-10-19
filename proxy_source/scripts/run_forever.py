import asyncio
import sys

from proxy_source import config
from proxy_source.utils.date_time import utc_now
from proxy_source.core import manager


async def run_once():
    start = utc_now()
    sys.stdout.write(f'Start time: {start}\n')
    new_proxies_cnt = await manager.fetch_and_save_proxies()
    sys.stdout.write(f'New proxies count: {new_proxies_cnt}.\n')
    active_proxies_cnt = await manager.filter_proxies()
    sys.stdout.write(f'Active proxies count: {active_proxies_cnt}.\n')
    end = utc_now()
    sys.stdout.write(f'End time: {end}.\n')
    elapsed_time_seconds = int((end - start).total_seconds())
    sys.stdout.write(f'Elapsed time: {elapsed_time_seconds} seconds.\n')


async def run_forever():
    while True:
        await run_once()


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        run_forever()
    )


if __name__ == '__main__':
    config.setup_logging()
    main()
