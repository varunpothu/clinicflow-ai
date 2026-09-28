# Booking Engine Alternatives

## Option A — Direct database booking from the AI agent

**Rejected.**

Advantages:
- Small amount of code.
- Fast prototype.

Risks:
- AI becomes an authority for side effects.
- Harder to constrain and audit.
- Prompt injection has a larger blast radius.
- Retry semantics can create duplicates.

## Option B — AI agent + deterministic booking service

**Chosen.**

AI produces structured intent or a proposal. The deterministic booking service owns validation, availability, idempotency and the final write.

Advantages:
- Clear authority boundary.
- Easier testing.
- Provider-independent AI layer.
- Safer failure handling.
- Good FDE story because integration boundaries are explicit.

## Option C — Fully event-driven booking

Possible later for high-volume deployments.

Advantages:
- Loose coupling.
- Strong asynchronous scalability.

Trade-off:
- More operational complexity.
- More eventual-consistency concerns.
- Harder local debugging.

ClinicFlow uses a hybrid: synchronous command handling for the booking decision, then transactional outbox + asynchronous events for notifications and analytics.
