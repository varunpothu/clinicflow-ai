
# Contributing

ClinicFlow AI follows a small-change, traceable engineering workflow.

## Local checks

Run the backend tests with pytest. Run Ruff for linting and formatting checks. Run MyPy for static typing.

## Commit convention

Use conventional commit prefixes such as:

- feat(api): add appointment request endpoint
- feat(booking): enforce double-booking protection
- feat(ai): add structured intent extraction
- test(workflow): cover approval expiry
- docs(architecture): record workflow orchestration decision

## Design rule

Every production behaviour should have a documented requirement, a test, and an observable audit or metric where appropriate.
