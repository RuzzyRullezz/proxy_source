from __future__ import annotations

import ipaddress
from typing import List, Dict, Optional

from pydantic import BaseModel

from proxy_source.utils.date_time import utc_now

from .. import proxies
from . import data_repository, http_client


class Proxy(BaseModel):
    host: str
    ip: str
    port: int
    lastseen: int
    delay: int
    cid: int
    country_code: Optional[str]
    country_name: Optional[str]
    city: Optional[str]
    checks_up: int
    checks_down: int
    anon: int
    http: int
    ssl: int
    socks4: int
    socks5: int


class ProxiesList(BaseModel):
    __root__: List[Proxy]


class DataRepository(data_repository.DataRepository):
    def __init__(self):
        scheme = 'https'
        netloc = 'hidemy.name'
        client = http_client.HttpClient(scheme, netloc)
        super().__init__(
            client,
            Proxy,
            ProxiesList,
        )

    def retrieve_proxy_dto_list_from_container(self, proxy_container: ProxiesList) -> List[Proxy]:
        return proxy_container.__root__

    def get_endpoint(self) -> str:
        endpoint = '/api/proxylist.txt'
        return endpoint

    def get_query_params(self) -> Dict:
        query_params = dict(
            out='js',
            http=1,
        )
        return query_params

    @property
    def source_type(self) -> proxies.ProxySourceIdType:
        return proxies.ProxySourceIdType("hidemyname")

    def proxy_from_dto(self, proxy_dto: Proxy) -> proxies.Proxy:
        schema: proxies.Proxy.ProtocolEnum
        schema = proxies.Proxy.ProtocolEnum.https if proxy_dto.ssl == 1 else proxies.Proxy.ProtocolEnum.http
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
        proxies_repository = cls()
        return proxies_repository
