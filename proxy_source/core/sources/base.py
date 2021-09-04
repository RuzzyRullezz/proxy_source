from abc import ABC, abstractmethod
from typing import List

from ..proxies import Proxy


class ProxySource(ABC):
    @property
    @abstractmethod
    def type(self) -> Proxy.SourceEnum:
        raise NotImplementedError

    @abstractmethod
    def get_proxies(self) -> List[Proxy]:
        raise NotImplementedError
