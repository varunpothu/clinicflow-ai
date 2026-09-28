from datetime import UTC, datetime, timedelta
from uuid import uuid4

import pytest

from app.services.waitlist import WaitlistService


def test_waitlist_rejects_invalid_window() -> None:
    service = WaitlistService()
    start = datetime.now(UTC)
    with pytest.raises(ValueError, match="INVALID_WAITLIST_WINDOW"):
        service.add(
            patient_id=uuid4(),
            appointment_type="routine",
            earliest=start,
            latest=start,
        )


def test_waitlist_returns_earliest_created_eligible_entry() -> None:
    service = WaitlistService()
    start = datetime.now(UTC) + timedelta(hours=2)
    patient = uuid4()
    first = service.add(
        patient_id=patient,
        appointment_type="routine",
        earliest=start - timedelta(hours=1),
        latest=start + timedelta(hours=1),
    )
    service.add(
        patient_id=uuid4(),
        appointment_type="routine",
        earliest=start - timedelta(hours=1),
        latest=start + timedelta(hours=1),
    )
    matched = service.match(
        appointment_type="routine",
        clinician_id=uuid4(),
        starts_at=start,
    )
    assert matched == first
