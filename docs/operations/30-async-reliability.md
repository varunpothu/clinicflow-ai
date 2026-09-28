# Async Reliability

## Why asynchronous work is separated

Appointment confirmation should not depend on an email provider being available at the exact moment the database transaction commits. The booking transaction records the intent to publish an event; a worker handles downstream notifications.

## Flow

Booking transaction -> Outbox event -> Queue -> Notification worker -> Provider

Failures follow:

Provider error -> bounded retry -> retry delay -> terminal failure -> DLQ -> staff exception queue

## Retry policy

Retries use exponential backoff with a hard maximum delay and a maximum attempt count. This prevents runaway retry storms.

## Operational principle

A failed notification is not a failed booking. The appointment remains authoritative while notification delivery is tracked independently.

## Local mode

The worker uses an in-memory console adapter for demonstrations. Production will use SQS and a provider adapter such as SES/SNS or another approved channel.
