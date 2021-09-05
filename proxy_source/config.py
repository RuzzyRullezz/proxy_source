import functools
import pathlib
from typing import List, Callable

from sqlalchemy.engine.url import URL
from starlette.config import Config
from starlette.datastructures import Secret

from proxy_source.vendors import loggers


config_path: pathlib.Path = pathlib.Path(__file__).parent.absolute() / ".env"
config: Config = Config(str(config_path))

BASE_PATH: pathlib.Path = pathlib.Path(__file__).parent.absolute()

# Use in tests
ALEMBIC_MIGRATIONS_PATH: pathlib.Path = BASE_PATH / "db"

ALLOWED_ORIGINS: List[str] = [
    "*",
]

TESTING: bool = config("TESTING", cast=bool, default=False)

DB_HOST: str = config("DB_HOST", default='127.0.0.1')
DB_PORT: int = config("DB_PORT", cast=int, default=5432)
DB_USER: str = config("DB_USER", default='proxy_source')
DB_PASSWORD: Secret = config("DB_PASSWORD", cast=Secret, default='proxy_source')
DB_DATABASE: str = config("DB_DATABASE", default='proxy_source')
DB_DSN_ASYNC: URL = URL(
    drivername="postgresql+asyncpg",
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
    database=DB_DATABASE,
)
DB_DSN_SYNC: URL = URL(
    drivername="postgresql",
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
    database=DB_DATABASE,
)

# RabbitMQ
RMQ_HOST: str = config("RMQ_HOST", cast=str, default="127.0.0.1")
RMQ_PORT: int = config("RMQ_PORT", cast=int, default=5672)
RMQ_VHOST: str = config("RMQ_VHOST", cast=str, default="proxy_source")
RMQ_USER: str = config("RMQ_USER", cast=str, default="proxy_source")
RMQ_PASSWORD: Secret = config("RMQ_PASSWORD", cast=Secret, default="proxy_source")

# Redis
REDIS_HOST: str = config("REDIS_HOST", cast=str, default="127.0.0.1")
REDIS_PORT: int = config("REDIS_PORT", cast=int, default=6379)
REDIS_DB: int = config("REDIS_DB", cast=int, default=0)
REDIS_USERNAME: str = config("REDIS_USERNAME", cast=str, default=None)
REDIS_PASSWORD: Secret = config("REDIS_PASSWORD", cast=Secret, default=None)

# Logging Telegram
TG_TOKEN: str = config("TG_TOKEN", cast=str, default=None)
TG_CHAT: str = config("TG_CHAT", cast=int, default=None)
# Logging Sentry
SENTRY_DSN: str = config("SENTRY_DSN", cast=str, default=None)
# Loggers startup
setup_logging: Callable[[], None] = functools.partial(
    loggers.setup,
    tg_token=TG_TOKEN,
    tg_chat=TG_CHAT,
    sentry_dsn=SENTRY_DSN,
)

PROXY_CHECK_MAX_WORKERS: int = config("PROXY_CHECK_MAX_WORKERS", cast=int, default=50)

# Proxy Sources
# https://best-proxies.ru/
BESTPROXIES_API_KEY: Secret = config("BESTPROXIES_API_KEY", cast=Secret, default=None)
