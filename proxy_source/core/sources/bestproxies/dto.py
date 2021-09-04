import datetime
import decimal
from typing import List

from pydantic import BaseModel


class Proxy(BaseModel):
    ip: str
    port: int
    hostname: str
    http: int
    https: int
    socks4: int
    socks5: int
    level: int
    google: int
    mailru: int
    twitter: int
    country_code: str
    response: int
    good_count: int
    bad_count: int
    last_check: datetime.datetime
    city: str
    region: str
    real_ip: str
    test_time: decimal.Decimal
    me: int


class ProxiesList(BaseModel):
    __root__: List[Proxy]
