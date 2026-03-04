"""Test SPA serving."""

import pytest
from pathlib import Path
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.routers.spa import setup_spa_static_files


class TestSPAServing:
    """Test SPA file serving."""

    def test_setup_spa_registers_root_route(self, tmp_path):
        """Test that setup_spa registers root route."""
        # Create a temporary frontend build directory with index.html
        build_dir = tmp_path / "frontend" / "build"
        build_dir.mkdir(parents=True)
        (build_dir / "index.html").write_text("<html><body>Test SPA</body></html>")

        # Create a new FastAPI app and setup SPA
        test_app = FastAPI()
        spa_router = setup_spa_static_files(test_app, frontend_build_dir=build_dir)
        test_app.include_router(spa_router)

        # Test the root route
        client = TestClient(test_app)
        response = client.get("/")
        assert response.status_code == 200
        assert "Test SPA" in response.text

    def test_setup_spa_with_missing_build_dir(self):
        """Test that setup_spa handles missing build directory gracefully."""
        test_app = FastAPI()
        # Use a non-existent path
        setup_spa_static_files(test_app, frontend_build_dir=Path("/nonexistent/path"))

        # Should not register any routes
        client = TestClient(test_app)
        response = client.get("/")
        assert response.status_code == 404

    def test_health_endpoint(self):
        """Test health check endpoint."""
        from main import app
        client = TestClient(app)
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}
