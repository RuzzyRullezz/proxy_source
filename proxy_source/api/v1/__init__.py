from fastapi import APIRouter

from .proxies.controllers import router as proxies_router

router = APIRouter()
router.include_router(proxies_router, prefix='/proxies')
