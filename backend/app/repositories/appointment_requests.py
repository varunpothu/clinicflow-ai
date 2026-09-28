from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.appointment_request import AppointmentRequest


class AppointmentRequestRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self, request_id: UUID) -> AppointmentRequest | None:
        result = await self.session.execute(
            select(AppointmentRequest).where(
                AppointmentRequest.id == str(request_id)
            )
        )
        return result.scalar_one_or_none()

    async def create(
        self,
        *,
        request_id: UUID,
        patient_id: UUID,
        appointment_type: str,
        natural_language: str | None,
        status: str,
    ) -> AppointmentRequest:
        request = AppointmentRequest(
            id=str(request_id),
            patient_id=str(patient_id),
            appointment_type=appointment_type,
            natural_language=natural_language,
            status=status,
            created_at=datetime.now(UTC),
        )
        self.session.add(request)
        await self.session.flush()
        return request
