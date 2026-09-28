
# AI Architecture

## AI responsibilities

Allowed:

- classify appointment intent
- extract dates, time windows, appointment type and preferences
- ask a clarification question
- produce a structured proposal explanation

Not allowed:

- direct SQL
- arbitrary HTTP calls
- modifying appointments
- changing clinic rules
- bypassing an approval requirement
- making clinical recommendations

## Guardrail pipeline

~~~mermaid
flowchart TD
    Input[Patient text] --> Sanitize[Input normalization]
    Sanitize --> Prompt[Versioned prompt]
    Prompt --> Model[LLM provider]
    Model --> Schema[Strict structured output]
    Schema --> Rules[Deterministic validation]
    Rules -->|valid| Workflow[Continue workflow]
    Rules -->|invalid| Repair[One bounded repair attempt]
    Repair --> Schema
    Rules -->|unsafe or ambiguous| Human[Human clarification]
~~~

## Provider strategy

Local development uses a mock provider that returns deterministic fixtures. Production uses an adapter for Amazon Bedrock. A future direct-provider adapter can be added without changing the domain contract.

## Prompt injection controls

Patient text is treated as untrusted data. System instructions are separate from user content. Tool calls use an allowlist and strict JSON schemas. The model never receives secrets or unrestricted database access.

## AI evaluation

The synthetic evaluation set will score intent classification, field extraction, schema validity, refusal/clarification behaviour, tool selection, latency and regression rate.
