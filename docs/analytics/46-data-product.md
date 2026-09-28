# Analytics Data Product

## Architectural principle

The transactional PostgreSQL database is the system of record. Reporting is a downstream data product.

## Pipeline

Transactional outbox -> SQS/EventBridge -> S3 raw zone -> Glue crawler/catalog -> Athena -> BI semantic layer.

## Why not query PostgreSQL directly?

Direct reporting queries can couple operational workloads to dashboard traffic and make schema evolution harder. The event contract allows the reporting model to evolve independently.

## First data products

### Scheduling Operations
- requests per day
- proposals created
- approvals per day
- median approval latency
- booking success rate
- conflict rate

### Patient Operations
- cancellation rate
- reschedule rate
- waitlist demand
- notification delivery rate

### AI Operations
- extraction success
- clarification rate
- schema-validation failures
- provider latency
- fallback rate

## Privacy

Free-form patient text is excluded from analytics events. Synthetic identifiers and operational metadata are sufficient for the demo.
