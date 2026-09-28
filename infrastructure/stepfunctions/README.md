# Durable Workflow Orchestration

This directory defines the production workflow pattern.

## Why Step Functions Standard

The appointment workflow can pause while a staff member reviews a proposal. A durable workflow engine stores this state externally, so an API container does not need to remain alive during human waiting time.

## Human approval callback

The RequestHumanApproval task receives a callback token. The token is associated with the proposal/approval record. When authorised staff approve or reject the proposal, a backend service calls the Step Functions callback API.

## Critical rule

The callback resumes the workflow. It does not itself create the appointment. The next state still performs final slot revalidation and invokes the booking service.

## Why not a long-running API process?

Keeping an HTTP request open for human approval creates poor reliability, scaling and timeout semantics. Durable workflow state is the appropriate boundary for multi-hour human interaction.

## Local mode

The repository's deterministic Python workflow state machine models this behaviour without requiring AWS.
