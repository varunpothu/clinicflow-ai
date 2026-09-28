# Cost Model

This is an architecture model, not a live AWS quotation.

## Main cost drivers

- ECS/Fargate compute
- RDS PostgreSQL compute and storage
- Bedrock inference
- S3 and data transfer
- CloudWatch logs and metrics
- API Gateway requests
- SQS/EventBridge requests
- Athena queries and BI usage

## Cost controls

Local development must not require AWS resources. CI should use mocks where possible. Development environments should be small, time-bounded and disposable. Logs require retention policies. AI requests need input/output size and retry limits.

## Alternative for very small workloads

A Lambda + DynamoDB architecture can reduce infrastructure management for low-volume workloads. It is not the target here because the portfolio is designed to demonstrate relational consistency, durable workflow control and containerised customer deployment.
