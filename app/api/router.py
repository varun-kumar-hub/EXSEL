from fastapi import APIRouter
from app.api.routes.auth import router as auth_router
from app.api.routes.dashboard import router as dashboard_router
from app.api.routes.gates import router as gates_router
from app.api.routes.sensors import router as sensors_router
from app.api.routes.alerts import router as alerts_router
from app.api.routes.distribution import router as distribution_router
from app.api.routes.analytics import router as analytics_router
from app.api.routes.history import router as history_router

api_router = APIRouter(prefix="/api")

api_router.include_router(auth_router)
api_router.include_router(dashboard_router)
api_router.include_router(gates_router)
api_router.include_router(sensors_router)
api_router.include_router(alerts_router)
api_router.include_router(distribution_router)
api_router.include_router(analytics_router)
api_router.include_router(history_router)

__all__ = ["api_router"]
