# Terraform Roadmap

## Why start with small AWS primitives?

The first infrastructure code deliberately provisions messaging, analytics storage and logging primitives. Network, database, ECS, IAM and secrets are added as separate modules once application contracts stabilise.

This keeps infrastructure changes reviewable and demonstrates incremental FDE delivery rather than a single opaque infrastructure file.

## Next modules

- networking
- security
- RDS PostgreSQL
- ECS cluster/service
- task definition
- ALB
- API Gateway
- Cognito
- Bedrock IAM policy
- SQS/EventBridge
- S3 analytics
- CloudWatch alarms

## Alternative

AWS CDK could express the same target in Python/TypeScript. Terraform was selected so infrastructure remains provider-agnostic at the authoring layer and easy to review as declarative state.
