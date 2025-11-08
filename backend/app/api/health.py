"""Health check endpoints for U-CHS backend application."""

from fastapi import APIRouter, Depends
from datetime import datetime
import logging
from typing import Dict

from ..models.schemas import HealthCheckResponse
from ..core.config import settings

logger = logging.getLogger(__name__)
router = APIRouter()


async def check_ml_service() -> bool:
    """Check if ML service is available."""
    try:
        from ..services.ml_service import MLService
        # Simple check - could be enhanced to actually test model loading
        return True
    except Exception as e:
        logger.error(f"ML service check failed: {e}")
        return False


async def check_storage_service() -> bool:
    """Check if storage service is available."""
    try:
        from ..services.storage_service import StorageService
        # Simple check - could be enhanced to test actual connectivity
        return True
    except Exception as e:
        logger.error(f"Storage service check failed: {e}")
        return False


async def check_database() -> bool:
    """Check if database is available."""
    try:
        # TODO: Add actual database connection check
        # For now, return True
        return True
    except Exception as e:
        logger.error(f"Database check failed: {e}")
        return False


@router.get("/", response_model=HealthCheckResponse)
async def health_check() -> HealthCheckResponse:
    """
    Basic health check endpoint.

    Returns:
        HealthCheckResponse: Application health status
    """
    return HealthCheckResponse(
        status="healthy",
        timestamp=datetime.utcnow(),
        version=settings.APP_VERSION,
        environment=settings.ENVIRONMENT,
        services={}
    )


@router.get("/detailed", response_model=HealthCheckResponse)
async def detailed_health_check() -> HealthCheckResponse:
    """
    Detailed health check endpoint with service status.

    Returns:
        HealthCheckResponse: Detailed application and service health status
    """
    # Check all services
    services_status: Dict[str, bool] = {
        "ml_service": await check_ml_service(),
        "storage_service": await check_storage_service(),
        "database": await check_database(),
    }

    # Determine overall status
    all_healthy = all(services_status.values())
    status = "healthy" if all_healthy else "degraded"

    logger.info(
        f"Health check performed - Status: {status}, Services: {services_status}"
    )

    return HealthCheckResponse(
        status=status,
        timestamp=datetime.utcnow(),
        version=settings.APP_VERSION,
        environment=settings.ENVIRONMENT,
        services=services_status
    )


@router.get("/ready")
async def readiness_check() -> Dict[str, str]:
    """
    Kubernetes readiness probe endpoint.

    Returns:
        Dict: Readiness status
    """
    # Check critical services
    ml_ready = await check_ml_service()
    storage_ready = await check_storage_service()

    if ml_ready and storage_ready:
        return {"status": "ready"}
    else:
        return {"status": "not_ready"}


@router.get("/live")
async def liveness_check() -> Dict[str, str]:
    """
    Kubernetes liveness probe endpoint.

    Returns:
        Dict: Liveness status
    """
    return {"status": "alive"}
