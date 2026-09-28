
# Observability

## Golden signals

Latency, traffic, errors and saturation are tracked for API, workflow, queue and external integrations.

## Business metrics

- requests created
- requests needing clarification
- proposals generated
- approval age
- approvals by outcome
- bookings confirmed
- booking conflicts
- cancellations
- reschedules
- notification failures
- workflow retries
- DLQ depth

## AI metrics

- model provider
- model version
- prompt version
- structured-output validity
- extraction confidence where applicable
- latency
- token usage
- provider error rate
- fallback rate

Sensitive prompt contents are not written into ordinary logs.

## Correlation

Every inbound request gets a correlation ID. Workflow events, database audit records and asynchronous messages carry the correlation ID or an immutable workflow ID.

## Alert examples

- booking conflict rate exceeds baseline
- queue age breaches SLA
- DLQ is non-empty for longer than the operational threshold
- AI schema invalid rate increases
- external notification provider errors spike
