
# Workflow Design

## State machine

~~~mermaid
stateDiagram-v2
    [*] --> RECEIVED
    RECEIVED --> EXTRACTING
    EXTRACTING --> NEEDS_CLARIFICATION
    EXTRACTING --> VALIDATING
    NEEDS_CLARIFICATION --> RECEIVED
    VALIDATING --> SEARCHING_AVAILABILITY
    SEARCHING_AVAILABILITY --> NO_AVAILABILITY
    SEARCHING_AVAILABILITY --> PROPOSED
    NO_AVAILABILITY --> WAITING_FOR_STAFF
    PROPOSED --> WAITING_FOR_APPROVAL
    WAITING_FOR_APPROVAL --> APPROVED
    WAITING_FOR_APPROVAL --> REJECTED
    WAITING_FOR_APPROVAL --> EXPIRED
    APPROVED --> REVALIDATING
    REVALIDATING --> BOOKING
    REVALIDATING --> CONFLICT
    CONFLICT --> PROPOSED
    BOOKING --> CONFIRMED
    BOOKING --> BOOKING_RETRY
    BOOKING_RETRY --> BOOKING
    BOOKING_RETRY --> FAILED
    CONFIRMED --> CANCELLED
    CONFIRMED --> RESCHEDULE_REQUESTED
~~~

## Why separate AI orchestration from business workflow?

AI orchestration is good at interpreting unstructured requests and choosing among a small allowlist of tools. Durable business workflows need explicit state, timeouts, retries, compensation and human callbacks.

Therefore ClinicFlow AI uses an AI gateway inside a deterministic workflow. AWS Step Functions is the production durability adapter; the domain state machine remains testable without AWS.

## Human approval

A proposal contains a version, expiry timestamp and immutable requested fields. Approval records the approver identity and the proposal version. An approval for a superseded version is rejected as stale.
