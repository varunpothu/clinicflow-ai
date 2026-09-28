from datetime import UTC, datetime
from uuid import UUID

from app.domain.lifecycle import AppointmentLifecycleError, cancel_appointment, reschedule_appointment
from app.services.demo_store import DemoStore


class AppointmentLifecycleService:
    def __init__(self, store: DemoStore) -> None:
        self.store = store

    def cancel(self, appointment_id: str, actor_id: UUID) -> dict[str, object]:
        appointment = self.store.appointments.get(appointment_id)
        if appointment is None:
            raise AppointmentLifecycleError("APPOINTMENT_NOT_FOUND")

        old_key = f'{appointment["clinician_id"]}:{appointment["starts_at"]}'
        updated = cancel_appointment(appointment, actor_id=actor_id)
        appointment.clear()
        appointment.update(updated)
        self.store.blocked_slots.discard(old_key)
        return appointment

    def reschedule(
        self,
        appointment_id: str,
        *,
        new_starts_at: datetime,
        new_ends_at: datetime,
    ) -> dict[str, object]:
        appointment = self.store.appointments.get(appointment_id)
        if appointment is None:
            raise AppointmentLifecycleError("APPOINTMENT_NOT_FOUND")

        clinician_id = UUID(str(appointment["clinician_id"]))
        old_start = datetime.fromisoformat(str(appointment["starts_at"])).astimezone(UTC)
        old_key = f"{clinician_id}:{old_start.isoformat()}"
        new_key = f"{clinician_id}:{new_starts_at.astimezone(UTC).isoformat()}"

        if new_key != old_key and new_key in self.store.blocked_slots:
            raise AppointmentLifecycleError("BOOKING_CONFLICT")

        updated = reschedule_appointment(
            appointment,
            new_starts_at=new_starts_at.astimezone(UTC),
            new_ends_at=new_ends_at.astimezone(UTC),
        )
        appointment.clear()
        appointment.update(updated)
        self.store.blocked_slots.discard(old_key)
        self.store.blocked_slots.add(new_key)
        return appointment
