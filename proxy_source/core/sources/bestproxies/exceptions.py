class BestProxiesException(Exception):
    pass


class CantParseBestProxiesResponseException(BestProxiesException):
    content: bytes

    def __init__(self, content: bytes):
        self.content = content

    def __str__(self) -> str:
        return '{!r}'.format(b'Can\'t parse content:\n{self.content}')
