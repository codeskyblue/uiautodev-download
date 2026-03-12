"""Test API endpoints."""

import pytest
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient

from main import app


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


@pytest.fixture
def mock_r2_service():
    """Mock R2 service."""
    with patch("app.routers.api.versions.r2_service") as mock:
        yield mock


class TestVersionsList:
    """Test GET /api/versions endpoint."""

    def test_get_versions_success(self, client, mock_r2_service):
        """Test successfully getting all versions."""
        # Setup mock
        mock_r2_service.list_versions.return_value = [
            "0.2.1", "0.2.0", "0.1.0"
        ]

        # Make request
        response = client.get("/api/versions")

        # Assertions
        assert response.status_code == 200
        assert response.json() == {
            "versions": ["0.2.1", "0.2.0", "0.1.0"]
        }
        mock_r2_service.list_versions.assert_called_once()

    def test_get_versions_empty(self, client, mock_r2_service):
        """Test getting versions when none exist."""
        # Setup mock
        mock_r2_service.list_versions.return_value = []

        # Make request
        response = client.get("/api/versions")

        # Assertions
        assert response.status_code == 200
        assert response.json() == {"versions": []}


class TestVersionDetail:
    """Test GET /api/versions/{version} endpoint."""

    def test_get_version_detail_success(self, client, mock_r2_service):
        """Test successfully getting version details."""
        # Setup mock
        mock_r2_service.get_version_detail.return_value = {
            "version": "0.2.1",
            "files": [
                {
                    "name": "uiautodev-desktop.dmg",
                    "size": 1024000,
                    "download_url": "https://dl.uiauto.dev/0.2.1/uiautodev-desktop.dmg"
                },
                {
                    "name": "uiautodev-windows.exe",
                    "size": 2048000,
                    "download_url": "https://dl.uiauto.dev/0.2.1/uiautodev-windows.exe"
                }
            ]
        }

        # Make request
        response = client.get("/api/versions/0.2.1")

        # Assertions
        assert response.status_code == 200
        data = response.json()
        assert data["version"] == "0.2.1"
        assert len(data["files"]) == 2
        mock_r2_service.get_version_detail.assert_called_once_with("0.2.1")

    def test_get_version_detail_not_found(self, client, mock_r2_service):
        """Test getting non-existent version."""
        # Setup mock
        mock_r2_service.get_version_detail.return_value = None

        # Make request
        response = client.get("/api/versions/999.0.0")

        # Assertions
        assert response.status_code == 404
        assert response.json() == {"detail": "Version not found"}
