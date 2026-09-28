from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True)
class WaitlistEntry:
    entry_id: UUID
    patient_id: UUID
    appointment_type: str
    preferred_clinician_id: UUID | None
    earliest: datetime
    latest: datetime
    created_at: datetime


class WaitlistEngine:
    @staticmethod
    def match(
        entries: list[WaitlistEntry],
        *,
        appointment_type: str,
        clinician_id: UUID,
        starts_at: datetime,
    ) -> WaitlistEntry | None:
        eligible = [
            entry
            for entry in entries
            if entry.appointment_type == appointment_type
            and (entry.preferred_clinician_id is None or entry.preferred_clinician_id == clinician_id)
            and entry.earliest <= starts_at <= entry.latest
        ]
        if not eligible:
            return None
        return min(eligible, key=lambda entry: (entry.created_at, entry.entry_id))
