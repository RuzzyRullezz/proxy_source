import datetime
from enum import Enum
from typing import Dict, Optional

from urllib.parse import urlunsplit, urlencode

import httpx
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

    httpx_client: httpx.AsyncClient

    def __init__(self, httpx_client: httpx.AsyncClient):
        self.httpx_client = httpx_client

    def get_full_url(self, endpoint: str, query_params: Optional[Dict[str, str]] = None) -> str:
        query: str = urlencode(query_params)
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
        body_data: Optional[Dict]
        if method == self.RequestMethodEnum.get:
            body_data = None
        elif method == self.RequestMethodEnum.post:
            body_data = self.get_body_data(data)
        else:
            raise NotImplementedError(f"Unsupported request method = {method}")
        request: httpx.Request = httpx.Request(
            method.value,
            url,
            data=body_data,
            headers=self.headers,
        )
        async with self.httpx_client as client:
            response: httpx.Response = await client.send(request, timeout=self.timeout.total_seconds())
        return response.content

    async def send_get(self, endpoint: str, query_params: Optional[Dict[str, str]] = None) -> bytes:
        full_url: str = self.get_full_url(endpoint, query_params=query_params)
        return await self.send_request(full_url, self.RequestMethodEnum.get)

    async def send_post(self, endpoint: str, data: Optional[BaseModel] = None) -> bytes:
        full_url: str = self.get_full_url(endpoint)
        return await self.send_request(full_url, self.RequestMethodEnum.post, data=data)
