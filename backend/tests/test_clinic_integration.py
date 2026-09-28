from datetime import UTC, datetime, timedelta
from uuid import uuid4

import pytest

from app.integrations.clinic_system import ExternalBookingConflict, MockClinicSchedulingSystem

def test_external_scheduler_is_idempotent() -> None:
    system = MockClinicSchedulingSystem()
    now = datetime.now(UTC)
    key = 'external-001'
    first = system.create_appointment(patient_reference='patient-001', clinician_id=uuid4(), starts_at=now, ends_at=now + timedelta(minutes=30), idempotency_key=key)
    second = system.create_appointment(patient_reference='patient-001', clinician_id=first.clinician_id, starts_at=now, ends_at=now + timedelta(minutes=30), idempotency_key=key)
    assert second.external_id == first.external_id

def test_external_scheduler_rejects_competing_slot() -> None:
    system = MockClinicSchedulingSystem()
    now = datetime.now(UTC)
    clinician = uuid4()
    system.create_appointment(patient_reference='patient-001', clinician_id=clinician, starts_at=now, ends_at=now + timedelta(minutes=30), idempotency_key='external-002')
    with pytest.raises(ExternalBookingConflict, match='EXTERNAL_BOOKING_CONFLICT'):
        system.create_appointment(patient_reference='patient-002', clinician_id=clinician, starts_at=now, ends_at=now + timedelta(minutes=30), idempotency_key='external-003')