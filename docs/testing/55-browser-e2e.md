# Browser E2E

The browser smoke test validates the most important user-facing control-room journey without requiring AWS.

## Covered

- application shell loads
- ClinicFlow branding is visible
- Patient demo navigation works
- natural-language request screen is visible
- human-in-the-loop boundary copy is visible

## Why not automate real booking here?

The full booking E2E requires a running API, database and test identity provider. The smoke test intentionally isolates the UI shell. A second environment-level suite will exercise API + PostgreSQL + external-scheduler sandbox together.
