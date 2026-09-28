# Worker Runtime

The repository contains two asynchronous worker boundaries.

## Outbox dispatcher

Reads unpublished transactional outbox events from PostgreSQL and publishes them to the configured booking queue.

## Notification consumer

Long-polls SQS, processes messages and deletes them only after successful notification handling.

## Failure semantics

Transient failures leave the message available for redelivery. Queue redrive policy handles terminal failures through the DLQ.

## Production contract

Workers should run as separate ECS services so CPU/memory scaling and failure isolation can be tuned independently from the HTTP API.
