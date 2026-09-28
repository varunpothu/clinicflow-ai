# Role-Based Access Control

## Roles

PATIENT, RECEPTIONIST, CLINICIAN, ADMIN, PLATFORM_OPERATOR and SYSTEM.

## Permission model

Permissions are explicit capabilities rather than broad endpoint labels. The backend checks permissions server-side.

## Examples

- PATIENT can create an appointment request and view their own appointments.
- RECEPTIONIST can approve scheduling proposals.
- CLINICIAN can view permitted clinic schedule information.
- ADMIN can configure clinic settings.
- PLATFORM_OPERATOR can inspect operational exceptions and replay workflows.
- SYSTEM has no default human business permissions.

## Fail-closed rule

Unknown permissions and missing authorisation must fail closed.

## Production identity adapter

The local principal object is intentionally provider-neutral. A future Cognito adapter will map claims/groups to this internal principal before application services execute.
