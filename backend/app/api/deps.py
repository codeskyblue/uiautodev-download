"""API dependencies."""

from fastapi import Depends

from app.services.r2 import r2_service

__all__ = ["r2_service", "Depends"]
