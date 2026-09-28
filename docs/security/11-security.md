
# Security and Privacy Design

## Security model

Roles:

PATIENT, RECEPTIONIST, CLINICIAN, ADMIN, PLATFORM_OPERATOR, SYSTEM.

Authorisation is enforced server-side on every protected operation. Frontend controls are usability features, not security boundaries.

## Data classification

Synthetic patient data is treated as if it were sensitive during engineering. Logs should prefer IDs and metadata over free-text content. Secrets never enter source control.

## Controls

- TLS for data in transit
- KMS-backed encryption for production stores
- Secrets Manager for application secrets
- IAM least privilege
- Cognito for user identity
- WAF and rate limiting at the edge
- request correlation IDs
- audit events for privileged actions
- immutable event history
- dependency and secret scanning in CI

## AI threat model

Threats include prompt injection, data exfiltration, model hallucination, schema bypass, tool abuse, denial through expensive prompts and unsafe persistence.

Mitigations include untrusted-input separation, strict schemas, tool allowlists, deterministic validation, bounded retries, cost/size limits and human approval.

## Key rule

No LLM response can directly execute a booking mutation.
