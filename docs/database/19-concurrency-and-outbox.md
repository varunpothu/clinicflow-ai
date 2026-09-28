# Concurrency, Idempotency and Transactional Outbox

## The booking race

Two staff users can see the same candidate slot. Both can approve it. The system must assume the UI is stale and protect the final write.

~~~mermaid
sequenceDiagram
 actor A as Staff A
 actor B as Staff B
 participant API
 participant DB
 A->>API: Approve proposal v3
 B->>API: Approve proposal v3
 API->>DB: Transactional revalidation
 API->>DB: Insert appointment + outbox event
 DB-->>API: Commit
 API-->>A: Confirmed
 API->>DB: Revalidation for B
 DB-->>API: Conflict
 API-->>B: Slot unavailable
~~~

## Idempotency

Every side-effecting command accepts an idempotency key. The key maps to the original result. A replay returns the recorded result instead of creating another appointment.

## Proposal versioning

Approval carries the proposal version. If a staff member approves version 2 after version 3 exists, the command fails as stale rather than applying an obsolete decision.

## Transactional outbox

The appointment write and outbox event are committed in one transaction. A worker later publishes the event to SQS/EventBridge. If publishing fails, the event remains available for retry.

This is deliberately preferred over “write to DB, then publish” because the latter creates a dual-write failure window.
