import logging.config
import socket
from typing import Dict, Optional, Any, List, Type

from anyio import BrokenResourceError
from raven import Client
from raven.transport import RequestsHTTPTransport


class NonLoggableExceptionsFilter(logging.Filter):
    def filter(self, record):
        exception_types: List[Type[Exception]] = [
            BrokenResourceError,
        ]
        exception_type = record.exc_info[0]
        return exception_type not in exception_types


def get_dict_config(
        tg_token: Optional[str] = None,
        tg_chat: Optional[int] = None,
        sentry_dsn: Optional[str] = None,
) -> Dict[str, Any]:
    hostname: str = socket.gethostname()
    null_handler: Dict[str, str] = {
        "class": "logging.NullHandler",
    }
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "verbose": {
                "format": "%(asctime)s [%(levelname)s] [{0} %(name)s:%(lineno)s] %(message)s".format(hostname)
            }
        },
        "filters": {
            "non_loggable_exceptions": {
                "()": NonLoggableExceptionsFilter,
            },
        },
        "handlers": {
            "console_handler": {
                "level": "ERROR",
                "class": "logging.StreamHandler",
                "filters": ["non_loggable_exceptions"],
            },
            "telegram_handler": {
                "class": "telegram_log.handler.TelegramHandler",
                "token": tg_token,
                "chat_ids": [tg_chat],
                "err_log_name": None,
                "level": "ERROR",
                "formatter": "verbose",
                "filters": ["non_loggable_exceptions"],
            } if tg_token and tg_token else null_handler,
            "sentry_handler": {
                "class": "raven.handlers.logging.SentryHandler",
                "client_cls": Client,
                "dsn": sentry_dsn,
                "level": "ERROR",
                "transport": RequestsHTTPTransport,
                "filters": ["non_loggable_exceptions"],
            } if sentry_dsn else null_handler,
        },
        "loggers": {
            "root": {
                "level": "DEBUG",
                "handlers": ["console_handler", "telegram_handler", "sentry_handler"]
            },
        }
    }


def setup(
        tg_token: Optional[str] = None,
        tg_chat: Optional[int] = None,
        sentry_dsn: Optional[str] = None,
):
    dict_config = get_dict_config(tg_token=tg_token, tg_chat=tg_chat, sentry_dsn=sentry_dsn)
    logging.config.dictConfig(dict_config)
