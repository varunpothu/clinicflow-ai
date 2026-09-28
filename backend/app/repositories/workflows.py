from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.workflow_event import WorkflowEvent


class WorkflowEventRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def append(
        self,
        *,
        workflow_id: UUID,
        event_type: str,
        state: str,
        occurred_at: datetime,
        payload: str | None = None,
    ) -> WorkflowEvent:
        result = await self.session.execute(
            select(func.max(WorkflowEvent.sequence_number)).where(
                WorkflowEvent.workflow_id == str(workflow_id)
            )
        )
        last_sequence = result.scalar_one_or_none() or 0
        event = WorkflowEvent(
            id=str(uuid4()),
            workflow_id=str(workflow_id),
            sequence_number=last_sequence + 1,
            event_type=event_type,
            state=state,
            payload=payload,
            occurred_at=occurred_at,
        )
        self.session.add(event)
        await self.session.flush()
        return event

    async def list_for_workflow(self, workflow_id: UUID) -> list[WorkflowEvent]:
        result = await self.session.execute(
            select(WorkflowEvent)
            .where(WorkflowEvent.workflow_id == str(workflow_id))
            .order_by(WorkflowEvent.sequence_number.asc())
        )
        return list(result.scalars().all())
