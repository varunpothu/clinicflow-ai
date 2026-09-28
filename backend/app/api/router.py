from fastapi import APIRouter

from app.api.appointment_requests import router as appointment_requests_router
from app.api.booking import router as booking_router
from app.api.health import router as health_router
from app.api.operations import router as operations_router
from app.api.patient import router as patient_router
from app.api.persistent_appointments import router as persistent_appointments_router
from app.api.persistent_booking import router as persistent_booking_router
from app.api.waitlist import router as waitlist_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(health_router)
api_router.include_router(appointment_requests_router)
api_router.include_router(booking_router)
api_router.include_router(persistent_booking_router)
api_router.include_router(operations_router)
api_router.include_router(patient_router)
api_router.include_router(persistent_appointments_router)
api_router.include_router(waitlist_router)
