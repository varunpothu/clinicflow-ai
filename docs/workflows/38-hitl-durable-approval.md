# Durable Human-in-the-Loop Approval

## Workflow

Patient request -> AI extraction -> deterministic validation -> availability -> proposal -> durable approval wait -> final revalidation -> booking -> notification.

## Approval lifecycle

PENDING -> APPROVED
PENDING -> REJECTED
PENDING -> EXPIRED

The approval record keeps the proposal version. A stale callback cannot approve a newer or older proposal version.

## Operational benefit

A staff member can take an action hours after a request without relying on application memory. Workflow state survives container restarts and deployment events.

## Failure scenarios

- staff never responds: expiry moves to exception handling
- slot is taken before approval: revalidation creates a new proposal
- callback is duplicated: approval/idempotency rules make the operation safe
- workflow times out: explicit terminal state and exception
