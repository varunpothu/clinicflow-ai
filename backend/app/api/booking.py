from datetime import UTC, datetime, timedelta
from uuid import UUID

from fastapi import APIRouter, Header, HTTPException, status
from pydantic import BaseModel, Field

from app.domain.availability import AvailabilityEngine
from app.domain.proposal import AppointmentProposal
from app.services.booking import BookingConflict, BookingService

router = APIRouter(prefix="/booking", tags=["booking"])

availability = AvailabilityEngine()
booking = BookingService()


class AvailabilityResponse(BaseModel):
    clinician_id: UUID
    starts_at: datetime
    ends_at: datetime


class ProposalCreate(BaseModel):
    request_id: UUID
    clinician_id: UUID
    patient_id: UUID
    appointment_type: str = Field(min_length=1, max_length=100)
    starts_at: datetime
    duration_minutes: int = Field(default=30, ge=15, le=180)


class ProposalResponse(BaseModel):
    proposal_id: UUID
    request_id: UUID
    clinician_id: UUID
    starts_at: datetime
    ends_at: datetime
    version: int
    expires_at: datetime
    rationale: str


class ApprovalResponse(BaseModel):
    appointment: dict[str, object]
    approved_by: UUID
    proposal_id: UUID
    proposal_version: int


@router.get("/availability", response_model=list[AvailabilityResponse])
def get_availability(clinician_id: UUID, from_date: datetime) -> list[AvailabilityResponse]:
    return [
        AvailabilityResponse(
            clinician_id=slot.clinician_id,
            starts_at=slot.starts_at,
            ends_at=slot.ends_at,
        )
        for slot in availability.generate(clinician_id, from_date, days=7)
    ]


@router.post("/proposals", response_model=ProposalResponse)
def create_proposal(payload: ProposalCreate) -> ProposalResponse:
    ends_at = payload.starts_at + timedelta(minutes=payload.duration_minutes)
    proposal = AppointmentProposal.create(
        request_id=payload.request_id,
        clinician_id=payload.clinician_id,
        appointment_type=payload.appointment_type,
        starts_at=payload.starts_at,
        ends_at=ends_at,
        version=1,
        expires_at=datetime.now(UTC) + timedelta(minutes=10),
        rationale="Candidate slot selected by deterministic availability rules.",
    )
    return ProposalResponse(**proposal.__dict__)


@router.post("/proposals/{proposal_id}/approve", response_model=ApprovalResponse)
def approve_proposal(
    proposal_id: UUID,
    payload: ProposalResponse,
    actor_id: UUID,
    idempotency_key: str = Header(min_length=8, max_length=200),
) -> ApprovalResponse:
    if payload.proposal_id != proposal_id:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="PROPOSAL_MISMATCH")
    proposal = AppointmentProposal(
        proposal_id=payload.proposal_id,
        request_id=payload.request_id,
        clinician_id=payload.clinician_id,
        appointment_type="routine_consultation",
        starts_at=payload.starts_at,
        ends_at=payload.ends_at,
        version=payload.version,
        expires_at=payload.expires_at,
        rationale=payload.rationale,
    )
    try:
        result = booking.approve_and_book(
            idempotency_key=idempotency_key,
            patient_id=payload.request_id,
            proposal=proposal,
            actor_id=actor_id,
        )
    except BookingConflict as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    return ApprovalResponse(
        appointment=result["appointment"],
        approved_by=actor_id,
        proposal_id=proposal_id,
        proposal_version=proposal.version,
    )
