from __future__ import annotations

import datetime
import decimal
import ipaddress
from typing import List, Dict

from pydantic import BaseModel

from proxy_source import config
from proxy_source.utils.date_time import utc_now

from proxy_source.core import proxies
from proxy_source.core.sources import data_repository
from proxy_source.core.sources import http_client


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


class DataRepository(data_repository.DataRepository):

    def __init__(self, api_key: str):
        scheme = 'https'
        netloc = 'api.best-proxies.ru'
        client = http_client.HttpClient(scheme, netloc)
        self.api_key = api_key
        super().__init__(
            client,
            Proxy,
            ProxiesList,
        )

    @property
    def source_type(self) -> proxies.ProxySourceIdType:
        return proxies.ProxySourceIdType('best_proxies')

    def retrieve_proxy_dto_list_from_container(self, proxy_container: ProxiesList) -> List[Proxy]:
        return proxy_container.__root__

    def get_endpoint(self) -> str:
        endpoint = 'proxylist.json'
        return endpoint

    def get_query_params(self) -> Dict:
        query_params = dict(
            key=self.api_key,
            type='http,https',
            response=1000,
            speed=1,
            level=1,
            limit=0,
        )
        return query_params

    def proxy_from_dto(self, proxy_dto: Proxy) -> proxies.Proxy:
        schema: proxies.Proxy.ProtocolEnum
        protocol_established_marker: int = 1
        if proxy_dto.http == protocol_established_marker:
            schema = proxies.Proxy.ProtocolEnum.http
        elif proxy_dto.https == protocol_established_marker:
            schema = proxies.Proxy.ProtocolEnum.https
        else:
            raise NotImplementedError("Unsupported proxy protocol.")
        return proxies.Proxy(
            protocol=schema,
            ip=ipaddress.ip_address(proxy_dto.ip),
            port=proxy_dto.port,
            user=None,
            password=None,
            source=self.source_type,
            created_at=utc_now(),
            is_active=False,
        )

    @classmethod
    def create(cls) -> DataRepository:
        assert config.BESTPROXIES_API_KEY is not None, 'set BESTPROXIES_API_KEY param in .env file'
        api_key = str(config.BESTPROXIES_API_KEY)
        proxies_repository = cls(api_key)
        return proxies_repository
