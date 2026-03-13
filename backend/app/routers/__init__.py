from fastapi import APIRouter
from .api import router as api_router
from .spa import setup_spa_static_files

router = APIRouter()

router.include_router(api_router, prefix='/api')

# Note: Static files must be mounted on the FastAPI app, not router
# This function is called from main.py
spa_static_router = None


def setup(app):
    """Setup SPA static files on the main app."""
    global spa_static_router
    spa_static_router = setup_spa_static_files(app)
    router.include_router(spa_static_router)