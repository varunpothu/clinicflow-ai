
# API Design

## Resource model

POST /api/v1/appointment-requests
GET /api/v1/appointment-requests/{request_id}
GET /api/v1/availability
GET /api/v1/proposals/{proposal_id}
GET /api/v1/approvals
POST /api/v1/approvals/{approval_id}/approve
POST /api/v1/approvals/{approval_id}/reject
POST /api/v1/approvals/{approval_id}/modify
GET /api/v1/appointments/{appointment_id}
POST /api/v1/appointments/{appointment_id}/cancel
POST /api/v1/appointments/{appointment_id}/reschedule
GET /api/v1/workflows/{workflow_id}
GET /api/v1/workflows/{workflow_id}/events

## API rules

- Version the public contract under /api/v1.
- Use idempotency keys on commands that can create side effects.
- Accept and return ISO 8601 timestamps.
- Validate all payloads at the boundary.
- Return stable machine-readable error codes.
- Emit correlation IDs in responses.

## Error envelope

{
  "type": "https://clinicflow.example/errors/booking-conflict",
  "title": "Booking conflict",
  "status": 409,
  "code": "BOOKING_CONFLICT",
  "detail": "The proposed slot is no longer available.",
  "correlation_id": "..."
}

The example is illustrative. Production error details must avoid leaking sensitive information.
