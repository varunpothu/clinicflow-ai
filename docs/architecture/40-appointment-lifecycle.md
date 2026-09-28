# Persisted Appointment Lifecycle

## Controlled states

CONFIRMED -> CANCELLED

CONFIRMED -> RESCHEDULED (same appointment identity, incremented version)

## Concurrency

Rescheduling includes the expected appointment version. A stale client cannot silently overwrite a newer appointment state.

The database active-slot uniqueness constraint is the final conflict backstop. If the new slot is already used, the transaction is rejected and the original appointment change is rolled back.

## Side effects

Cancellation and rescheduling create audit events and outbox events in the same transaction as the appointment change.

## Idempotency

Both commands require an idempotency key. Replaying the same command returns the original result. Reusing the key with a different fingerprint fails closed.
