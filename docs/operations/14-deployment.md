
# Deployment Strategy

## Local

- Python virtual environment
- SQLite for zero-dependency bootstrap
- mock AI provider
- local deterministic workflow engine
- no AWS credentials required for tests

## AWS target

~~~mermaid
flowchart LR
    Internet --> CF[CloudFront]
    CF --> WAF[WAF]
    WAF --> APIGW[API Gateway]
    APIGW --> ECS[ECS Fargate]
    ECS --> RDS[RDS PostgreSQL]
    ECS --> SQS[SQS + DLQ]
    ECS --> EB[EventBridge]
    ECS --> BED[Bedrock]
    SQS --> Worker[Worker Fargate]
    Worker --> S3[S3]
    EB --> S3
    S3 --> Athena[Athena]
    Athena --> QS[QuickSight]
~~~

## CI/CD

1. Lint and format validation
2. Type checks
3. Unit and integration tests
4. Security and secret scans
5. Container build
6. Push image to ECR
7. Terraform plan
8. Controlled deployment
9. Smoke tests
10. Post-deployment health verification

Production promotion should be gated by successful tests and an explicit environment approval.
