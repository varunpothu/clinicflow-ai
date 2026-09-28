# Support and Operating Model

## L1: Clinic staff
Handles patient-facing clarification, proposal review and ordinary scheduling exceptions.

## L2: Platform operations
Handles workflow failures, queues, DLQ items, infrastructure and deployment issues.

## L3: Engineering
Handles defects, integration contract changes, AI regressions and architectural changes.

## Incident priorities

CRITICAL: uncontrolled side effect, data-integrity concern or full booking outage.

HIGH: booking conflicts or workflow failure affecting active patient operations.

MEDIUM: delayed notification, degraded AI extraction or elevated queue age.

LOW: non-blocking analytics or demo-environment issue.

## Incident evidence

Capture:
- correlation ID
- workflow ID
- proposal/appointment ID
- timestamps
- exception code
- retry count
- last known workflow state

Do not copy sensitive patient free text into tickets or ordinary logs.
