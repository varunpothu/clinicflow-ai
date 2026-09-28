from datetime import UTC, datetime
from uuid import UUID, uuid4

from app.domain.waitlist import WaitlistEngine, WaitlistEntry


class WaitlistService:
    def __init__(self) -> None:
        self.entries: list[WaitlistEntry] = []

    def add(
        self,
        *,
        patient_id: UUID,
        appointment_type: str,
        earliest: datetime,
        latest: datetime,
        preferred_clinician_id: UUID | None = None,
    ) -> WaitlistEntry:
        if earliest.tzinfo is None or latest.tzinfo is None:
            raise ValueError("TIMEZONE_REQUIRED")
        if latest <= earliest:
            raise ValueError("INVALID_WAITLIST_WINDOW")
        entry = WaitlistEntry(
            entry_id=uuid4(),
            patient_id=patient_id,
            appointment_type=appointment_type,
            preferred_clinician_id=preferred_clinician_id,
            earliest=earliest.astimezone(UTC),
            latest=latest.astimezone(UTC),
            created_at=datetime.now(UTC),
        )
        self.entries.append(entry)
        return entry

    def match(
        self,
        *,
        appointment_type: str,
        clinician_id: UUID,
        starts_at: datetime,
    ) -> WaitlistEntry | None:
        if starts_at.tzinfo is None:
            raise ValueError("TIMEZONE_REQUIRED")
        return WaitlistEngine.match(
            self.entries,
            appointment_type=appointment_type,
            clinician_id=clinician_id,
            starts_at=starts_at.astimezone(UTC),
        )
