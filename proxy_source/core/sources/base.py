from abc import ABC, abstractmethod
from typing import List

from proxy_source import config
from proxy_source.utils.date_time import utc_now
from proxy_source.vendors.rest_api.outgoing_request_log.requests.client import SessionLoggable

from ..proxies.models import Proxy, ProxyProtocolEnum
from . import bestproxies
from . import logs


class ProxySource(ABC):
    @property
    @abstractmethod
    def type(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_proxies(self) -> List[Proxy]:
        raise NotImplementedError


class BestProxiesSource(ProxySource):
    @property
    def type(self) -> str:
        return 'best_proxies'

    def get_proxies(self) -> List[Proxy]:
        repository = self.create_proxies_repository()
        dto_proxies_list = repository.get_proxy_list()
        proxy_list = list(map(self.proxy_from_dto, dto_proxies_list))
        return proxy_list

    @staticmethod
    def create_repo_client() -> bestproxies.client.Client:
        session = SessionLoggable(logs.store.create_outgoing_request_log)
        client = bestproxies.client.Client(session)
        return client

    def create_proxies_repository(self) -> bestproxies.repository.DataRepository:
        client = self.create_repo_client()
        assert config.BESTPROXIES_API_KEY is not None, 'set BESTPROXIES_API_KEY param in .env file'
        api_key = str(config.BESTPROXIES_API_KEY)
        proxies_repository = bestproxies.repository.DataRepository(client, api_key)
        return proxies_repository

    def proxy_from_dto(self, dto_proxy: bestproxies.dto.Proxy) -> Proxy:
        protocol: ProxyProtocolEnum
        protocol_established_marker: int = 1
        if dto_proxy.http == protocol_established_marker:
            protocol = ProxyProtocolEnum.http
        elif dto_proxy.https == protocol_established_marker:
            protocol = ProxyProtocolEnum.https
        else:
            raise NotImplementedError("Unsupported proxy protocol.")
        return Proxy(
            protocol=protocol,
            ip=dto_proxy.ip,
            port=dto_proxy.port,
            user=None,
            password=None,
            source=self.type,
            created_at=utc_now(),
        )
