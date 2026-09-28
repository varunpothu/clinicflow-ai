# Architecture Summary

## Selected approach

- FastAPI for a lightweight typed API layer
- PostgreSQL for transactional booking state
- SQLite for zero-dependency local development
- Bedrock behind an AI provider abstraction
- deterministic domain services for business rules
- human approval for controlled booking side effects
- Step Functions for durable cloud workflow waits/retries
- SQS/EventBridge-style event delivery
- transactional outbox for database-to-event consistency
- ECS/Fargate for persistent application runtime
- API Gateway + Cognito JWT at the authenticated edge
- Terraform for cloud infrastructure
- React/TypeScript for the operations console

## Important alternatives

### Lambda instead of ECS
Good for sporadic workloads and less server management. ECS was chosen for predictable long-running API behaviour and simpler packaging of a multi-service runtime.

### DynamoDB instead of PostgreSQL
Good for high-scale key-value access and serverless patterns. PostgreSQL was chosen because appointment transactions, relational reporting and concurrency constraints are central to the problem.

### Direct model SDK instead of Bedrock
Simpler for a single provider. The Bedrock abstraction keeps enterprise AWS deployment, model choice and provider boundaries cleaner.

### Kafka instead of SQS/EventBridge
Kafka offers strong streaming capabilities and ecosystem depth. SQS/EventBridge keeps this workflow simpler, cheaper to operate and sufficient for the event volume expected in the demonstration.

### Temporal/custom workflow engine instead of Step Functions
Temporal can provide rich workflow semantics. Step Functions was selected for native AWS durability, callback waits and operational integration.

## Design rule

Every alternative is judged against the customer problem, failure mode, operational burden and FDE delivery timeline. The selected stack is intentionally modular so alternatives can be swapped behind interfaces.
