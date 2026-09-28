# Analytics Data Product

ClinicFlow treats operational analytics as a downstream data product rather than querying the transactional database for every dashboard.

## Event flow

Booking transaction -> transactional outbox -> EventBridge/SQS -> S3 raw events -> Glue catalog -> Athena models -> BI dashboards.

## Core measures

- request volume
- clarification rate
- proposal conversion
- approval latency
- booking success/conflict rate
- cancellation rate
- reschedule rate
- notification failure rate
- AI fallback rate
- workflow retry rate

## Data contract

The event schema in events/appointment-event.schema.json defines the stable analytics-facing contract. The transactional schema may evolve independently.

## Privacy design

Analytics events use synthetic identifiers and operational metadata. Free-form patient text is excluded.
