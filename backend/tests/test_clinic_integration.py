from datetime import UTC, datetime, timedelta
from uuid import uuid4

import pytest

from app.integrations.clinic_system import MockClinicSchedulingSystem


def test_mock_clinic_system_enforces_external_slot_conflict() -> None:
    system = MockClinicSchedulingSystem()
    clinician = uuid4()
    start = datetime.now(UTC) + timedelta(days=1)
    end = start + timedelta(minutes=30)

    first = system.create_appointment(
        patient_reference="patient-001",
        clinician_id=clinician,
        starts_at=start,
        ends_at=end,
    )
    assert first.external_id == "NS-00001"
    assert not system.is_available(clinician, start)

    with pytest.raises(ValueError, match="EXTERNAL_BOOKING_CONFLICT"):
        system.create_appointment(
            patient_reference="patient-002",
            clinician_id=clinician,
            starts_at=start,
            ends_at=end,
        )
