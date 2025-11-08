"""API module for U-CHS backend application."""

from fastapi import APIRouter
from .health import router as health_router
from .analysis import router as analysis_router
from .images import router as images_router
from .users import router as users_router

# Create main API router
api_router = APIRouter()

# Include sub-routers
api_router.include_router(health_router, prefix="/health", tags=["Health"])
api_router.include_router(users_router, prefix="/users", tags=["Users"])
api_router.include_router(images_router, prefix="/images", tags=["Images"])
api_router.include_router(analysis_router, prefix="/analysis", tags=["Analysis"])

__all__ = ["api_router"]
