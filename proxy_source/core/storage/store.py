import dataclasses
import datetime
import ipaddress
import typing

import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession

from proxy_source.db.sessions import create_transaction_session

from .. import proxies
from . import db_scheme


async def create_list(proxy_list: typing.List[proxies.Proxy]):
    async with create_transaction_session() as db_session:
        for proxy in proxy_list:
            await create(db_session, proxy)


async def create(db_session: AsyncSession, proxy: proxies.Proxy):
    proxy_db = proxy_to_db(proxy)
    db_session.add(proxy_db)
    await db_session.flush()


def proxy_to_db(proxy: proxies.Proxy) -> db_scheme.ProxyDb:
    proxy_db: db_scheme.ProxyDb = db_scheme.ProxyDb(
        created_at=proxy.created_at,
        protocol=proxy.protocol,
        ip=proxy.ip,
        port=proxy.port,
        user=proxy.user,
        password=proxy.password,
        source=proxy.source,
        is_active=proxy.is_active,
    )
    return proxy_db


async def update_list(proxy_list: typing.List[proxies.Proxy]):
    async with create_transaction_session() as db_session:
        for proxy in proxy_list:
            await update(db_session, proxy)


async def update(db_session: AsyncSession, proxy: proxies.Proxy):
    proxy_db = await get_proxy_db_or_none(db_session, proxy.ip, proxy.port)
    assert proxy_db is not None
    proxy_db.created_at = proxy.created_at
    proxy_db.protocol = proxy.protocol
    proxy_db.user = proxy.user
    proxy_db.password = proxy.password
    proxy_db.source = proxy.source
    proxy_db.is_active = proxy.is_active
    db_session.add(proxy_db)
    await db_session.flush()


async def get_proxy_db_or_none(
        db_session: AsyncSession,
        ip: ipaddress.IPv4Address,
        port: int
) -> typing.Optional[db_scheme.ProxyDb]:
    select_stmt = sqlalchemy.select(db_scheme.ProxyDb).where(
        db_scheme.ProxyDb.ip == ip,
        db_scheme.ProxyDb.port == port,
    )
    result = await db_session.execute(select_stmt)
    proxy_db: typing.Optional[db_scheme.ProxyDb] = result.scalar()
    return proxy_db


async def filter_proxy_list(proxy_list: typing.Iterable[proxies.Proxy]) -> typing.List[proxies.Proxy]:
    filtered_proxy_list: typing.List[proxies.Proxy] = []
    async with create_transaction_session() as db_session:
        for proxy in proxy_list:
            if await is_stored(db_session, proxy):
                continue
            filtered_proxy_list.append(proxy)
        return filtered_proxy_list


async def is_stored(db_session: AsyncSession, proxy: proxies.Proxy) -> bool:
    proxy_db = await get_proxy_db_or_none(db_session, proxy.ip, proxy.port)
    return proxy_db is not None


@dataclasses.dataclass
class GetListQuery:
    is_active: typing.Optional[bool] = None
    created_from: typing.Optional[datetime.datetime] = None
    created_to: typing.Optional[datetime.datetime] = None


async def get_list(get_list_query: GetListQuery) -> typing.List[proxies.Proxy]:
    async with create_transaction_session() as db_session:
        select_stmt = sqlalchemy.select(db_scheme.ProxyDb).filter()
        if get_list_query.is_active is not None:
            select_stmt = select_stmt.filter(db_scheme.ProxyDb.is_active == get_list_query.is_active)
        if get_list_query.created_from is not None:
            select_stmt = select_stmt.filter(get_list_query.created_from <= db_scheme.ProxyDb.created_at)
        if get_list_query.created_to is not None:
            select_stmt = select_stmt.filter(db_scheme.ProxyDb.created_at <= get_list_query.created_to)
        select_stmt = select_stmt.order_by(
            sqlalchemy.desc(db_scheme.ProxyDb.created_at)
        )
        result = await db_session.execute(select_stmt)
        proxy_db_list: typing.List[db_scheme.ProxyDb] = result.scalars().all()
        return list(map(proxy_from_db, proxy_db_list))


def proxy_from_db(proxy_db: db_scheme.ProxyDb) -> proxies.Proxy:
    proxy: proxies.Proxy = proxies.Proxy(
        created_at=proxy_db.created_at,
        protocol=proxy_db.protocol,
        ip=proxy_db.ip,
        port=proxy_db.port,
        user=proxy_db.user,
        password=proxy_db.password,
        source=proxies.ProxySourceIdType(proxy_db.source),
        is_active=proxy_db.is_active,
    )
    return proxy


async def mark_all_as_inactive():
    async with create_transaction_session() as db_session:
        update_stmt = sqlalchemy.update(db_scheme.ProxyDb).values(is_active=False)
        await db_session.execute(update_stmt)
