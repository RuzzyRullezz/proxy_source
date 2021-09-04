from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from proxy_source import config


engine = create_engine(
    config.DB_DSN,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(autocommit=True, autoflush=False, expire_on_commit=True, bind=engine)
