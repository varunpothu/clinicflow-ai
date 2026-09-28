# Messaging Adapter

## Contract

The domain publishes a message envelope containing a message ID, event type, serialized payload and correlation ID.

The domain does not know whether the message is handled by an in-memory test bus or Amazon SQS.

## Production path

Transactional outbox -> publisher worker -> SQS -> notification/integration worker.

## Why not call SQS directly from the booking transaction?

The booking transaction should not depend on network availability or a queue API. The outbox provides durable intent; a worker performs the external publish.

## Failure handling

A failed publish increments the attempt count. After the configured maximum, the event moves into an operational failure path for investigation and replay.

## Future event routing

EventBridge can fan out selected domain events to analytics and integration consumers while SQS remains the work queue for task-style processing.