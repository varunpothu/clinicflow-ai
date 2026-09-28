from datetime import datetime
from uuid import UUID


class AppointmentLifecycleError(ValueError):
    pass


def cancel_appointment(appointment: dict[str, object], *, actor_id: UUID) -> dict[str, object]:
    status = appointment.get("status")
    if status != "CONFIRMED":
        raise AppointmentLifecycleError("APPOINTMENT_NOT_ACTIVE")

    updated = dict(appointment)
    updated["status"] = "CANCELLED"
    updated["version"] = int(updated.get("version", 1)) + 1
    updated["cancelled_by"] = str(actor_id)
    updated["cancelled_at"] = datetime.utcnow().isoformat()
    return updated


def reschedule_appointment(
    appointment: dict[str, object],
    *,
    new_starts_at: datetime,
    new_ends_at: datetime,
) -> dict[str, object]:
    if appointment.get("status") != "CONFIRMED":
        raise AppointmentLifecycleError("APPOINTMENT_NOT_ACTIVE")
    if new_ends_at <= new_starts_at:
        raise AppointmentLifecycleError("INVALID_RESCHEDULE_RANGE")

    updated = dict(appointment)
    updated["starts_at"] = new_starts_at.isoformat()
    updated["ends_at"] = new_ends_at.isoformat()
    updated["version"] = int(updated.get("version", 1)) + 1
    updated["status"] = "CONFIRMED"
    return updated
