from uuid import UUID

from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.db.dependencies import get_session
from app.repositories.appointment_requests import AppointmentRequestRepository
from app.schemas.appointment import AppointmentRequestAccepted, AppointmentRequestCreate
from app.security.auth import Principal
from app.security.dependencies import require_demo_permission
from app.security.rbac import Permission
from app.services.persistent_intake import PersistentIntakeService

router = APIRouter(prefix="/appointment-requests", tags=["appointment-requests"])


@router.get("/{request_id}")
async def get_appointment_request(
    request_id: UUID,
    principal: Principal = Depends(
        require_demo_permission(Permission.REQUEST_APPOINTMENT)
    ),
    session: AsyncSession = Depends(get_session),
) -> dict[str, object]:
    record = await AppointmentRequestRepository(session).get(UUID(str(request_id)))
    if record is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="REQUEST_NOT_FOUND")
    if principal.role.value == "PATIENT" and principal.subject_id != UUID(record.patient_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="FORBIDDEN")
    return {
        "request_id": record.id,
        "patient_id": record.patient_id,
        "appointment_type": record.appointment_type,
        "status": record.status,
        "created_at": record.created_at.isoformat(),
    }


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
