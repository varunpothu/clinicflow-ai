from datetime import UTC, datetime, timedelta
from uuid import uuid4

from app.domain.appointment_request import AppointmentRequest
from app.domain.validation import validate_request
from app.workflows.states import WorkflowState
from app.workflows.transitions import can_transition


def test_valid_request() -> None:
    start = datetime.now(UTC) + timedelta(days=1)
    request = AppointmentRequest(
        request_id=uuid4(), patient_id=uuid4(), appointment_type="routine", preferred_start=start
    )
    assert validate_request(request).valid


def test_invalid_time_range() -> None:
    start = datetime.now(UTC) + timedelta(days=1)
    request = AppointmentRequest(
        request_id=uuid4(), patient_id=uuid4(), appointment_type="routine",
        preferred_start=start, preferred_end=start - timedelta(minutes=1)
    )
    result = validate_request(request)
    assert not result.valid
    assert "preferred_end must be after preferred_start" in result.errors


def test_workflow_transition_is_explicit() -> None:
    assert can_transition(WorkflowState.RECEIVED, WorkflowState.EXTRACTING)
    assert not can_transition(WorkflowState.RECEIVED, WorkflowState.CONFIRMED)
