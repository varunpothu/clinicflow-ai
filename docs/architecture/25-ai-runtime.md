# AI Runtime Architecture

## Runtime boundary

Patient text flows through input guardrails, a versioned system prompt, Bedrock Converse, a constrained extraction tool, strict schema validation and then deterministic scheduling.

Unsafe or ambiguous requests move toward clarification rather than invented values.

## AWS implementation

ClinicFlow uses the Amazon Bedrock Runtime Converse API as its production adapter. AWS currently documents Converse as a common interface across supported models and the bedrock-runtime endpoint as the current runtime path for new inference applications. Bedrock Guardrails can be attached to Converse calls for policy evaluation. citeturn702348search0turn702348search1turn702348search5turn702348search2

Application validation remains mandatory. The generated tool-call arguments are validated by the application because the Converse guardrail path does not evaluate generated tool arguments. citeturn702348search2

## Why the model still cannot book

A valid model payload creates only an informational AppointmentIntent. Scheduling rules create candidates. Approval and booking services own controlled side effects.

## Local mode

The mock provider is deterministic. The test suite therefore works without AWS credentials or inference cost.
