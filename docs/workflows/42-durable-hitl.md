# Durable HITL Workflow

The ASL definition under infrastructure/step-functions models the production workflow boundary.

## Human approval pattern

The workflow pauses using a callback task token. The staff application receives the proposal reference and token through the approval channel. The approval service later signals the waiting execution with success/failure.

## Why this matters

A web request should not stay open while a human decides. Durable workflow state survives process restarts and can enforce an approval timeout.

## Conflict recovery

Final availability revalidation is a separate state after approval. A stale proposal therefore becomes a workflow conflict, not an invalid booking.

## Local alternative

The local deterministic workflow engine keeps state in application memory for development. The business transition rules are shared; AWS Step Functions is the production durability adapter.
