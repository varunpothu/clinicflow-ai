# Schema Map

| Table | Purpose | Critical controls |
|---|---|---|
| patients | synthetic patient identity | unique external reference |
| clinicians | clinician directory | active flag |
| appointment_types | duration/configuration | positive duration |
| appointments | authoritative booking state | active-slot uniqueness, version |
| workflow_runs | durable workflow state | state + correlation indexes |
| approvals | human decision state | proposal version + expiry |
| outbox_events | downstream event guarantee | publish state + attempt count |

The schema is deliberately relational. Business-critical state is kept in the same transaction as its audit/outbox effects where practical.
