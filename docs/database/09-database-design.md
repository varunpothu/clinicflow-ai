
# Database Design

## Core entities

~~~mermaid
erDiagram
    PATIENT ||--o{ APPOINTMENT_REQUEST : creates
    PATIENT ||--o{ APPOINTMENT : owns
    CLINICIAN ||--o{ APPOINTMENT : receives
    APPOINTMENT_TYPE ||--o{ APPOINTMENT : defines
    APPOINTMENT_REQUEST ||--o{ PROPOSAL : generates
    PROPOSAL ||--o{ APPROVAL : requires
    WORKFLOW_RUN ||--o{ WORKFLOW_EVENT : records
    WORKFLOW_RUN ||--o{ APPOINTMENT_REQUEST : orchestrates
    APPOINTMENT ||--o{ AUDIT_EVENT : produces
    OUTBOX_EVENT }o--|| WORKFLOW_RUN : references
~~~

## Initial tables

patients, clinicians, appointment_types, availability_slots, appointment_requests, proposals, approvals, appointments, workflow_runs, workflow_events, audit_events, outbox_events, idempotency_keys, notifications, ai_interactions.

## Concurrency controls

- Unique constraint over clinician + start_time for active appointments.
- Transactional revalidation immediately before insert.
- Idempotency key for approval and booking commands.
- Version column for proposals and appointments.
- Database transaction wraps appointment write and outbox record.

## Time

Store instants as UTC. Store the clinic's IANA timezone as configuration. Convert only at input/output boundaries. DST-aware logic must be tested.

## Production database

PostgreSQL is the target because transactional integrity, constraints, indexing and concurrency semantics matter more to this domain than horizontally distributed key-value access.
