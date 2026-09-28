from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class MessageEnvelope:
    message_id: str
    event_type: str
    payload: str
    correlation_id: str


class MessageBus(Protocol):
    def publish(self, message: MessageEnvelope) -> str: ...


class InMemoryMessageBus:
    def __init__(self) -> None:
        self.messages: list[MessageEnvelope] = []

    def publish(self, message: MessageEnvelope) -> str:
        self.messages.append(message)
        return "PUBLISHED"


class SQSMessageBus:
    """Thin AWS adapter. Domain services depend on MessageBus, not boto3."""

    def __init__(self, *, queue_url: str, region_name: str) -> None:
        import boto3  # type: ignore[import-untyped]

        self.queue_url = queue_url
        self.client = boto3.client("sqs", region_name=region_name)

    def publish(self, message: MessageEnvelope) -> str:
        self.client.send_message(
            QueueUrl=self.queue_url,
            MessageBody=message.payload,
            MessageAttributes={
                "event_type": {"DataType": "String", "StringValue": message.event_type},
                "correlation_id": {"DataType": "String", "StringValue": message.correlation_id},
            },
        )
        return "PUBLISHED"