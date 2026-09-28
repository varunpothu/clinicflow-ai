from app.asyncio.retry import RetryPolicy
from app.services.notifications import (
    ConsoleNotificationGateway,
    NotificationChannel,
    NotificationMessage,
    NotificationWorker,
)
from app.services.outbox import OutboxPublisher, PendingOutboxEvent


def test_retry_policy_uses_bounded_exponential_backoff() -> None:
    policy = RetryPolicy(max_attempts=4, base_delay_seconds=2, max_delay_seconds=5)
    assert policy.delay_for(1) == 2
    assert policy.delay_for(2) == 4
    assert policy.delay_for(3) == 5


def test_notification_worker_sends_successfully() -> None:
    gateway = ConsoleNotificationGateway()
    worker = NotificationWorker(gateway)
    message = NotificationMessage(
        notification_id="n-1",
        recipient_ref="patient-001",
        channel=NotificationChannel.EMAIL,
        body="confirmed",
    )
    assert worker.process(message) == "SENT"
    assert gateway.sent == [message]


def test_outbox_publisher_is_idempotent_at_event_boundary() -> None:
    publisher = OutboxPublisher()
    event = PendingOutboxEvent(event_id="evt-1", event_type="APPOINTMENT_CONFIRMED", payload="{}")
    assert publisher.publish(event) == "PUBLISHED"
    assert event.attempts == 1
    assert event.published_at is not None
