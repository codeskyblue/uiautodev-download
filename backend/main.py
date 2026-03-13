"""Main FastAPI application."""

import asyncio
import os
from contextlib import asynccontextmanager

from cashews import cache
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.services.r2 import r2_service


# Configure cache (in-memory backend)
cache.setup("mem://")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup - warm up cache in background
    async def warm_cache():
        try:
            await r2_service.list_versions()
        except Exception:
            pass

    asyncio.create_task(warm_cache())
    yield
    # Shutdown
    await cache.clear()


app = FastAPI(
    title="uiautodev Download API",
    description="Download API for uiautodev tools",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
from app.routers import router, setup
setup(app)
app.include_router(router)


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    from app.config import settings

    print(settings.model_dump_json(indent=2))
    port = int(os.getenv("PORT", 7001))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True,
    )
