from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from proxy_source import config

from . import routing


cors_middleware_params = dict(
    allow_origins=config.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


def init_app():
    title = 'Proxies API'
    application = FastAPI(title=title)
    application.add_middleware(CORSMiddleware, **cors_middleware_params)
    application.include_router(routing.root_router, prefix='')
    return application


config.setup_logging()
app = init_app()
