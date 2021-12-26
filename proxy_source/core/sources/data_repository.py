from __future__ import annotations

import abc
from abc import ABC
from typing import TypeVar, Type, List, Dict, Generic

from pydantic import BaseModel, ValidationError

from .. import proxies
from . import http_client
from . import exceptions


TProxyDTOContainer = TypeVar('TProxyDTOContainer', bound=BaseModel)
TProxyDTO = TypeVar('TProxyDTO', bound=BaseModel)


class DataRepository(ABC, Generic[TProxyDTO, TProxyDTOContainer]):
    client: http_client.HttpClient
    proxy_dto_type: Type[TProxyDTO]
    proxy_dto_container_type: Type[TProxyDTOContainer]

    def __init__(
            self,
            client: http_client.HttpClient,
            proxy_dto_type: Type[TProxyDTO],
            proxy_dto_container_type: Type[TProxyDTOContainer],
    ):
        self.client = client
        self.proxy_dto_type = proxy_dto_type
        self.proxy_dto_container_type = proxy_dto_container_type

    async def get_proxy_list(self) -> List[proxies.Proxy]:
        proxy_dto_list = await self.get_proxy_dto_list()
        proxy_list = list(map(self.proxy_from_dto, proxy_dto_list))
        return proxy_list

    async def get_proxy_dto_list(self) -> List[TProxyDTO]:
        proxy_list_container = await self.get_proxy_dto_container()
        return self.retrieve_proxy_dto_list_from_container(proxy_list_container)

    async def get_proxy_dto_container(self) -> TProxyDTOContainer:
        data = await self.get_data()
        proxy_container: TProxyDTOContainer = self.parse(data)
        return proxy_container

    @abc.abstractmethod
    def retrieve_proxy_dto_list_from_container(self, proxy_container: TProxyDTOContainer) -> List[TProxyDTO]:
        raise NotImplementedError()

    async def get_data(self) -> bytes:
        endpoint = self.get_endpoint()
        query_params = self.get_query_params()
        response = await self.client.send_get(endpoint, query_params=query_params)
        return response

    @abc.abstractmethod
    def get_endpoint(self) -> str:
        raise NotImplementedError()

    @abc.abstractmethod
    def get_query_params(self) -> Dict:
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def source_type(self) -> proxies.ProxySourceIdType:
        raise NotImplementedError()

    def parse(self, data: bytes) -> TProxyDTOContainer:
        try:
            return self.proxy_dto_container_type.parse_raw(data)
        except ValidationError:
            raise exceptions.CantParseProxySourceDataException(self.proxy_dto_container_type, data)

    @abc.abstractmethod
    def proxy_from_dto(self, proxy_dto: TProxyDTO) -> proxies.Proxy:
        raise NotImplementedError()

    @classmethod
    @abc.abstractmethod
    def create(cls) -> DataRepository:
        raise NotImplementedError()
