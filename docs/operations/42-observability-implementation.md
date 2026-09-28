# Observability Implementation

## Correlation ID

Every request uses X-Correlation-ID. If the caller does not provide one, the API generates one and returns it in the response header.

## Structured logs

The backend emits JSON logs containing timestamp, level, route, status and correlation ID.

## Why this matters

Customer support, incident response and distributed tracing all need a stable identifier that connects browser requests, workflow events, queue messages and external integration calls.

## Production extension

OpenTelemetry will attach the same identifier to traces and span attributes. CloudWatch will collect application logs and alarms will use business and infrastructure metrics.
