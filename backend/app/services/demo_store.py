from datetime import UTC, datetime
from uuid import UUID


class DemoStore:
    def __init__(self) -> None:
        self.blocked_slots: set[str] = set()
        self.appointments: dict[str, dict[str, object]] = {}

    def slot_is_available(self, clinician_id: UUID, starts_at: datetime) -> bool:
        key = f"{clinician_id}:{starts_at.astimezone(UTC).isoformat()}"
        return key not in self.blocked_slots

    def book(
        self,
        *,
        appointment_id: str,
        clinician_id: UUID,
        starts_at: datetime,
        ends_at: datetime,
        patient_id: UUID,
        appointment_type: str,
    ) -> dict[str, object]:
        key = f"{clinician_id}:{starts_at.astimezone(UTC).isoformat()}"
        if key in self.blocked_slots:
            raise ValueError("BOOKING_CONFLICT")
        self.blocked_slots.add(key)
        appointment: dict[str, object] = {
            "appointment_id": appointment_id,
            "patient_id": str(patient_id),
            "clinician_id": str(clinician_id),
            "appointment_type": appointment_type,
            "starts_at": starts_at.isoformat(),
            "ends_at": ends_at.isoformat(),
            "status": "CONFIRMED",
        }
        self.appointments[appointment_id] = appointment
        return appointment
