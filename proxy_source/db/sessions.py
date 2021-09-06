from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from proxy_source import config

async_engine = create_async_engine(
    str(config.DB_DSN_ASYNC),
    echo=True,
    echo_pool=True,
    max_overflow=0,
    pool_size=1,
)


def get_async_db_session() -> AsyncSession:
    session_factory = sessionmaker(async_engine, class_=AsyncSession)
    session = session_factory()
    return session

