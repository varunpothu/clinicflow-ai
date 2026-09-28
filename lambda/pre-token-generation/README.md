# Cognito Pre-Token Generation Trigger

This Lambda copies the user's clinic identifier into the access token as a clinic_id claim.

ClinicFlow API Gateway maps that verified access-token claim into the internal principal header before the request reaches the private ALB.

The trigger is intentionally small and deterministic: it does not call external services or make authorization decisions.