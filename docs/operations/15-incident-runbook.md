
# Incident Runbook

## P1: duplicate booking suspected

1. Stop further automated booking attempts.
2. Inspect the workflow and idempotency records.
3. Confirm database appointment uniqueness.
4. Identify affected synthetic scenario.
5. Preserve audit evidence.
6. Resolve manually through the staff workflow.
7. Root-cause the race, retry or idempotency path.
8. Add a regression test before re-enabling the path.

## P1: AI provider outage

The application switches to the configured deterministic mock/fallback behaviour for non-production demonstrations or moves requests into a human clarification state. Booking authority is not expanded because the model is unavailable.

## P2: queue backlog

Inspect queue depth, age, worker capacity, retry count and downstream dependency errors. Scale workers if safe, otherwise pause retries and drain after dependency recovery.

## Operational principle

Prefer a visible exception over a silent success. Every automatic retry has a bounded limit and a terminal state.
