from datetime import UTC, datetime
import json
from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.appointment import Appointment
from app.repositories.appointments import AppointmentRepository
from app.repositories.audit import AuditRepository
from app.repositories.idempotency import PersistentIdempotencyRepository
from app.repositories.outbox import OutboxRepository


class PersistentAppointmentLifecycleService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.appointments = AppointmentRepository(session)
        self.idempotency = PersistentIdempotencyRepository(session)
        self.audit = AuditRepository(session)
        self.outbox = OutboxRepository(session)

    async def cancel(
        self,
        *,
        appointment_id: UUID,
        actor_id: UUID,
        idempotency_key: str,
        correlation_id: str,
    ) -> dict[str, object]:
        fingerprint = f"cancel:{appointment_id}:{actor_id}"

        async with self.session.begin():
            existing = await self.idempotency.get(idempotency_key)
            if existing is not None:
                if existing.fingerprint != fingerprint:
                    raise ValueError("IDEMPOTENCY_KEY_REUSE")
                decoded = json.loads(existing.result_json)
                if isinstance(decoded, dict):
                    return decoded
                raise ValueError("IDEMPOTENCY_RECORD_INVALID")

            appointment = await self.appointments.get(appointment_id)
            self._require_active(appointment)
            if appointment is None:
                raise AssertionError("unreachable")

            appointment.status = "CANCELLED"
            appointment.version += 1
            result: dict[str, object] = {
                "appointment_id": str(appointment.id),
                "status": appointment.status,
                "version": appointment.version,
            }
            now = datetime.now(UTC)
            await self.audit.record(
                event_type="APPOINTMENT_CANCELLED",
                summary="Appointment cancelled by authorised actor.",
                correlation_id=correlation_id,
                actor_id=actor_id,
                entity_id=appointment.id,
                occurred_at=now,
            )
            await self.outbox.add(
                aggregate_id=appointment.id,
                event_type="APPOINTMENT_CANCELLED",
                payload=result | {"correlation_id": correlation_id},
                occurred_at=now,
            )
            await self.idempotency.put(idempotency_key, fingerprint, result)
            return result

    async def reschedule(
        self,
        *,
        appointment_id: UUID,
        actor_id: UUID,
        new_starts_at: datetime,
        new_ends_at: datetime,
        expected_version: int,
        idempotency_key: str,
        correlation_id: str,
    ) -> dict[str, object]:
        if new_starts_at.tzinfo is None or new_ends_at.tzinfo is None:
            raise ValueError("TIMEZONE_REQUIRED")
        if new_ends_at <= new_starts_at:
            raise ValueError("INVALID_RESCHEDULE_RANGE")

        fingerprint = (
            f"reschedule:{appointment_id}:{expected_version}:"
            f"{new_starts_at.isoformat()}:{new_ends_at.isoformat()}"
        )

        async with self.session.begin():
            existing = await self.idempotency.get(idempotency_key)
            if existing is not None:
                if existing.fingerprint != fingerprint:
                    raise ValueError("IDEMPOTENCY_KEY_REUSE")
                decoded = json.loads(existing.result_json)
                if isinstance(decoded, dict):
                    return decoded
                raise ValueError("IDEMPOTENCY_RECORD_INVALID")

            appointment = await self.appointments.get(appointment_id)
            self._require_active(appointment)
            if appointment is None:
                raise AssertionError("unreachable")
            if appointment.version != expected_version:
                raise ValueError("STALE_APPOINTMENT")

            appointment.starts_at = new_starts_at.astimezone(UTC)
            appointment.ends_at = new_ends_at.astimezone(UTC)
            appointment.version += 1

            try:
                await self.session.flush()
            except IntegrityError as exc:
                raise ValueError("APPOINTMENT_CONFLICT") from exc

            result: dict[str, object] = {
                "appointment_id": str(appointment.id),
                "status": appointment.status,
                "version": appointment.version,
                "starts_at": appointment.starts_at.isoformat(),
                "ends_at": appointment.ends_at.isoformat(),
            }
            now = datetime.now(UTC)
            await self.audit.record(
                event_type="APPOINTMENT_RESCHEDULED",
                summary="Appointment rescheduled by authorised actor.",
                correlation_id=correlation_id,
                actor_id=actor_id,
                entity_id=appointment.id,
                occurred_at=now,
            )
            await self.outbox.add(
                aggregate_id=appointment.id,
                event_type="APPOINTMENT_RESCHEDULED",
                payload=result | {"correlation_id": correlation_id},
                occurred_at=now,
            )
            await self.idempotency.put(idempotency_key, fingerprint, result)
            return result

    @staticmethod
    def _require_active(appointment: Appointment | None) -> None:
        if appointment is None:
            raise ValueError("APPOINTMENT_NOT_FOUND")
        if appointment.status != "CONFIRMED":
            raise ValueError("APPOINTMENT_NOT_ACTIVE")
