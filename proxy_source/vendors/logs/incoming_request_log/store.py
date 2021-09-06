from abc import abstractmethod
from typing import Protocol, runtime_checkable

from .context import LogContextIncoming
from .models import IncomingRequestBase


@runtime_checkable
class IIncomingRequestStore(Protocol):
    @staticmethod
    @abstractmethod
    async def save_incoming_log(log_context: LogContextIncoming) -> IncomingRequestBase:
        raise NotImplementedError()
