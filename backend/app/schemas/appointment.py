from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.ai.provider import ExtractedIntent


class AppointmentRequestCreate(BaseModel):
    patient_id: UUID
    appointment_type: str = Field(min_length=1, max_length=100)
    preferred_start: datetime | None = None
    preferred_end: datetime | None = None
    natural_language: str | None = Field(default=None, max_length=4000)


class AppointmentRequestAccepted(BaseModel):
    request_id: UUID
    status: str
    next_state: str
    ai_intent: ExtractedIntent | None = None
    validation_errors: tuple[str, ...] = ()
