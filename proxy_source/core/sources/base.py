from abc import ABC, abstractmethod
from typing import List

from .. import proxies
from .. import checkers


class ProxySource(ABC):
    @property
    @abstractmethod
    def type(self) -> proxies.Proxy.SourceEnum:
        raise NotImplementedError

    @abstractmethod
    async def get_all_proxies(self) -> List[proxies.Proxy]:
        raise NotImplementedError

    async def get_proxies(self) -> List[proxies.Proxy]:
        all_proxies = await self.get_all_proxies()
        alive_anon_proxies = await checkers.filter_alive_anon_proxies(all_proxies)
        return alive_anon_proxies
