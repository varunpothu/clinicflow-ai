
# Functional Requirements

| ID | Requirement | Priority |
|---|---|---|
| FR-001 | Create appointment request from structured or natural-language input | Must |
| FR-002 | Extract scheduling intent into a versioned schema | Must |
| FR-003 | Validate extracted intent deterministically | Must |
| FR-004 | Search available slots using clinic rules | Must |
| FR-005 | Generate a proposal with validity window and rationale | Must |
| FR-006 | Route proposal to authorised human approver | Must |
| FR-007 | Approve, reject or modify proposal | Must |
| FR-008 | Revalidate slot at booking time | Must |
| FR-009 | Prevent duplicate booking from repeated approval | Must |
| FR-010 | Record audit event for material state changes | Must |
| FR-011 | Retry transient asynchronous failures and expose DLQ exceptions | Should |
| FR-012 | Support cancellation and rescheduling | Should |
| FR-013 | Support waitlist matching | Later |
| FR-014 | Support multi-location scheduling | Later |
| FR-015 | Provide analytics for workflow and operational health | Should |
| FR-016 | Provide replayable synthetic scenarios for demonstrations | Should |

## Business rules

1. A slot can be booked only when currently available.
2. A proposal is not a booking.
3. Human approval is mandatory for controlled bookings.
4. Patient text is untrusted input.
5. AI output must pass schema and business-rule validation.
6. Booking requests must be idempotent.
7. All timestamps are stored in UTC; clinic display uses the configured IANA timezone.
