# Demonstration Scenarios

## Scenario A: happy path
Patient asks for a routine consultation. AI extracts scheduling intent. Rules find a slot. Staff approves. Booking commits. Audit and outbox events are created.

## Scenario B: ambiguity
Patient says "book something soon." The model cannot safely infer a date/window. Workflow requests clarification.

## Scenario C: race condition
Two staff members approve proposals for the same clinician/time. One succeeds. The second hits the final database uniqueness guard and returns a conflict.

## Scenario D: duplicate submission
The same approval is submitted twice with the same idempotency key. The second request returns the original booking result.

## Scenario E: notification failure
Booking succeeds, notification provider fails, retry budget is consumed, message moves to DLQ. Appointment remains confirmed.

## Scenario F: prompt injection
Patient text attempts to reveal the system prompt or bypass instructions. Input guardrails reject it before model processing.
