from typing import List

import sqlalchemy as sa

from proxy_source.db.sessions import create_transaction_session

from . import models
from . import db_scheme


def proxy_db_from_proxy(proxy: models.Proxy) -> db_scheme.ProxyDb:
    proxy_db: db_scheme.ProxyDb = db_scheme.ProxyDb(
        created_at=proxy.created_at,
        protocol=proxy.protocol,
        ip=proxy.ip,
        port=proxy.port,
        user=proxy.user,
        password=proxy.password,
        source=proxy.source,
        deleted_at=None,
    )
    return proxy_db


def proxy_from_proxy_db(proxy_db: db_scheme.ProxyDb) -> models.Proxy:
    proxy: models.Proxy = models.Proxy(
        created_at=proxy_db.created_at,
        protocol=proxy_db.protocol,
        ip=str(proxy_db.ip),
        port=proxy_db.port,
        user=proxy_db.user,
        password=proxy_db.password,
        source=proxy_db.source,
    )
    return proxy


async def save_proxies(*proxies_list: models.Proxy):
    proxies_db_list: List[db_scheme.ProxyDb] = list(map(proxy_db_from_proxy, proxies_list))
    async with create_transaction_session() as db_session:
        db_session.add_all(proxies_db_list)


async def get_active_proxies() -> List[models.Proxy]:
    select_stmt = sa.select(db_scheme.ProxyDb).where(
        db_scheme.ProxyDb.deleted_at.is_(None),
    )
    async with create_transaction_session() as db_session:
        proxies_db_list = (await db_session.execute(select_stmt)).scalars().all()
        return list(map(proxy_from_proxy_db, proxies_db_list))
