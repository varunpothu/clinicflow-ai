from datetime import UTC, datetime, timedelta
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, Header, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.correlation import get_correlation_id
from app.db.dependencies import get_session
from app.models.approval import Approval
from app.repositories.approvals import ApprovalRepository
from app.repositories.proposals import ProposalRepository
from app.security.auth import Principal
from app.security.dependencies import require_demo_permission
from app.security.rbac import Permission
from app.services.persistent_approval import PersistentApprovalService

router = APIRouter(prefix="/persistent-booking", tags=["persistent-booking"])


class ProposalCreateCommand(BaseModel):
    request_id: UUID
    patient_id: UUID
    clinician_id: UUID
    appointment_type: str = Field(min_length=1, max_length=100)
    starts_at: datetime
    duration_minutes: int = Field(default=30, ge=15, le=180)


class ProposalResponse(BaseModel):
    proposal_id: UUID
    approval_id: UUID
    proposal_version: int
    status: str
    expires_at: datetime


class ApprovalCommand(BaseModel):
    proposal_version: int = Field(ge=1)


@router.post("/proposals", response_model=ProposalResponse, status_code=status.HTTP_201_CREATED)
async def create_persisted_proposal(
    command: ProposalCreateCommand,
    principal: Principal = Depends(
        require_demo_permission(Permission.VIEW_APPROVAL_QUEUE)
    ),
    session: AsyncSession = Depends(get_session),
) -> ProposalResponse:
    del principal
    expires_at = datetime.now(UTC) + timedelta(minutes=10)
    proposal_repository = ProposalRepository(session)
    approval_repository = ApprovalRepository(session)

    async with session.begin():
        proposal = await proposal_repository.create(
            proposal_id=uuid4(),
            request_id=command.request_id,
            patient_id=command.patient_id,
            clinician_id=command.clinician_id,
            appointment_type=command.appointment_type,
            starts_at=command.starts_at,
            ends_at=command.starts_at + timedelta(minutes=command.duration_minutes),
            expires_at=expires_at,
            rationale="Candidate slot created by deterministic scheduling rules.",
        )
        approval = await approval_repository.create(proposal)

    return ProposalResponse(
        proposal_id=UUID(proposal.id),
        approval_id=approval.id,
        proposal_version=proposal.version,
        status=proposal.status,
        expires_at=proposal.expires_at,
    )


@router.get("/approvals")
async def list_persisted_approvals(
    principal: Principal = Depends(
        require_demo_permission(Permission.VIEW_APPROVAL_QUEUE)
    ),
    session: AsyncSession = Depends(get_session),
) -> list[dict[str, object]]:
    del principal
    result = await session.execute(
        select(Approval).where(Approval.status == "PENDING").order_by(Approval.expires_at)
    )
    return [
        {
            "approval_id": approval.id,
            "proposal_id": approval.proposal_id,
            "proposal_version": approval.proposal_version,
            "status": approval.status,
            "expires_at": approval.expires_at,
        }
        for approval in result.scalars().all()
    ]


@router.post("/proposals/{proposal_id}/approve")
async def approve_persisted_proposal(
    proposal_id: UUID,
    command: ApprovalCommand,
    idempotency_key: str = Header(min_length=8, max_length=200),
    principal: Principal = Depends(
        require_demo_permission(Permission.APPROVE_PROPOSAL)
    ),
    session: AsyncSession = Depends(get_session),
) -> dict[str, object]:
    service = PersistentApprovalService(session)
    try:
        return await service.approve(
            proposal_id=proposal_id,
            proposal_version=command.proposal_version,
            approver_id=principal.subject_id,
            idempotency_key=idempotency_key,
            correlation_id=get_correlation_id(),
        )
    except ValueError as exc:
        code = str(exc)
        error_status = status.HTTP_409_CONFLICT
        if code == "PROPOSAL_NOT_FOUND":
            error_status = status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code=error_status, detail=code) from exc
