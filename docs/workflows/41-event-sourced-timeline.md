# Workflow Event Timeline

ClinicFlow keeps an append-oriented workflow event history alongside the current workflow state.

## Why keep both?

The current state answers “where is the workflow now?”

The event timeline answers “how did it get here?”

Keeping both makes operational debugging, audit review and customer support much easier than reconstructing history from mutable rows.

## Sequence

Each workflow event has a monotonic sequence number within its workflow.

Example:

1. REQUEST_RECEIVED
2. EXTRACTION_STARTED
3. EXTRACTION_COMPLETED
4. VALIDATION_PASSED
5. AVAILABILITY_SEARCHED
6. PROPOSAL_CREATED
7. APPROVAL_REQUESTED
8. APPROVED
9. BOOKED

The event timeline is not a full event-sourcing architecture. The appointment tables remain authoritative for current business state; the workflow timeline is the operational history.

## Concurrency note

The workflow event table enforces a unique workflow_id + sequence_number constraint. The production append repository must retry on sequence collisions rather than allowing duplicate timeline positions.
