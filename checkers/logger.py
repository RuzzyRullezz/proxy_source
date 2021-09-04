import logging

from proxy_source import config


config.setup_logging()


try:
    raise RuntimeError("test error")
except Exception as exc:
    logging.getLogger().exception(exc)
