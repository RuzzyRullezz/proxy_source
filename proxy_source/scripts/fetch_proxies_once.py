import asyncio
import logging

from proxy_source import config
from proxy_source.utils.date_time import utc_now
from proxy_source.core import manager


async def fetch():
    logger = logging.getLogger()
    start = utc_now()
    new_proxies_cnt = await manager.fetch_and_save_proxies()
    end = utc_now()
    elapsed_time_seconds = int((end - start).total_seconds())
    logger.info(f'Start time: {start}'
                f'\nEnd time: {end}'
                f'\nElapsed time: {elapsed_time_seconds} seconds'
                f'\nNew proxies count: {new_proxies_cnt}.')


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        fetch()
    )


if __name__ == '__main__':
    config.setup_logging()
    main()
