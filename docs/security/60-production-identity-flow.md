# Production Identity Boundary

## Request path

Cognito issues the access token. API Gateway validates the JWT signature, issuer and audience before invoking the private integration.

API Gateway then overwrites internal headers from verified JWT and request context values:

- X-Principal-Subject
- X-Principal-Clinic
- X-Principal-Groups
- X-Correlation-ID

FastAPI consumes only these trusted headers when APP_ENV is not local.

Client-supplied X-Demo-* headers are accepted only in local mode.

## Security boundary

The ALB is internal and accepts traffic from the API Gateway VPC Link security group. The backend therefore does not expose a direct public application path.

The backend still treats missing, malformed, or unknown claims as authentication failures.

## Claim contract

The production access token must provide:

- sub
- custom:clinic_id (or clinic_id)
- cognito:groups containing one supported ClinicFlow role

For a multi-clinic rollout, identity provisioning must guarantee the clinic claim for every user.