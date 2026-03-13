"""Version API routes."""

from fastapi import APIRouter, HTTPException

from app.schemas.version import VersionsList, VersionDetail
from app.services.r2 import r2_service

router = APIRouter()


@router.get("", response_model=VersionsList)
async def list_versions() -> VersionsList:
    """Get list of all available versions.

    Returns versions sorted in descending order (newest first).
    """
    versions = await r2_service.list_versions()
    return VersionsList(versions=versions)


@router.get("/{version:str}", response_model=VersionDetail)
async def get_version_detail(version: str) -> VersionDetail:
    """Get detailed information about a specific version.

    Args:
        version: Version string (e.g., "0.2.1")

    Returns:
        Version detail with file list

    Raises:
        HTTPException: If version is not found
    """
    detail = await r2_service.get_version_detail(version)
    if detail is None:
        raise HTTPException(status_code=404, detail="Version not found")
    return detail
