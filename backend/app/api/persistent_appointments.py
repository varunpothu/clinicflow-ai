from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, Header, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.appointment import Appointment

from app.core.correlation import get_correlation_id
from app.db.dependencies import get_session
from app.security.auth import Principal
from app.security.dependencies import require_demo_permission
from app.security.rbac import Permission
from app.services.persistent_lifecycle import PersistentAppointmentLifecycleService

router = APIRouter(prefix="/persistent-appointments", tags=["persistent-appointments"])


class RescheduleCommand(BaseModel):
    expected_version: int = Field(ge=1)
    new_starts_at: datetime
    new_ends_at: datetime


def assert_patient_access(principal: Principal, patient_id: UUID) -> None:
    if principal.role.value == "PATIENT" and principal.subject_id != patient_id:
        raise HTTPException(status_code=403, detail="FORBIDDEN")


@router.get("/me")
async def list_my_appointments(
    principal: Principal = Depends(require_demo_permission(Permission.VIEW_OWN_APPOINTMENTS)),
    session: AsyncSession = Depends(get_session),
) -> list[dict[str, object]]:
    result = await session.execute(
        select(Appointment).where(Appointment.patient_id == principal.subject_id).order_by(Appointment.starts_at)
    )
    return [
        {
            "appointment_id": str(item.id),
            "clinician_id": str(item.clinician_id),
            "appointment_type": item.appointment_type,
            "starts_at": item.starts_at.isoformat(),
            "ends_at": item.ends_at.isoformat(),
            "status": item.status,
            "version": item.version,
        }
        for item in result.scalars().all()
    ]


@router.post("/{appointment_id}/cancel")
async def cancel_appointment(
    appointment_id: UUID,
    idempotency_key: str = Header(min_length=8, max_length=200),
    principal: Principal = Depends(
        require_demo_permission(Permission.CANCEL_OWN_APPOINTMENT)
    ),
    session: AsyncSession = Depends(get_session),
) -> dict[str, object]:
    service = PersistentAppointmentLifecycleService(session)
    appointment = await service.appointments.get(appointment_id)
    if appointment is None:
        raise HTTPException(status_code=404, detail="APPOINTMENT_NOT_FOUND")
    assert_patient_access(principal, UUID(str(appointment.patient_id)))
    try:
        return await service.cancel(
            appointment_id=appointment_id,
            actor_id=principal.subject_id,
            idempotency_key=idempotency_key,
            correlation_id=get_correlation_id(),
        )
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@router.post("/{appointment_id}/reschedule")
async def reschedule_appointment(
    appointment_id: UUID,
    command: RescheduleCommand,
    idempotency_key: str = Header(min_length=8, max_length=200),
    principal: Principal = Depends(
        require_demo_permission(Permission.RESCHEDULE_OWN_APPOINTMENT)
    ),
    session: AsyncSession = Depends(get_session),
) -> dict[str, object]:
    service = PersistentAppointmentLifecycleService(session)
    appointment = await service.appointments.get(appointment_id)
    if appointment is None:
        raise HTTPException(status_code=404, detail="APPOINTMENT_NOT_FOUND")
    assert_patient_access(principal, UUID(str(appointment.patient_id)))
    try:
        return await service.reschedule(
            appointment_id=appointment_id,
            actor_id=principal.subject_id,
            new_starts_at=command.new_starts_at,
            new_ends_at=command.new_ends_at,
            expected_version=command.expected_version,
            idempotency_key=idempotency_key,
            correlation_id=get_correlation_id(),
        )
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
