import json
from typing import Any

from app.services.notifications import NotificationChannel, NotificationMessage, NotificationWorker


class SQSNotificationConsumer:
    def __init__(self, client: Any, queue_url: str, worker: NotificationWorker) -> None:
        self.client = client
        self.queue_url = queue_url
        self.worker = worker

    def poll_once(self) -> int:
        response = self.client.receive_message(
            QueueUrl=self.queue_url,
            MaxNumberOfMessages=10,
            WaitTimeSeconds=20,
            VisibilityTimeout=60,
        )
        messages = response.get('Messages', [])
        processed = 0

        for raw in messages:
            body = json.loads(raw['Body'])
            notification = NotificationMessage(
                notification_id=str(body['notification_id']),
                recipient_ref=str(body['recipient_ref']),
                channel=NotificationChannel(str(body['channel'])),
                body=str(body['body']),
            )
            attempt = int(body.get('attempt', 1))
            outcome = self.worker.process(notification, attempt)
            if outcome == 'SENT':
                self.client.delete_message(
                    QueueUrl=self.queue_url,
                    ReceiptHandle=raw['ReceiptHandle'],
                )
            processed += 1

        return processed