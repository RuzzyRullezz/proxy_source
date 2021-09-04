import logging.config
import socket
from typing import Dict, Optional, Any

from raven import Client  # type: ignore
from raven.transport import RequestsHTTPTransport  # type: ignore


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
        "filters": {},
        "handlers": {
            "console_handler": {
                "class": "logging.StreamHandler",
            },
            "telegram_handler": {
                "class": "telegram_log.handler.TelegramHandler",
                "token": tg_token,
                "chat_ids": [tg_chat],
                "err_log_name": None,
                "level": "ERROR",
                "formatter": "verbose",
                "filters": [],
            } if tg_token and tg_token else null_handler,
            "sentry_handler": {
                "class": "raven.handlers.logging.SentryHandler",
                "client_cls": Client,
                "dsn": sentry_dsn,
                "level": "ERROR",
                "transport": RequestsHTTPTransport,
                "filters": [],
            } if sentry_dsn else null_handler,
        },
        "loggers": {
            "root": {
                "level": "INFO",
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
