# Clinic Scheduling System Integration

## Why an adapter

Customer systems differ. One clinic may expose REST, another may use a message interface or an existing scheduling platform.

The workflow therefore depends on the provider-neutral ClinicSchedulingSystem contract.

## Contract

- availability lookup
- idempotent appointment creation
- deterministic conflict errors
- external appointment reference
- timezone-aware timestamps

## Conflict model

External booking conflict becomes an explicit operational event. It does not silently create a second local appointment.

## System-of-record options

### ClinicFlow as system of record
Local PostgreSQL commits first and the external system is synchronised asynchronously.

### Existing scheduler as system of record
External booking executes first and ClinicFlow stores the external reference.

### Hybrid
A local hold is created first, followed by external confirmation before the hold becomes confirmed.

The demo uses PostgreSQL as the application store and a mock external scheduler to demonstrate the customer integration boundary.