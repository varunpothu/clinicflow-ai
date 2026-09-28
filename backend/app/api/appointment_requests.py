from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.db.dependencies import get_session
from app.schemas.appointment import AppointmentRequestAccepted, AppointmentRequestCreate
from app.security.auth import Principal
from app.security.dependencies import require_demo_permission
from app.security.rbac import Permission
from app.services.persistent_intake import PersistentIntakeService

router = APIRouter(prefix="/appointment-requests", tags=["appointment-requests"])


@router.post("", response_model=AppointmentRequestAccepted, status_code=status.HTTP_202_ACCEPTED)
async def create_appointment_request(
    payload: AppointmentRequestCreate,
    idempotency_key: str = Header(min_length=8, max_length=200),
    principal: Principal = Depends(
        require_demo_permission(Permission.REQUEST_APPOINTMENT)
    ),
    session: AsyncSession = Depends(get_session),
) -> AppointmentRequestAccepted:
    if principal.role.value == "PATIENT" and principal.subject_id != payload.patient_id:
        raise HTTPException(status_code=403, detail="FORBIDDEN")

    service = PersistentIntakeService(session, get_settings())
    try:
        result = await service.create(
            patient_id=payload.patient_id,
            appointment_type=payload.appointment_type,
            natural_language=payload.natural_language,
            idempotency_key=idempotency_key,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc

    return AppointmentRequestAccepted.model_validate(result)
