import ipaddress
from typing import List, Optional

import sqlalchemy as sa

from proxy_source.db.sessions import create_transaction_session, Session
from proxy_source.utils.date_time import utc_now

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
        ip=proxy_db.ip,
        port=proxy_db.port,
        user=proxy_db.user,
        password=proxy_db.password,
        source=proxy_db.source,
    )
    return proxy


async def save_proxies(*proxies_list: models.Proxy):
    async with create_transaction_session() as db_session:
        for proxy in proxies_list:
            if await is_proxy_in_store(db_session, proxy):
                continue
            proxy_db = proxy_db_from_proxy(proxy)
            db_session.add(proxy_db)


async def get_active_proxies() -> List[models.Proxy]:
    select_stmt = sa.select(db_scheme.ProxyDb).where(
        db_scheme.ProxyDb.deleted_at.is_(None),
    )
    async with create_transaction_session() as db_session:
        proxies_db_list = (await db_session.execute(select_stmt)).scalars().all()
        return list(map(proxy_from_proxy_db, proxies_db_list))


async def is_proxy_in_store(db_session: Session, proxy: models.Proxy) -> bool:
    proxy_db: Optional[db_scheme.ProxyDb] = await get_proxy_db_or_none(db_session, proxy)
    return proxy_db is not None


async def get_proxy_db_or_none(db_session: Session, proxy: models.Proxy) -> Optional[db_scheme.ProxyDb]:
    select_stmt = sa.select(db_scheme.ProxyDb).where(
        db_scheme.ProxyDb.ip == ipaddress.ip_address(proxy.ip),
        db_scheme.ProxyDb.port == proxy.port,
    )
    result = await db_session.execute(select_stmt)
    proxy_db: Optional[db_scheme.ProxyDb] = result.scalar()
    return proxy_db


async def mark_proxy_as_deleted(db_session: Session, proxy: models.Proxy):
    proxy_db: Optional[db_scheme.ProxyDb] = await get_proxy_db_or_none(db_session, proxy)
    assert proxy_db is not None
    proxy_db.deleted_at = utc_now()


async def mark_proxies_as_deleted(*proxies_list: models.Proxy):
    async with create_transaction_session() as db_session:
        for proxy in proxies_list:
            await mark_proxy_as_deleted(db_session, proxy)
