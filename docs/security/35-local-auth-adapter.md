# Local Identity Adapter

The local demo uses optional X-Demo-Role and X-Demo-Subject headers to simulate an authenticated principal.

This is deliberately isolated from business services.

## Production replacement

In AWS, the same dependency boundary will map Cognito/JWT claims to the internal Principal object. Controllers and domain services should not need to know how the user authenticated.

## Important

The local default exists only to keep the portfolio demo runnable. A production deployment must require a real identity provider and server-side authorisation checks.
