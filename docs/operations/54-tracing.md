# Distributed Tracing

Each HTTP request receives or propagates an X-Correlation-ID and creates an OpenTelemetry span.

The correlation ID is also logged, allowing a reviewer to connect:
API request -> AI extraction -> workflow -> booking -> outbox -> downstream event.

The current implementation uses the OpenTelemetry API with a no-op/default SDK path, so local execution remains lightweight. A production environment can attach an OTLP exporter or CloudWatch-compatible collector without changing domain services.
