from datetime import date, time
from typing import Literal

from pydantic import BaseModel, Field


class AppointmentIntent(BaseModel):
    """Strict, model-facing contract. It contains no executable authority."""

    intent: Literal["BOOK_APPOINTMENT", "CANCEL_APPOINTMENT", "RESCHEDULE_APPOINTMENT", "UNKNOWN"]
    appointment_type: str | None = Field(default=None, min_length=1, max_length=100)
    preferred_date: date | None = None
    preferred_date_end: date | None = None
    preferred_after: time | None = None
    preferred_before: time | None = None
    clinician_preference: str | None = Field(default=None, max_length=100)
    clarification_required: bool
    clarification_question: str | None = Field(default=None, max_length=500)
    rationale: str = Field(min_length=1, max_length=1000)


class AIExtractionResult(BaseModel):
    intent: AppointmentIntent
    provider: str
    model: str
    prompt_version: str
    latency_ms: int