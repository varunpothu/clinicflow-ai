from dataclasses import dataclass
from enum import StrEnum


class NotificationChannel(StrEnum):
    EMAIL = "EMAIL"
    SMS = "SMS"


@dataclass(frozen=True)
class NotificationMessage:
    notification_id: str
    recipient_ref: str
    channel: NotificationChannel
    body: str


class NotificationGateway:
    def send(self, message: NotificationMessage) -> None:
        raise NotImplementedError


class ConsoleNotificationGateway(NotificationGateway):
    def __init__(self) -> None:
        self.sent: list[NotificationMessage] = []

    def send(self, message: NotificationMessage) -> None:
        self.sent.append(message)


class NotificationWorker:
    def __init__(
        self,
        gateway: NotificationGateway,
        max_attempts: int = 3,
    ) -> None:
        self.gateway = gateway
        self.max_attempts = max_attempts

    def process(self, message: NotificationMessage, attempt: int = 1) -> str:
        if attempt > self.max_attempts:
            return "DLQ"
        try:
            self.gateway.send(message)
        except Exception:
            if attempt >= self.max_attempts:
                return "DLQ"
            return f"RETRY:{attempt + 1}"
        return "SENT"
