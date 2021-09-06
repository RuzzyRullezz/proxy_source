from typing import TypeVar, Type, List, cast, Mapping, Any, Sequence

from pydantic import BaseModel, ValidationError

from . import dto
from . import exceptions
from . import client as repo_client


TModel = TypeVar('TModel', bound=BaseModel)


class DataRepository:
    client: repo_client.Client
    api_key: str

    def __init__(self, client: repo_client.Client, api_key: str):
        self.client = client
        self.api_key = api_key

    @staticmethod
    def parse(model: Type[TModel], response: bytes) -> TModel:
        try:
            return model.parse_raw(response)
        except ValidationError:
            raise exceptions.CantParseBestProxiesResponseException(response)

    async def get_proxy_list(self) -> List[dto.Proxy]:
        endpoint = 'proxylist.json'
        query_params = cast(
            Mapping[Any, Sequence[Any]],
            dict(
                key=self.api_key,
                type='http,https',
                response=1000,
                speed=1,
                level=1,
                limit=0,
            )
        )
        response = await self.client.send_get(endpoint, query_params=query_params)
        dto_proxies_list: dto.ProxiesList = self.parse(dto.ProxiesList, response)
        return dto_proxies_list.__root__
