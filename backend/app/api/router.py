from fastapi import APIRouter

from app.api.appointment_requests import router as appointment_requests_router
from app.api.booking import router as booking_router
from app.api.health import router as health_router
from app.api.operations import router as operations_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(health_router)
api_router.include_router(appointment_requests_router)
api_router.include_router(booking_router)
api_router.include_router(operations_router)
