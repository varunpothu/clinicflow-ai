# Production Boundaries

ClinicFlow separates identity, AI inference, business workflow, appointment state, downstream delivery, audit and analytics.

| Boundary | Authority | Failure strategy |
|---|---|---|
| Identity | Cognito adapter / Principal | fail closed |
| AI | Bedrock adapter | clarification/fallback |
| Business workflow | deterministic workflow | durable state + retry |
| Appointment state | PostgreSQL | transaction + constraints |
| Delivery | SQS/EventBridge | retry + DLQ |
| Audit | append-oriented persistence | preserve history |
| Analytics | S3/Glue/Athena | asynchronous |

The local identity adapter uses headers only for development. Production maps verified Cognito claims to the same Principal type. Business code does not depend on Cognito APIs.

The local workflow engine provides a deterministic contract. Production can use Step Functions for durable, long-running approval waits and retries.

The domain emits logical events. The delivery adapter chooses SQS, EventBridge or a local implementation.
