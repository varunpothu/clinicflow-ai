from uuid import UUID

from fastapi import APIRouter, Depends, Header, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.correlation import get_correlation_id
from app.db.dependencies import get_session
from app.security.dependencies import require_demo_permission
from app.security.rbac import Permission
from app.security.auth import Principal
from app.services.persistent_approval import PersistentApprovalService

router = APIRouter(prefix="/persistent-booking", tags=["persistent-booking"])


class ApprovalCommand(BaseModel):
    proposal_version: int = Field(ge=1)


@router.post("/proposals/{proposal_id}/approve")
async def approve_persisted_proposal(
    proposal_id: UUID,
    command: ApprovalCommand,
    idempotency_key: str = Header(min_length=8, max_length=200),
    principal: Principal = Depends(require_demo_permission(Permission.APPROVE_PROPOSAL)),
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
        status_code = status.HTTP_409_CONFLICT
        if code in {"PROPOSAL_NOT_FOUND"}:
            status_code = status.HTTP_404_NOT_FOUND
        if code in {"FORBIDDEN"}:
            status_code = status.HTTP_403_FORBIDDEN
        raise HTTPException(status_code=status_code, detail=code) from exc
