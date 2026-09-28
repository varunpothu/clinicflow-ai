from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class AppointmentRequest(BaseModel):
    request_id: UUID
    patient_id: UUID
    appointment_type: str = Field(min_length=1, max_length=100)
    preferred_start: datetime | None = None
    preferred_end: datetime | None = None
    preferred_clinician_id: UUID | None = None
    natural_language: str | None = Field(default=None, max_length=4000)
