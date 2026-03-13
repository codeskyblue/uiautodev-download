"""SPA serving routes."""

from pathlib import Path
from typing import Optional

from fastapi import APIRouter
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.config import settings

def create_spa_router(frontend_build_dir: Optional[Path] = None) -> APIRouter:
    """Create SPA router with optional custom build directory.

    Args:
        frontend_build_dir: Path to frontend build directory. If None, uses settings.

    Returns:
        APIRouter with SPA routes
    """
    if frontend_build_dir is None:
        frontend_build_dir = settings.frontend_build_dir

    spa_router = APIRouter()

    @spa_router.get("/")
    async def root():
        """Serve SPA index.html."""
        index_file = frontend_build_dir / "index.html"
        if index_file.exists():
            return FileResponse(str(index_file))
        return {"message": "uiautodev Download API", "docs": "/docs"}

    return spa_router


def setup_spa_static_files(app, frontend_build_dir: Optional[Path] = None) -> APIRouter:
    """Setup SPA static file serving and return SPA router.

    Args:
        app: FastAPI application instance
        frontend_build_dir: Path to frontend build directory. If None, uses settings.

    Returns:
        APIRouter with SPA routes
    """
    if frontend_build_dir is None:
        frontend_build_dir = settings.frontend_build_dir

    if not frontend_build_dir.exists():
        return create_spa_router(frontend_build_dir)

    # Mount _app directory for static assets
    app_dir = frontend_build_dir / "_app"
    if app_dir.exists():
        app.mount("/_app", StaticFiles(directory=str(app_dir)), name="app")

    # Mount robots.txt
    robots_file = frontend_build_dir / "robots.txt"
    if robots_file.exists():
        app.mount("/robots.txt", StaticFiles(directory=str(frontend_build_dir)), name="robots")

    return create_spa_router(frontend_build_dir)
