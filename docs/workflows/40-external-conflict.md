# External Scheduling Conflict

A customer scheduling platform may disagree with ClinicFlow's locally observed availability.

Flow:

Local candidate -> final local check -> external availability check -> external booking -> confirmation.

If the external system reports a conflict, ClinicFlow records an integration conflict and returns to proposal generation. It does not assume the local cache is authoritative.

This is an intentional consistency boundary for real-world customer integrations.
