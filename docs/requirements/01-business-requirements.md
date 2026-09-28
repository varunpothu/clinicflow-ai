
# Business Requirements

## Customer

NorthStar Health Clinic is a fictional multi-clinician clinic used to model a realistic customer engagement. The operational problem is appointment administration: requests arrive through inconsistent channels, staff spend time interpreting intent and checking availability, and booking changes are hard to audit.

## Problem statement

The system must reduce administrative effort while keeping booking authority with authorised people and keeping the scheduling result deterministic.

## Outcomes

| Outcome | Target interpretation |
|---|---|
| Faster request handling | Reduce manual interpretation and repeated availability checks |
| Fewer avoidable errors | Validate requests and re-check slots immediately before booking |
| Better operational control | Give staff an approval queue, exception view and workflow state |
| Traceability | Record who, what, when and why for material workflow decisions |
| Safe AI adoption | Keep model output constrained to structured proposals |

## Scope

In scope: patient appointment requests, availability search, proposal creation, staff approval, booking, cancellation, rescheduling, reminders, exception handling, audit, operational analytics and customer integration.

Out of scope: diagnosis, triage, treatment recommendation, prescription, autonomous clinical decisions and real patient data.

## Success measures

The project will measure request-to-proposal latency, human approval latency, successful booking rate, double-booking prevention, exception rate, retry rate, notification delivery rate and AI extraction/evaluation metrics.
