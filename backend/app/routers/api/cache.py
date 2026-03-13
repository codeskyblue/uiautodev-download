"""Cache API routes."""

from fastapi import APIRouter

from app.services.r2 import r2_service

router = APIRouter()


@router.get("/clear")
async def clear_cache() -> dict:
    """Clear all version-related caches.

    Returns:
        Success message
    """
    await r2_service.clear_cache()
    return {"message": "Cache cleared successfully"}
