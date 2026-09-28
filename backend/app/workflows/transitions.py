from app.workflows.states import WorkflowState


ALLOWED_TRANSITIONS: dict[WorkflowState, frozenset[WorkflowState]] = {
    WorkflowState.RECEIVED: frozenset({WorkflowState.EXTRACTING}),
    WorkflowState.EXTRACTING: frozenset({WorkflowState.NEEDS_CLARIFICATION, WorkflowState.VALIDATING}),
    WorkflowState.NEEDS_CLARIFICATION: frozenset({WorkflowState.RECEIVED}),
    WorkflowState.VALIDATING: frozenset({WorkflowState.SEARCHING_AVAILABILITY}),
    WorkflowState.SEARCHING_AVAILABILITY: frozenset({WorkflowState.NO_AVAILABILITY, WorkflowState.PROPOSED}),
    WorkflowState.NO_AVAILABILITY: frozenset({WorkflowState.WAITING_FOR_STAFF}),
    WorkflowState.PROPOSED: frozenset({WorkflowState.WAITING_FOR_APPROVAL}),
    WorkflowState.WAITING_FOR_APPROVAL: frozenset({WorkflowState.APPROVED, WorkflowState.REJECTED, WorkflowState.EXPIRED}),
    WorkflowState.APPROVED: frozenset({WorkflowState.REVALIDATING}),
    WorkflowState.REVALIDATING: frozenset({WorkflowState.BOOKING, WorkflowState.CONFLICT}),
    WorkflowState.CONFLICT: frozenset({WorkflowState.PROPOSED}),
    WorkflowState.BOOKING: frozenset({WorkflowState.CONFIRMED, WorkflowState.BOOKING_RETRY, WorkflowState.FAILED}),
    WorkflowState.BOOKING_RETRY: frozenset({WorkflowState.BOOKING, WorkflowState.FAILED}),
    WorkflowState.CONFIRMED: frozenset({WorkflowState.CANCELLED, WorkflowState.RESCHEDULE_REQUESTED}),
    WorkflowState.RESCHEDULE_REQUESTED: frozenset({WorkflowState.SEARCHING_AVAILABILITY, WorkflowState.PROPOSED}),
    WorkflowState.CANCELLED: frozenset(),
    WorkflowState.REJECTED: frozenset(),
    WorkflowState.EXPIRED: frozenset(),
    WorkflowState.FAILED: frozenset(),
}


def can_transition(current: WorkflowState, target: WorkflowState) -> bool:
    return target in ALLOWED_TRANSITIONS[current]
