# ClinicFlow AI Project Status

Updated: 2026-09-28

## Completed

### Customer and FDE design
- customer problem statement
- personas and permissions
- user journeys and current/future workflow
- functional and non-functional requirements
- architecture decision records
- local Windows setup
- interview/demo script
- visual design system and colorful architecture illustrations

### Backend
- FastAPI application
- API versioning
- appointment request intake
- deterministic request validation
- explicit workflow state machine
- availability engine
- proposal generation
- server-owned proposal approval
- idempotency controls
- conflict-safe booking service
- cancellation and rescheduling
- deterministic waitlist matching
- audit event model and API
- operational exception model and API
- correlation ID middleware
- structured JSON logging
- database readiness probe

### AI
- strict appointment-intent contract
- prompt versioning
- input-length guardrail
- prompt-injection guardrails
- deterministic mock AI provider
- Amazon Bedrock Converse adapter
- constrained extraction tool schema
- post-model Pydantic validation
- synthetic AI evaluation fixtures
- AI release-gate documentation

### Persistence
- SQLAlchemy models
- PostgreSQL target design
- SQLite local bootstrap
- Alembic runtime setup
- initial migration
- active appointment partial uniqueness
- proposal and approval repositories
- appointment repository
- workflow event repository
- audit repository
- outbox repository
- persistent idempotency repository
- atomic approval-to-book transaction service

### Async and integration
- transactional outbox model
- notification worker
- retry policy
- DLQ behaviour
- provider-neutral messaging interface
- SQS adapter
- mock clinic scheduling-system adapter
- external booking conflict handling
- durable Step Functions HITL workflow definition

### Frontend
- React + TypeScript staff operations console
- colorful dashboard
- approval queue
- conflict indicators
- workflow timeline
- exception health
- system pulse
- patient natural-language demo screen

### Infrastructure and CI
- Terraform foundation
- SQS/DLQ, S3 and CloudWatch primitives
- backend container image
- GitHub Actions backend CI
- GitHub Actions frontend build/typecheck
- Terraform format/init/validate

## Current milestone

Production-shaped local workflow + AI gateway + persistent relational design + HITL control plane + customer integration boundary.

## Next implementation

1. Replace remaining in-memory demo stores with repository-backed APIs.
2. Add full approval/patient/appointment persistence endpoints.
3. Add Cognito/JWT production identity adapter.
4. Add complete AWS network/RDS/ECS/IAM Terraform modules.
5. Add SQS worker runtime with DLQ replay tooling.
6. Add OpenTelemetry traces and business metrics.
7. Add synthetic AI regression runner.
8. Add analytics pipeline and dashboard data model.
9. Add full end-to-end browser tests.
10. Add deployment workflow and environment promotion gates.

## Non-negotiable architectural rule

AI never receives unrestricted database access and cannot bypass human approval for controlled booking side effects.
