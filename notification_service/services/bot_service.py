import os
import aio_pika
from task_service.logger import setup_logger

logger = setup_logger(__name__)


async def send_notification(tg_id: str, task_id: str):
    connection = await aio_pika.connect_robust(os.getenv("RABBITMQ_URL"))
    async with connection:
        channel = await connection.channel()

        logger.debug(f"send notification({task_id}) to bot_servcie for user: {tg_id}")

        await channel.default_exchange.publish(
            aio_pika.Message(body=f"notify|{tg_id}|{task_id}".encode(), content_type="text/plain"),
            routing_key="bot_notifications_queue",
        )
