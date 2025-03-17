import os
import aio_pika
from task_service.logger import setup_logger

logger = setup_logger(__name__)


async def send_notification(tg_id: str, text: str):
    connection = await aio_pika.connect_robust(os.getenv("RABBITMQ_URL"))
    async with connection:
        channel = await connection.channel()

        logger.debug(f"send notification({text}) to bot_servcie for user: {tg_id}")

        await channel.default_exchange.publish(
            aio_pika.Message(body=f"{tg_id}|{text}".encode(), content_type="text/plain"),
            routing_key="bot_notifications_queue",
        )
