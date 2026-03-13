"""Test API endpoints."""

import pytest
from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient

from main import app


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


class TestVersionsList:
    """Test GET /api/versions endpoint."""

    def test_get_versions_success(self, client):
        """Test successfully getting all versions."""
        with patch("app.services.r2.r2_service.list_versions",
                   AsyncMock(return_value=["0.2.1", "0.2.0", "0.1.0"])):
            response = client.get("/api/versions")
            assert response.status_code == 200
            assert response.json() == {"versions": ["0.2.1", "0.2.0", "0.1.0"]}

    def test_get_versions_empty(self, client):
        """Test getting versions when none exist."""
        with patch("app.services.r2.r2_service.list_versions",
                   AsyncMock(return_value=[])):
            response = client.get("/api/versions")
            assert response.status_code == 200
            assert response.json() == {"versions": []}


class TestVersionDetail:
    """Test GET /api/versions/{version} endpoint."""

    def test_get_version_detail_success(self, client):
        """Test successfully getting version details."""
        with patch("app.services.r2.r2_service.get_version_detail",
                   AsyncMock(return_value={
                       "version": "0.2.1",
                       "files": [
                           {"name": "uiautodev-desktop.dmg", "size": 1024000,
                            "download_url": "https://dl.uiauto.dev/0.2.1/uiautodev-desktop.dmg"},
                           {"name": "uiautodev-windows.exe", "size": 2048000,
                            "download_url": "https://dl.uiauto.dev/0.2.1/uiautodev-windows.exe"}
                       ]
                   })):
            response = client.get("/api/versions/0.2.1")
            assert response.status_code == 200
            data = response.json()
            assert data["version"] == "0.2.1"
            assert len(data["files"]) == 2

    def test_get_version_detail_not_found(self, client):
        """Test getting non-existent version."""
        with patch("app.services.r2.r2_service.get_version_detail",
                   AsyncMock(return_value=None)):
            response = client.get("/api/versions/999.0.0")
            assert response.status_code == 404
            assert response.json() == {"detail": "Version not found"}


class TestCacheClear:
    """Test GET /api/cache/clear endpoint."""

    def test_clear_cache_success(self, client):
        """Test successfully clearing cache."""
        with patch("app.services.r2.r2_service.clear_cache",
                   AsyncMock(return_value=None)):
            response = client.get("/api/cache/clear")
            assert response.status_code == 200
            assert response.json() == {"message": "Cache cleared successfully"}
