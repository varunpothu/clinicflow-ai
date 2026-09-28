# Staff Console

The staff console is designed as an operational control room rather than a generic CRUD screen.

## Main areas

### Overview
Shows:
- pending approvals
- confirmed bookings
- open exceptions
- AI extraction quality
- service pulse

### Approval queue
Each proposal displays the patient, appointment type, clinician, proposed time, status and age. Actions are explicit: approve, reject, modify or resolve conflict.

### Workflow timeline
A chronological view links request, AI extraction, proposal, approval, booking and exception events.

### Exception health
Exceptions use semantic severity:
- red = high/critical
- amber = medium
- blue/green = informational or low operational risk

### System pulse
The dashboard surfaces API latency, AI latency, database latency and outbox backlog.

## Interaction principle

The frontend is not the security boundary. Approval, identity and authorisation are enforced by the backend. The UI mirrors the server state and provides operators with explainable context.
