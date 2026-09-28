import json
from typing import Protocol


class EventPublisher(Protocol):
    def publish(self, *, event_type: str, payload: dict[str, object], deduplication_key: str) -> str: ...


class ConsoleEventPublisher:
    def __init__(self) -> None:
        self.events: list[dict[str, object]] = []

    def publish(self, *, event_type: str, payload: dict[str, object], deduplication_key: str) -> str:
        self.events.append({
            "event_type": event_type,
            "payload": payload,
            "deduplication_key": deduplication_key,
        })
        return deduplication_key


class SQSMessagePublisher:
    def __init__(self, queue_url: str, region_name: str) -> None:
        import boto3  # type: ignore[import-untyped]

        self.queue_url = queue_url
        self.client = boto3.client("sqs", region_name=region_name)

    def publish(self, *, event_type: str, payload: dict[str, object], deduplication_key: str) -> str:
        body = json.dumps({
            "event_type": event_type,
            "payload": payload,
            "deduplication_key": deduplication_key,
        })
        response = self.client.send_message(
            QueueUrl=self.queue_url,
            MessageBody=body,
            MessageAttributes={
                "event_type": {"DataType": "String", "StringValue": event_type},
                "deduplication_key": {"DataType": "String", "StringValue": deduplication_key},
            },
        )
        return str(response["MessageId"])
