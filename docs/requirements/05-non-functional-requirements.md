
# Non-Functional Requirements

## Reliability

Transient dependencies must have bounded retries, exponential backoff and dead-letter handling. Durable state must not depend on in-memory process state.

## Consistency

The booking write is the source of truth. Availability shown before approval is advisory and is never treated as a reservation.

## Performance

Target interactive API operations at low-second response times under normal load. Asynchronous work should not block user-facing requests unless the user explicitly needs the result.

## Security

Use least privilege, role-based authorisation, encrypted secrets, secure transport, input validation, auditability, and data minimisation.

## Observability

Every request carries a correlation ID. Material workflow transitions emit structured events. Metrics cover latency, volume, errors, retries, queue depth and approval SLA.

## Maintainability

Business rules remain deterministic and testable without requiring an LLM or AWS account.

## Portability

Local development must work with a mock AI provider and a local relational database. AWS integrations are adapters, not hard-coded domain dependencies.
