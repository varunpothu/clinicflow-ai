# Container Runtime

The backend Dockerfile packages the FastAPI application for ECS/Fargate.

## Runtime rules

- non-root execution will be added to the hardened production image
- health checks should call the liveness endpoint
- secrets are injected at runtime
- environment-specific configuration is externalised
- image tags should be immutable commit SHAs in deployment pipelines

The local Windows workflow does not require Docker. The Dockerfile exists for CI and AWS deployment parity.
