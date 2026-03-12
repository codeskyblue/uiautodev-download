from fastapi import APIRouter
from .versions import router as ver_router

router = APIRouter()

router.include_router(ver_router, prefix='/versions')