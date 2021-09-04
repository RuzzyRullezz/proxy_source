class IpServiceException(Exception):
    pass


class IpServiceNot200Exception(IpServiceException):
    status_code: int

    def __init__(self, status_code: int):
        self.status_code = status_code


class IpServiceNetworkException(IpServiceException):
    pass
