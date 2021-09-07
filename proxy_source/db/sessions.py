import asyncio
import contextlib
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from proxy_source import config

async_engine = create_async_engine(
    str(config.DB_DSN_ASYNC),
    poolclass=NullPool,
    echo=False,
    echo_pool=False,
)


Session = sessionmaker(async_engine, class_=AsyncSession)
lock = asyncio.Lock()


@contextlib.asynccontextmanager
async def create_transaction_session() -> AsyncGenerator[AsyncSession, None]:
    async with lock, Session() as session, session.begin():
        yield session
