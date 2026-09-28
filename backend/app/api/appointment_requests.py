from uuid import uuid4

from fastapi import APIRouter, HTTPException, status

from app.domain.appointment_request import AppointmentRequest
from app.domain.validation import validate_request
from app.schemas.appointment import AppointmentRequestAccepted, AppointmentRequestCreate

router = APIRouter(prefix="/appointment-requests", tags=["appointment-requests"])


@router.post("", response_model=AppointmentRequestAccepted, status_code=status.HTTP_202_ACCEPTED)
def create_appointment_request(payload: AppointmentRequestCreate) -> AppointmentRequestAccepted:
    request = AppointmentRequest(request_id=uuid4(), **payload.model_dump())
    validation = validate_request(request)
    if not validation.valid:
        raise HTTPException(status_code=422, detail={"code": "INVALID_REQUEST", "errors": validation.errors})
    return AppointmentRequestAccepted(
        request_id=request.request_id,
        status="accepted",
        next_state="EXTRACTING" if request.natural_language else "VALIDATING",
    )
