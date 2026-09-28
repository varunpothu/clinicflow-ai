from datetime import UTC, datetime, timedelta
from uuid import uuid4

import pytest

from app.domain.lifecycle import AppointmentLifecycleError, cancel_appointment, reschedule_appointment
from app.domain.waitlist import WaitlistEngine, WaitlistEntry


def test_cancel_changes_status_and_increments_version() -> None:
    appointment = {"status": "CONFIRMED", "version": 2}
    result = cancel_appointment(appointment, actor_id=uuid4())
    assert result["status"] == "CANCELLED"
    assert result["version"] == 3


def test_cannot_reschedule_cancelled_appointment() -> None:
    with pytest.raises(AppointmentLifecycleError, match="APPOINTMENT_NOT_ACTIVE"):
        reschedule_appointment(
            {"status": "CANCELLED", "version": 1},
            new_starts_at=datetime.now(UTC) + timedelta(days=1),
            new_ends_at=datetime.now(UTC) + timedelta(days=1, minutes=30),
        )


def test_waitlist_match_is_deterministic() -> None:
    now = datetime.now(UTC)
    clinician = uuid4()
    first = WaitlistEntry(
        entry_id=uuid4(),
        patient_id=uuid4(),
        appointment_type="routine",
        preferred_clinician_id=clinician,
        earliest=now,
        latest=now + timedelta(days=2),
        created_at=now,
    )
    second = WaitlistEntry(
        entry_id=uuid4(),
        patient_id=uuid4(),
        appointment_type="routine",
        preferred_clinician_id=None,
        earliest=now,
        latest=now + timedelta(days=2),
        created_at=now + timedelta(minutes=1),
    )
    result = WaitlistEngine.match(
        [second, first],
        appointment_type="routine",
        clinician_id=clinician,
        starts_at=now + timedelta(hours=1),
    )
    assert result == first
