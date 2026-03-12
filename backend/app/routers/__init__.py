from fastapi import APIRouter
from .api import router as api_router
from .spa import setup_spa_static_files

router = APIRouter()

router.include_router(api_router, prefix='/api')

spa_router = setup_spa_static_files(router)
router.include_router(spa_router)