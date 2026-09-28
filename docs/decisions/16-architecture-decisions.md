# Architecture Decision Records

## ADR-001: FastAPI over Django REST
Decision: FastAPI. The platform is API/workflow focused and benefits from typed request models and a framework-light domain layer. Django REST remains a viable alternative when a richer built-in admin ecosystem is the primary requirement.

## ADR-002: PostgreSQL over DynamoDB
Decision: PostgreSQL. Scheduling needs transactional writes, relational constraints, clear joins and strong conflict protection. DynamoDB scales well but would move more consistency logic into application code.

## ADR-003: Deterministic workflow plus AI gateway
Decision: keep durable business orchestration separate from the LLM. AI is probabilistic; booking control requires explicit state, timers, retries and human callbacks. LangGraph is useful for AI orchestration but is not the sole source of durable business state. Temporal is powerful but adds platform complexity beyond this portfolio scope.

## ADR-004: Human-in-the-loop approval
Decision: mandatory approval before controlled booking. This demonstrates safe administrative automation without granting autonomous write authority to the model.

## ADR-005: SQS/EventBridge over Kafka
Decision: SQS + EventBridge. AWS-native managed primitives cover work queues and event routing with lower operational burden. Kafka/MSK is a future option for larger streaming ecosystems.

## ADR-006: ECS/Fargate over Lambda-only
Decision: ECS/Fargate for the core service. It provides container parity, shared Python dependencies and predictable long-running service behaviour. Lambda remains useful for small event handlers.

## ADR-007: Bedrock behind provider abstraction
Decision: Bedrock adapter behind a common AI interface. This aligns the production target with AWS while avoiding provider lock-in inside domain logic.

## ADR-008: Transactional outbox
Decision: persist outbound events in the same database transaction as business state. This prevents the dual-write gap between a booking change and event publication. Direct publish is simpler but can lose events after a successful DB commit.

## ADR-009: Synthetic healthcare data
Decision: synthetic data only. The portfolio does not need real patient information and should demonstrate strong controls without creating unnecessary privacy exposure.
