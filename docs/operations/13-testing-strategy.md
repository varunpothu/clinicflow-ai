
# Testing Strategy

## Test pyramid

~~~mermaid
flowchart BT
    Unit[Unit tests] --> Service[Service and domain tests]
    Service --> API[API and repository integration tests]
    API --> Workflow[Workflow tests]
    Workflow --> E2E[End-to-end tests]
    AI[AI evaluation suite] --> Workflow
~~~

## Required cases

- valid appointment request
- missing patient information
- ambiguous date or time
- no availability
- proposal expiry
- approval rejection
- approval of stale proposal
- double approval
- simultaneous booking race
- booking retry
- permanent booking failure
- notification failure
- cancellation
- rescheduling
- authorisation failure
- idempotency replay
- prompt injection attempt
- invalid AI structured output
- AI provider outage and fallback

## Test environments

Unit tests use pure Python and mocks. Repository tests can use SQLite for fast local feedback. PostgreSQL integration tests are required in CI before production deployment because SQLite cannot reproduce every PostgreSQL locking and constraint behaviour.
