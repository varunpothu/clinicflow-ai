# Demo Script

## 1. Customer problem
Show NorthStar Health Clinic's operational problem and current-state pain points.

## 2. Patient request
Enter a natural-language scheduling request such as: “I need a routine consultation next week after 4pm, preferably Tuesday or Wednesday.”

## 3. AI extraction
Show the structured request and explain that model output is untrusted until validated.

## 4. Deterministic availability
Show candidate slots produced by scheduling rules.

## 5. Human approval
Open the staff queue. Modify a proposed time and approve it.

## 6. Race-condition demonstration
Simulate another booking taking the slot before final commit. Show conflict handling, proposal regeneration and audit history.

## 7. Exception handling
Force a notification failure and show retry, eventual DLQ and exception visibility.

## 8. Observability
Show correlation ID, workflow events, metrics and audit history.

## 9. Architecture explanation
Explain why AI is constrained, why PostgreSQL is used, why the outbox exists and why production workflow durability is separate from AI orchestration.
