"""Application configuration settings."""

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings.

    Attributes:
        r2_endpoint: Cloudflare R2 endpoint URL
        r2_access_key_id: R2 access key ID
        r2_secret_access_key: R2 secret access key
        r2_bucket_name: R2 bucket name
        r2_base_url: Base URL for R2 file downloads
        frontend_build_dir: Path to frontend build directory
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    r2_endpoint: str
    r2_access_key_id: str
    r2_secret_access_key: str
    r2_bucket_name: str
    r2_base_url: str = "https://dl.uiauto.dev"

    @property
    def frontend_build_dir(self) -> Path:
        """Get frontend build directory path."""
        project_root = Path(__file__).parent.parent.parent.parent
        return project_root / "frontend" / "build"


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance.

    Returns:
        Settings: Application settings
    """
    return Settings()


settings = get_settings()
