from datetime import UTC, datetime
from uuid import UUID


class AppointmentLifecycleError(ValueError):
    pass


def _next_version(appointment: dict[str, object]) -> int:
    version = appointment.get("version", 1)
    if not isinstance(version, int):
        raise AppointmentLifecycleError("INVALID_VERSION")
    return version + 1


def cancel_appointment(appointment: dict[str, object], *, actor_id: UUID) -> dict[str, object]:
    if appointment.get("status") != "CONFIRMED":
        raise AppointmentLifecycleError("APPOINTMENT_NOT_ACTIVE")

    updated = dict(appointment)
    updated["status"] = "CANCELLED"
    updated["version"] = _next_version(appointment)
    updated["cancelled_by"] = str(actor_id)
    updated["cancelled_at"] = datetime.now(UTC).isoformat()
    return updated


def reschedule_appointment(
    appointment: dict[str, object],
    *,
    new_starts_at: datetime,
    new_ends_at: datetime,
) -> dict[str, object]:
    if appointment.get("status") != "CONFIRMED":
        raise AppointmentLifecycleError("APPOINTMENT_NOT_ACTIVE")
    if new_starts_at.tzinfo is None or new_ends_at.tzinfo is None:
        raise AppointmentLifecycleError("TIMEZONE_REQUIRED")
    if new_ends_at <= new_starts_at:
        raise AppointmentLifecycleError("INVALID_RESCHEDULE_RANGE")

    updated = dict(appointment)
    updated["starts_at"] = new_starts_at.astimezone(UTC).isoformat()
    updated["ends_at"] = new_ends_at.astimezone(UTC).isoformat()
    updated["version"] = _next_version(appointment)
    updated["status"] = "CONFIRMED"
    return updated
