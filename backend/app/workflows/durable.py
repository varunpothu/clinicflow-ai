import json
from dataclasses import dataclass
from typing import Protocol

from app.workflows.states import WorkflowState


@dataclass(frozen=True)
class WorkflowCommand:
    workflow_id: str
    state: WorkflowState
    correlation_id: str
    input_payload: dict[str, object]


class DurableWorkflow(Protocol):
    def start(self, command: WorkflowCommand) -> str: ...


class LocalWorkflowEngine:
    def __init__(self) -> None:
        self.runs: dict[str, WorkflowCommand] = {}

    def start(self, command: WorkflowCommand) -> str:
        self.runs[command.workflow_id] = command
        return command.workflow_id


class StepFunctionsWorkflow:
    def __init__(self, state_machine_arn: str, region_name: str) -> None:
        import boto3

        self.state_machine_arn = state_machine_arn
        self.client = boto3.client("stepfunctions", region_name=region_name)

    def start(self, command: WorkflowCommand) -> str:
        response = self.client.start_execution(
            stateMachineArn=self.state_machine_arn,
            name=command.workflow_id,
            input=json.dumps({
                "workflow_id": command.workflow_id,
                "state": command.state,
                "correlation_id": command.correlation_id,
                "input": command.input_payload,
            }),
        )
        return str(response["executionArn"])
