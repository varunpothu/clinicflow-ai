from fastapi import APIRouter, HTTPException, status

from app.core.config import get_settings
from app.schemas.appointment import AppointmentRequestAccepted, AppointmentRequestCreate
from app.workflows.intake import AppointmentIntakeWorkflow

router = APIRouter(prefix="/appointment-requests", tags=["appointment-requests"])


@router.post("", response_model=AppointmentRequestAccepted, status_code=status.HTTP_202_ACCEPTED)
def create_appointment_request(payload: AppointmentRequestCreate) -> AppointmentRequestAccepted:
    workflow = AppointmentIntakeWorkflow(get_settings())
    try:
        result = workflow.start(
            patient_id=payload.patient_id,
            appointment_type=payload.appointment_type,
            natural_language=payload.natural_language,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"code": str(exc)},
        ) from exc

    return AppointmentRequestAccepted(
        request_id=result.request.request_id,
        status="accepted",
        next_state=result.state,
        ai_intent=result.ai_intent,
        validation_errors=result.validation.errors,
    )
