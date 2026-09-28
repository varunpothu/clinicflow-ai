from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class ExtractedIntent:
    appointment_type: str
    preferred_time_text: str | None
    clarification_required: bool
    rationale: str


class AIProvider(Protocol):
    def extract_intent(self, text: str) -> ExtractedIntent: ...


class MockAIProvider:
    """Deterministic local adapter; no network call and no model authority."""

    def extract_intent(self, text: str) -> ExtractedIntent:
        normalized = text.strip()
        return ExtractedIntent(
            appointment_type="routine_consultation",
            preferred_time_text=normalized or None,
            clarification_required=not bool(normalized),
            rationale="Local deterministic fixture used until the Bedrock adapter is configured.",
        )
