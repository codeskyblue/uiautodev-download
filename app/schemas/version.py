"""Version-related API response schemas."""

from pydantic import BaseModel


class FileInfo(BaseModel):
    """File information model."""

    name: str
    size: int
    download_url: str


class VersionDetail(BaseModel):
    """Version detail model."""

    version: str
    files: list[FileInfo]


class VersionsList(BaseModel):
    """List of versions model."""

    versions: list[str]
