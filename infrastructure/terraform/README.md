# AWS Infrastructure

This directory contains the production deployment target for ClinicFlow AI.

## Target services

- VPC with public/private subnet boundaries
- API Gateway / edge integration
- ECS/Fargate application
- RDS PostgreSQL
- SQS queue and dead-letter queue
- EventBridge event routing
- S3 analytics/data lake
- IAM least-privilege roles
- KMS encryption keys
- Secrets Manager
- CloudWatch logs/alarms

## Provisioning principle

Terraform is intentionally kept separate from application code. Local development does not require Terraform or an AWS account.

## Deployment sequence

1. Network and security primitives
2. Database and secrets
3. Messaging
4. ECS compute
5. Edge/API
6. Observability
7. Analytics

Environment-specific values belong in tfvars or a secure CI/CD variable store and must never be committed.
