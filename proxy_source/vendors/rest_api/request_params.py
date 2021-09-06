from typing import Optional, Callable, cast

from fastapi import Request


def get_ip_address(header_key: str = "X-Real-IP") -> Callable[[Request], Optional[str]]:
    def inner(request: Request) -> Optional[str]:
        header_data: Optional[str] = request.headers.get(header_key, None)
        if not header_data:
            return None
        return header_data.split(",")[0]
    return inner


def get_user_agent(request: Request) -> Optional[str]:
    return cast(Optional[str], request.headers.get('user-agent', None))
