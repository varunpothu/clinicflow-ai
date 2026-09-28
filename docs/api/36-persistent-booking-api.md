# Persistent Booking API

## Staff proposal creation

POST /api/v1/persistent-booking/proposals

Creates a server-owned proposal and a PENDING approval record in one transaction.

## Approval queue

GET /api/v1/persistent-booking/approvals

Requires VIEW_APPROVAL_QUEUE.

## Approval execution

POST /api/v1/persistent-booking/proposals/{proposal_id}/approve

Requires APPROVE_PROPOSAL and an idempotency key.

The body contains only the proposal version. Appointment details are loaded from the server-owned proposal record.

## Example flow

Patient request -> proposal creation -> approval queue -> human approval -> final booking transaction -> audit + outbox.
