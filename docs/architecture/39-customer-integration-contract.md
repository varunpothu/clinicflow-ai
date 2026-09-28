# Customer Integration Contract

## Why this boundary exists

NorthStar Health Clinic is fictional, but a real FDE engagement would rarely replace the customer's whole scheduling platform. ClinicFlow therefore treats the external clinic/EHR scheduling system as a contract.

## Adapter interface

The application depends on:
- availability lookup
- appointment creation

The implementation can be:
- local mock system
- REST API adapter
- FHIR-based adapter
- vendor SDK adapter
- queue/event integration

## Integration rules

1. External identifiers are preserved.
2. Time values use the agreed clinic timezone at the integration boundary and UTC internally.
3. External conflicts become explicit workflow conflicts.
4. Retries must be idempotent.
5. Integration credentials remain outside application source code.
6. Contract tests run against a sandbox/mock provider before production.

## FDE value

This turns the project from a standalone scheduling app into a customer-deployment pattern: discover the customer's interface, map it to a stable internal contract, then swap the adapter without rewriting the workflow.
