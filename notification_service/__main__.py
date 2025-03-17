import asyncio
import aio_pika
import os
from notification_service.logger import setup_logger
from notification_service.services.task_service import process_task_update

logger = setup_logger(__name__)


async def main():
    connection = await aio_pika.connect_robust(os.getenv("RABBITMQ_URL"))
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue("task_updates_queue", durable=True)

        async for message in queue:
            async with message.process():
                await process_task_update(message.body.decode())


if __name__ == "__main__":
    try:
        logger.info("Start Notification_Service_App")
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Interrupted")
    except Exception as ex:
        logger.critical(ex)
