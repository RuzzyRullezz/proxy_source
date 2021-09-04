import datetime

import pendulum


def utc_now() -> datetime.datetime:
    return pendulum.now(pendulum.UTC)
