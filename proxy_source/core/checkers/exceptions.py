class IpServiceException(Exception):
    pass


class IpServiceNot200Exception(IpServiceException):
    status_code: int

    def __init__(self, status_code: int):
        self.status_code = status_code


class IpServiceParseResponseException(IpServiceException):
    content: bytes

    def __init__(self, content: bytes):
        self.content = content

    def __str__(self) -> str:
        return self.content.decode()


class IpServiceNetworkException(IpServiceException):
    pass
