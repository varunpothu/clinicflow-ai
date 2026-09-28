from datetime import datetime
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.appointment import Appointment


class AppointmentRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

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
        await self.session.flush()
        return appointment
