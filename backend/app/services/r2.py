"""R2 storage service for managing version files."""

import re
from typing import Optional

import asyncio
import boto3
from botocore.exceptions import ClientError
from cashews import cache

from app.config import settings
from app.schemas.version import VersionDetail, FileInfo

# Cache TTL: 10 minutes
CACHE_TTL = "10m"


class R2Service:
    """Service for interacting with Cloudflare R2 storage."""

    def __init__(self):
        """Initialize R2 service with application settings."""
        self.endpoint = settings.r2_endpoint
        self.access_key = settings.r2_access_key_id
        self.secret_key = settings.r2_secret_access_key
        self.bucket = settings.r2_bucket_name
        self.base_url = settings.r2_base_url
        self.s3_client = boto3.client(
            "s3",
            endpoint_url=self.endpoint,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
        )

    @cache(ttl=CACHE_TTL, key="versions:list")
    async def list_versions(self) -> list[str]:
        """List all available versions (cached for 10 minutes).

        Returns:
            List of version strings sorted in descending order.
        """
        return await asyncio.to_thread(self._list_versions_sync)

    def _list_versions_sync(self) -> list[str]:
        """Synchronous implementation of list_versions."""
        try:
            paginator = self.s3_client.get_paginator("list_objects_v2")
            result = paginator.paginate(Bucket=self.bucket, Delimiter="/")

            versions = []
            for prefix in result.search("CommonPrefixes"):
                if prefix:
                    version = prefix.get("Prefix", "").rstrip("/")
                    if version and re.match(r"^\d+\.\d+\.\d+$", version):
                        versions.append(version)

            return sorted(versions, reverse=True)

        except ClientError as e:
            raise RuntimeError(f"Failed to list versions: {e}")

    @cache(ttl=CACHE_TTL, key="version:{version}")
    async def get_version_detail(self, version: str) -> Optional[VersionDetail]:
        """Get detailed information about a specific version (cached for 10 minutes).

        Args:
            version: Version string (e.g., "0.2.1")

        Returns:
            VersionDetail object with file list, or None if not found.
        """
        return await asyncio.to_thread(self._get_version_detail_sync, version)

    def _get_version_detail_sync(self, version: str) -> Optional[VersionDetail]:
        """Synchronous implementation of get_version_detail."""
        try:
            prefix = f"{version}/"
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket,
                Prefix=prefix,
            )

            if "Contents" not in response:
                return None

            files = []
            for obj in response["Contents"]:
                file_name = obj["Key"].replace(prefix, "")
                if file_name:
                    files.append(FileInfo(
                        name=file_name,
                        size=obj["Size"],
                        download_url=f"{self.base_url}/{obj['Key']}"
                    ))

            return VersionDetail(
                version=version,
                files=files
            )

        except ClientError as e:
            raise RuntimeError(f"Failed to get version detail: {e}")

    async def clear_cache(self) -> None:
        """Clear all version-related caches.

        This clears both the versions list cache and individual version detail caches.
        """
        await cache.delete("versions:list")
        # Clear individual version caches
        await cache.clear()


# Create global service instance
r2_service = R2Service()
