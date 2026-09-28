# Persistent Data Layer

The project is moving from in-memory demo stores to migration-controlled relational persistence.

## PostgreSQL design

PostgreSQL is authoritative for appointment state. The database transaction is the final consistency boundary.

## Partial uniqueness

An active appointment is protected with a unique clinician + start-time index for HELD/CONFIRMED states. Cancelled appointments do not consume the active slot.

## Migration strategy

Alembic owns schema evolution. Application models and migrations are versioned together.

## Local development

SQLite remains available for a zero-Docker demo. PostgreSQL-specific integration tests are required before production because locking, partial indexes and concurrency behaviour must be validated against the production engine.

## Transaction boundary

A production approval command will use one transaction for final availability check, appointment write, audit event and outbox event. Downstream notifications remain asynchronous.