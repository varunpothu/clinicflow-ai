# AI Evaluation Plan

## Dataset categories

- exact date and time
- date range
- after/before constraints
- clinician preference
- appointment type
- ambiguous request
- missing information
- cancellation
- rescheduling
- unsupported clinical questions
- prompt injection
- malformed/adversarial input

## Metrics

Intent accuracy; field extraction accuracy; clarification rate; structured-output validity; unsafe-input detection; prompt-version regression rate; latency; provider error/fallback rate.

## Release gate

A prompt or model change must pass the synthetic regression suite, schema validation and safety cases before promotion.

## Important boundary

AI evaluation measures administrative language handling. It is not a measure of clinical correctness.
