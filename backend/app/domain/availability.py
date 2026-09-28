from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from uuid import UUID

from zoneinfo import ZoneInfo


@dataclass(frozen=True)
class Slot:
    clinician_id: UUID
    starts_at: datetime
    ends_at: datetime

    @property
    def key(self) -> str:
        return f"{self.clinician_id}:{self.starts_at.isoformat()}"


@dataclass(frozen=True)
class AvailabilityPolicy:
    clinic_timezone: str = "Europe/London"
    start_hour: int = 9
    end_hour: int = 17
    slot_minutes: int = 30


class AvailabilityEngine:
    def __init__(self, policy: AvailabilityPolicy | None = None) -> None:
        self.policy = policy or AvailabilityPolicy()

    def generate(
        self,
        clinician_id: UUID,
        start_date: datetime,
        days: int,
        blocked_slots: set[str] | None = None,
    ) -> list[Slot]:
        blocked = blocked_slots or set()
        zone = ZoneInfo(self.policy.clinic_timezone)
        local_start = start_date.astimezone(zone).replace(
            hour=self.policy.start_hour, minute=0, second=0, microsecond=0
        )
        slots: list[Slot] = []
        for day_offset in range(days):
            day = local_start + timedelta(days=day_offset)
            if day.weekday() >= 5:
                continue
            cursor = day
            day_end = day.replace(hour=self.policy.end_hour)
            while cursor + timedelta(minutes=self.policy.slot_minutes) <= day_end:
                start_utc = cursor.astimezone(UTC)
                end_utc = (cursor + timedelta(minutes=self.policy.slot_minutes)).astimezone(UTC)
                slot = Slot(clinician_id, start_utc, end_utc)
                if slot.key not in blocked:
                    slots.append(slot)
                cursor += timedelta(minutes=self.policy.slot_minutes)
        return slots
