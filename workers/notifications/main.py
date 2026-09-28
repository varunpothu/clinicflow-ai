from app.services.notifications import (
    ConsoleNotificationGateway,
    NotificationChannel,
    NotificationMessage,
    NotificationWorker,
)


def run_demo() -> str:
    gateway = ConsoleNotificationGateway()
    worker = NotificationWorker(gateway)
    message = NotificationMessage(
        notification_id="not-1001",
        recipient_ref="patient-001",
        channel=NotificationChannel.EMAIL,
        body="Your NorthStar Health Clinic appointment is confirmed.",
    )
    return worker.process(message)


if __name__ == "__main__":
    print(run_demo())
