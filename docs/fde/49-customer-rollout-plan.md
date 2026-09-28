# FDE Customer Rollout Plan

## Phase 0: Discovery
- map current appointment workflow
- identify existing scheduling/EHR system
- document appointment types, durations, clinics and staff roles
- identify approval policy and exception ownership
- agree integration system-of-record

## Phase 1: Sandbox
- use synthetic patients and clinicians
- connect only to mock/external sandbox endpoints
- replay representative request scenarios
- measure extraction, clarification, proposal and booking behaviour

## Phase 2: Controlled pilot
- one clinic/location
- limited staff cohort
- human approval required for every controlled booking
- daily exception review
- explicit rollback procedure

## Phase 3: Production expansion
- additional clinicians
- additional locations
- notification channels
- operational dashboards
- alerting and SLOs
- scheduled disaster recovery tests

## Rollback

Rollback should disable new workflow executions and preserve existing confirmed appointments. Pending proposals can be expired. Outbox events remain replayable.

## Customer success measures

- reduced manual scheduling effort
- lower approval turnaround time
- lower booking conflict rate
- high workflow completion rate
- low notification failure rate
- zero uncontrolled booking side effects
