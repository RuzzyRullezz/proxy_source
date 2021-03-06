from sqlalchemy import UniqueConstraint

from proxy_source.db.base import Base

import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as sa_pg


class ProxyDb(Base):  # type: ignore
    __tablename__ = 'proxy'
    __table_args__ = (
        UniqueConstraint('ip', 'port', name='ip_port_unique'),
    )
    id = sa.Column(sa.BigInteger(), primary_key=True, index=True)
    created_at = sa.Column(sa.DateTime(timezone=True), index=True, nullable=False)
    protocol = sa.Column(sa.Unicode(), index=True, nullable=False)
    ip = sa.Column(sa_pg.INET(), index=False, nullable=False)
    port = sa.Column(sa.Integer(), index=False, nullable=False)
    user = sa.Column(sa.Unicode(), index=True, nullable=True)
    password = sa.Column(sa.Unicode(), index=True, nullable=True)
    source = sa.Column(sa.Unicode(), index=True, nullable=False)
    is_active = sa.Column(sa.Boolean(), index=True, nullable=False, server_default='False')
