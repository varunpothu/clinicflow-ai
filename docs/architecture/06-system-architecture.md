
# System Architecture

## Logical architecture

~~~mermaid
flowchart LR
    Patient[Patient UI] --> Web[Web App]
    Staff[Staff Console] --> Web
    Web --> Edge[CloudFront + WAF]
    Edge --> API[API Gateway]
    API --> App[FastAPI on ECS/Fargate]
    App --> Workflow[Workflow Services]
    App --> DB[(RDS PostgreSQL)]
    Workflow --> AIGW[AI Gateway]
    AIGW --> Bedrock[Amazon Bedrock]
    Workflow --> Queue[SQS]
    Workflow --> Bus[EventBridge]
    Queue --> Worker[Worker Services]
    Worker --> DB
    Worker --> Notify[Notification Adapter]
    Bus --> Analytics[S3 / Glue / Athena]
    Analytics --> BI[QuickSight]
    App --> Obs[CloudWatch + OTel]
    Worker --> Obs
~~~

## Trust boundaries

1. Browser to edge
2. Edge to application
3. Application to data and integration services
4. AI provider boundary
5. Asynchronous worker boundary
6. Analytics boundary

Sensitive operations such as booking writes stay behind application services. The model has no direct database credentials and no arbitrary tool execution.

## Local versus production

Local mode replaces AWS dependencies with deterministic adapters. Production can swap in Cognito, Bedrock, RDS, SQS/EventBridge and CloudWatch without changing the core scheduling domain.
