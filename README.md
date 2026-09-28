# ClinicFlow AI

AI-assisted, human-in-the-loop clinic appointment orchestration for a fictional customer, NorthStar Health Clinic.

> **Core control principle:** AI proposes → deterministic rules validate → human approves → system executes → every important action is auditable.

This repository is a portfolio-grade Forward Deployed Engineer (FDE) project. It demonstrates discovery, workflow design, API engineering, AI guardrails, integration design, cloud architecture, security, observability, testing, deployment, incident response, and operational documentation.

## Safety boundary
ClinicFlow AI uses synthetic data only. It is an administrative scheduling system, not a clinical decision-support, diagnosis, triage, or treatment system. The AI layer is intentionally constrained: it can interpret scheduling intent and propose structured actions, but it cannot directly mutate the booking database.

## Build strategy
The project is designed local-first and cloud-ready:

- Backend: Python, FastAPI, SQLAlchemy
- Frontend: React + TypeScript
- Data: PostgreSQL in production, SQLite-compatible local bootstrap
- AI: provider abstraction with Amazon Bedrock as the AWS production adapter
- Workflow: deterministic domain state machine locally, AWS Step Functions adapter for durable production orchestration
- Async integration: transactional outbox + SQS/EventBridge
- Cloud: ECS/Fargate, RDS PostgreSQL, S3, CloudWatch, Cognito, IAM, KMS, Secrets Manager
- Infrastructure: Terraform
- CI/CD: GitHub Actions
- Observability: structured logs, correlation IDs, metrics, traces, audit events
- Testing: unit, integration, API, workflow, AI evaluation, and end-to-end tests

## Repository map

- docs/requirements — customer problem, personas, journeys, functional and non-functional requirements
- docs/architecture — system, integration, AI, resilience, and deployment architecture
- docs/workflows — appointment request, approval, booking, exception, retry, cancellation, and rescheduling flows
- docs/database — data model, constraints, indexing, concurrency and retention decisions
- docs/api — API contract and error model
- docs/security — threat model, RBAC, privacy controls, auditability and AI safety
- docs/operations — observability, testing, deployment, incident response, cost controls
- docs/decisions — architecture decision records and rejected alternatives
- backend — FastAPI application and domain services
- frontend — staff and patient web applications
- workers — asynchronous jobs and integration workers
- data/synthetic — reproducible synthetic clinic data
- infrastructure/terraform — AWS infrastructure as code
- .github/workflows — CI/CD automation

## Target workflow

1. A patient expresses a scheduling request in natural language or structured form.
2. The application creates an immutable request and workflow run.
3. AI extracts scheduling intent into a strict schema.
4. Deterministic validation checks required fields and booking policy.
5. Availability is queried using deterministic scheduling rules.
6. A proposal is generated with explainable reasons and a validity window.
7. A receptionist or authorised staff member approves, rejects, or modifies the proposal.
8. Booking is revalidated immediately before the write to prevent stale-slot races.
9. The appointment is created transactionally and an audit event is recorded.
10. Notifications and analytics are emitted asynchronously through the outbox.
11. Failures enter retry/DLQ/exception workflows rather than disappearing silently.

## Documentation-first delivery
The first implementation milestone establishes the customer contract and operating model before deep application code. Later milestones add the runnable booking engine, AI adapters, staff console, integration sandbox, Terraform, and production hardening.

## Disclaimer
This is a portfolio engineering project using fictional entities and synthetic data. It is not an NHS or healthcare-provider production system and must not be connected to real patient data without a full security, privacy, clinical-safety, compliance, and governance programme.