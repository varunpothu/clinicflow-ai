from datetime import datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.appointment import Appointment


class AppointmentConflictError(Exception):
    """Raised when database constraints reject an appointment write."""


class AppointmentRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self, appointment_id: UUID) -> Appointment | None:
        result = await self.session.execute(
            select(Appointment).where(Appointment.id == appointment_id)
        )
        return result.scalar_one_or_none()

    async def create(
        self,
        *,
        patient_id: UUID,
        clinician_id: UUID,
        appointment_type: str,
        starts_at: datetime,
        ends_at: datetime,
        status: str = "CONFIRMED",
    ) -> Appointment:
        appointment = Appointment(
            patient_id=patient_id,
            clinician_id=clinician_id,
            appointment_type=appointment_type,
            starts_at=starts_at,
            ends_at=ends_at,
            status=status,
        )
        self.session.add(appointment)
        try:
            await self.session.flush()
        except IntegrityError as exc:
            raise AppointmentConflictError("APPOINTMENT_CONFLICT") from exc
        return appointment
