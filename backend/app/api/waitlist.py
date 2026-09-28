from datetime import datetime
from uuid import UUID

from fastapi import APIRouter
from pydantic import BaseModel

from app.services.waitlist import WaitlistService

router = APIRouter(prefix="/waitlist", tags=["waitlist"])
service = WaitlistService()


class WaitlistCreate(BaseModel):
    patient_id: UUID
    appointment_type: str
    earliest: datetime
    latest: datetime
    preferred_clinician_id: UUID | None = None


@router.post("")
def add_to_waitlist(payload: WaitlistCreate) -> dict[str, object]:
    entry = service.add(**payload.model_dump())
    return {"entry_id": str(entry.entry_id), "status": "ACTIVE"}


@router.get("/match")
def match_waitlist(
    appointment_type: str,
    clinician_id: UUID,
    starts_at: datetime,
) -> dict[str, object]:
    entry = service.match(
        appointment_type=appointment_type,
        clinician_id=clinician_id,
        starts_at=starts_at,
    )
    if entry is None:
        return {"matched": False}
    return {"matched": True, "entry_id": str(entry.entry_id), "patient_id": str(entry.patient_id)}
