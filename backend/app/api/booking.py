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
    patient_id: UUID
    clinician_id: UUID
    appointment_type: str
    starts_at: datetime
    ends_at: datetime
    version: int
    expires_at: datetime
    rationale: str


class ApprovalRequest(BaseModel):
    patient_id: UUID
    proposal_version: int = Field(ge=1)


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
    return ProposalResponse(
        proposal_id=proposal.proposal_id,
        request_id=proposal.request_id,
        patient_id=payload.patient_id,
        clinician_id=proposal.clinician_id,
        appointment_type=proposal.appointment_type,
        starts_at=proposal.starts_at,
        ends_at=proposal.ends_at,
        version=proposal.version,
        expires_at=proposal.expires_at,
        rationale=proposal.rationale,
    )


@router.post("/proposals/{proposal_id}/approve", response_model=ApprovalResponse)
def approve_proposal(
    proposal_id: UUID,
    proposal: ProposalResponse,
    approval: ApprovalRequest,
    actor_id: UUID,
    idempotency_key: str = Header(min_length=8, max_length=200),
) -> ApprovalResponse:
    if proposal.proposal_id != proposal_id:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="PROPOSAL_MISMATCH")
    if approval.proposal_version != proposal.version:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="STALE_PROPOSAL")
    if approval.patient_id != proposal.patient_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="PATIENT_MISMATCH")

    domain_proposal = AppointmentProposal(
        proposal_id=proposal.proposal_id,
        request_id=proposal.request_id,
        clinician_id=proposal.clinician_id,
        appointment_type=proposal.appointment_type,
        starts_at=proposal.starts_at,
        ends_at=proposal.ends_at,
        version=proposal.version,
        expires_at=proposal.expires_at,
        rationale=proposal.rationale,
    )
    try:
        result = booking.approve_and_book(
            idempotency_key=idempotency_key,
            patient_id=approval.patient_id,
            proposal=domain_proposal,
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
