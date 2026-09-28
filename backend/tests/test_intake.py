from uuid import uuid4

from app.core.config import Settings
from app.workflows.intake import AppointmentIntakeWorkflow
from app.workflows.states import WorkflowState


def test_natural_language_enters_ai_extraction() -> None:
    workflow = AppointmentIntakeWorkflow(Settings(ai_provider="mock"))
    result = workflow.start(
        patient_id=uuid4(),
        appointment_type="routine",
        natural_language="Tuesday after 4pm",
    )
    assert result.ai_intent is not None
    assert result.state == WorkflowState.VALIDATING


def test_empty_request_is_clarification() -> None:
    workflow = AppointmentIntakeWorkflow(Settings(ai_provider="mock"))
    result = workflow.start(
        patient_id=uuid4(),
        appointment_type="routine",
        natural_language=None,
    )
    assert result.state == WorkflowState.NEEDS_CLARIFICATION
    assert result.validation.valid is False
