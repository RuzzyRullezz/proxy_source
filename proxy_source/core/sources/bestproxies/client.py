import datetime
from enum import Enum
from typing import Dict, Optional, Mapping, Any, Sequence

from urllib.parse import urlunsplit, urlencode

import aiohttp
from pydantic import BaseModel


class Client:

    class RequestMethodEnum(str, Enum):
        get = 'GET'
        post = 'POST'

    scheme: str = 'https'
    netloc: str = 'api.best-proxies.ru'
    encoding: str = 'utf-8'
    timeout: datetime.timedelta = datetime.timedelta(seconds=60)
    headers: Dict[str, str] = {
        'Content-Type': 'application/json',
        'Content-Encoding': encoding,
    }

    def get_full_url(self, endpoint: str, query_params: Optional[Mapping[Any, Sequence[Any]]] = None) -> str:
        query: Optional[str] = None
        if query_params is not None:
            query = urlencode(query_params)
        return urlunsplit((self.scheme, self.netloc, endpoint, query, None))

    @staticmethod
    def get_body_data(data: BaseModel) -> Dict:
        body_data: Dict = data.dict()
        return body_data

    async def send_request(
            self,
            url: str,
            method: RequestMethodEnum,
            data: Optional[BaseModel] = None,
    ) -> bytes:
        body_data: Optional[Dict] = None
        if method == self.RequestMethodEnum.post and data is not None:
            body_data = self.get_body_data(data)
        async with aiohttp.request(
            method.value,
            url,
            data=body_data,
            headers=self.headers,
        ) as response:
            return await response.read()

    async def send_get(self, endpoint: str, query_params: Optional[Mapping[Any, Sequence[Any]]] = None) -> bytes:
        full_url: str = self.get_full_url(endpoint, query_params=query_params)
        return await self.send_request(full_url, self.RequestMethodEnum.get)

    async def send_post(self, endpoint: str, data: Optional[BaseModel] = None) -> bytes:
        full_url: str = self.get_full_url(endpoint)
        return await self.send_request(full_url, self.RequestMethodEnum.post, data=data)
