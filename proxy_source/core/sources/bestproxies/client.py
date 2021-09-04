import datetime
from enum import Enum
from typing import Dict, Optional

from urllib.parse import urlunsplit, urlencode

import requests
from pydantic import BaseModel
from requests import Session, Response


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

    session: Session

    def __init__(self, session: Session):
        self.session = session

    def get_full_url(self, endpoint: str, query_params: Optional[Dict[str, str]] = None) -> str:
        query: str = urlencode(query_params)
        return urlunsplit((self.scheme, self.netloc, endpoint, query, None))

    @staticmethod
    def get_body_data(data: BaseModel) -> Dict:
        body_data: Dict = data.dict()
        return body_data

    def send_request(
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
        prepared_request: requests.PreparedRequest = requests.Request(
            method.value,
            url,
            data=body_data,
            headers=self.headers,
        ).prepare()
        response: Response = self.session.send(prepared_request, timeout=self.timeout.total_seconds())
        return response.content

    def send_get(self, endpoint: str, query_params: Optional[Dict[str, str]] = None) -> bytes:
        full_url: str = self.get_full_url(endpoint, query_params=query_params)
        return self.send_request(full_url, self.RequestMethodEnum.get)

    def send_post(self, endpoint: str, data: Optional[BaseModel] = None) -> bytes:
        full_url: str = self.get_full_url(endpoint)
        return self.send_request(full_url, self.RequestMethodEnum.post, data=data)
