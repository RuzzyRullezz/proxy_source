import asyncio

from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.schedulers.base import BaseScheduler
from apscheduler.triggers.cron import CronTrigger
from pytz import utc

from proxy_source import config
from proxy_source.scripts import fetch_proxies, filter_proxies


def get_scheduler() -> BaseScheduler:
    jobstores = {
        'default': SQLAlchemyJobStore(url=str(config.DB_DSN_SYNC))
    }
    job_defaults = {
        'coalesce': False,
        'max_instances': 2
    }
    return AsyncIOScheduler(jobstores=jobstores, job_defaults=job_defaults, timezone=utc)


def add_jobs(scheduler: BaseScheduler):
    scheduler.add_job(
        fetch_proxies.fetch,
        trigger=CronTrigger.from_crontab("*/10 * * * *"),
        id=fetch_proxies.fetch.__name__,
        replace_existing=True,
    )
    scheduler.add_job(
        filter_proxies.filter_proxies,
        trigger=CronTrigger.from_crontab("*/5 * * * *"),
        id=filter_proxies.filter_proxies.__name__,
        replace_existing=True,
    )


def run():
    scheduler = get_scheduler()
    add_jobs(scheduler)
    try:
        scheduler.start()
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        scheduler.shutdown()


if __name__ == "__main__":
    config.setup_logging()
    run()
