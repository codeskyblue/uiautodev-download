from fastapi import APIRouter
from .versions import router as ver_router
from .cache import router as cache_router

router = APIRouter()

router.include_router(ver_router, prefix='/versions')
router.include_router(cache_router, prefix='/cache')