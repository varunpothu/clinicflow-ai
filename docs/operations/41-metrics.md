# Application Metrics

ClinicFlow keeps business and technical telemetry behind a small application metrics abstraction.

## Local

The registry provides deterministic counters and bounded latency samples for the demo environment.

## Production

The metrics abstraction will be bridged to CloudWatch/OpenTelemetry. Domain services should record business events such as booking conflicts, proposal approvals, retries and AI fallback usage without depending directly on a monitoring vendor.

## Current HTTP metrics

- http.requests.total
- http.status.<status_code>
- http.request latency

The registry intentionally keeps bounded samples so local demos do not grow memory without limit.
