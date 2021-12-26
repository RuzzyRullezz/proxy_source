from typing import Type


class ProxySourceException(Exception):
    pass


class CantParseProxySourceDataException(ProxySourceException):
    model: Type
    data: bytes

    def __init__(self, model: Type, data: bytes):
        self.model = model
        self.data = data

    def __str__(self) -> str:
        return '{!r}'.format(b'Model: {self.model.__name__}\nCan\'t parse data:\n{self.data}')
