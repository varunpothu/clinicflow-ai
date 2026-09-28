import asyncio

from app.core.config import get_settings
from app.db.session import SessionLocal
from app.integrations.sqs import SQSMessagePublisher
from app.services.outbox_dispatcher import OutboxDispatcher


async def run_once() -> int:
    settings = get_settings()
    queue_url = settings.booking_queue_url
    if not queue_url:
        raise RuntimeError('BOOKING_QUEUE_URL_REQUIRED')
    publisher = SQSMessagePublisher(queue_url, settings.aws_region)
    async with SessionLocal() as session:
        return await OutboxDispatcher(session, publisher).dispatch_batch()


if __name__ == '__main__':
    print(asyncio.run(run_once()))