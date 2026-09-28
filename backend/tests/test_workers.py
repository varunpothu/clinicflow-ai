import json

from app.services.notifications import ConsoleNotificationGateway, NotificationWorker
from app.workers.sqs_consumer import SQSNotificationConsumer


class FakeSQS:
    def __init__(self) -> None:
        self.deleted: list[str] = []

    def receive_message(self, **_: object) -> dict[str, object]:
        return {
            "Messages": [{
                "Body": json.dumps({
                    "notification_id": "n-1",
                    "recipient_ref": "patient-001",
                    "channel": "EMAIL",
                    "body": "confirmed",
                    "attempt": 1,
                }),
                "ReceiptHandle": "receipt-1",
            }]
        }

    def delete_message(self, **kwargs: object) -> None:
        self.deleted.append(str(kwargs["ReceiptHandle"]))


def test_sqs_consumer_deletes_successful_message() -> None:
    gateway = ConsoleNotificationGateway()
    queue = FakeSQS()
    consumer = SQSNotificationConsumer(queue, "queue", NotificationWorker(gateway))
    assert consumer.poll_once() == 1
    assert queue.deleted == ["receipt-1"]
