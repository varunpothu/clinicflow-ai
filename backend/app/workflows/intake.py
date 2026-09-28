from dataclasses import dataclass
from uuid import UUID, uuid4

from app.ai.factory import build_ai_provider
from app.ai.provider import ExtractedIntent
from app.core.config import Settings
from app.domain.appointment_request import AppointmentRequest
from app.domain.validation import ValidationResult, validate_request
from app.workflows.states import WorkflowState


@dataclass(frozen=True)
class IntakeResult:
    request: AppointmentRequest
    ai_intent: ExtractedIntent | None
    validation: ValidationResult
    state: WorkflowState


class AppointmentIntakeWorkflow:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.ai = build_ai_provider(settings)

    def start(
        self,
        *,
        patient_id: UUID,
        appointment_type: str,
        natural_language: str | None,
    ) -> IntakeResult:
        request = AppointmentRequest(
            request_id=uuid4(),
            patient_id=patient_id,
            appointment_type=appointment_type,
            natural_language=natural_language,
        )

        ai_intent: ExtractedIntent | None = None
        state = WorkflowState.VALIDATING
        if natural_language:
            ai_intent = self.ai.extract_intent(natural_language)
            if ai_intent.clarification_required:
                state = WorkflowState.NEEDS_CLARIFICATION

        validation = validate_request(request)
        if not validation.valid:
            state = WorkflowState.NEEDS_CLARIFICATION

        return IntakeResult(
            request=request,
            ai_intent=ai_intent,
            validation=validation,
            state=state,
        )
