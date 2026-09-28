import json
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.factory import build_ai_provider
from app.core.config import Settings
from app.repositories.appointment_requests import AppointmentRequestRepository
from app.repositories.idempotency import PersistentIdempotencyRepository


class PersistentIntakeService:
    def __init__(self, session: AsyncSession, settings: Settings) -> None:
        self.session = session
        self.settings = settings
        self.requests = AppointmentRequestRepository(session)
        self.idempotency = PersistentIdempotencyRepository(session)

    async def create(
        self,
        *,
        patient_id: UUID,
        appointment_type: str,
        natural_language: str | None,
        idempotency_key: str,
    ) -> dict[str, object]:
        fingerprint = (
            f"request:{patient_id}:{appointment_type}:"
            f"{(natural_language or '').strip()}"
        )

        async with self.session.begin():
            existing = await self.idempotency.get(idempotency_key)
            if existing is not None:
                if existing.fingerprint != fingerprint:
                    raise ValueError("IDEMPOTENCY_KEY_REUSE")
                value = json.loads(existing.result_json)
                if isinstance(value, dict):
                    return value
                raise ValueError("IDEMPOTENCY_RECORD_INVALID")

            from app.domain.appointment_request import AppointmentRequest as DomainRequest
            from app.workflows.states import WorkflowState
            from app.domain.validation import validate_request

            request_id = __import__("uuid").uuid4()
            domain_request = DomainRequest(
                request_id=request_id,
                patient_id=patient_id,
                appointment_type=appointment_type,
                natural_language=natural_language,
            )

            validation = validate_request(domain_request)
            state = WorkflowState.VALIDATING.value
            ai_result = None
            if natural_language:
                ai_result = build_ai_provider(self.settings).extract_intent(natural_language)
                if ai_result.clarification_required:
                    state = WorkflowState.NEEDS_CLARIFICATION.value

            if not validation.valid:
                state = WorkflowState.NEEDS_CLARIFICATION.value

            await self.requests.create(
                request_id=request_id,
                patient_id=patient_id,
                appointment_type=appointment_type,
                natural_language=natural_language,
                status=state,
            )

            result: dict[str, object] = {
                "request_id": str(request_id),
                "status": "accepted",
                "next_state": state,
                "ai_intent": (
                    {
                        "appointment_type": ai_result.appointment_type,
                        "preferred_time_text": ai_result.preferred_time_text,
                        "clarification_required": ai_result.clarification_required,
                        "clarification_question": ai_result.clarification_question,
                        "rationale": ai_result.rationale,
                    }
                    if ai_result
                    else None
                ),
                "validation_errors": list(validation.errors),
            }
            await self.idempotency.put(idempotency_key, fingerprint, result)
            return result
