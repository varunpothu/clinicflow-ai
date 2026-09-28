# Cognito Identity Boundary

ClinicFlow keeps JWT verification outside business services.

## Production path

Client -> Cognito -> API Gateway/JWT authorizer -> verified claims -> CognitoClaimsMapper -> Principal -> RBAC -> application service.

The application should not re-implement token cryptography in every endpoint. The edge authorizer handles signature/issuer/audience validation; the mapper turns trusted claims into the provider-neutral Principal object.

## Local path

The local demo uses X-Demo-Role and X-Demo-Subject headers so the same RBAC logic can be exercised without a cloud identity provider.

## Fail closed

Missing subject, clinic or recognised role is an authentication/authorisation failure.
