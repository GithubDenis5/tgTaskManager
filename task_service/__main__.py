import asyncio
import aio_pika
from task_service.services.bot_service import process_message
from task_service.requests_processor import init_db
from task_service.logger import setup_logger
from task_service.requests_processor import send_restored_notifications
import os


logger = setup_logger(__name__)


async def main():
    connection = await aio_pika.connect_robust(os.getenv("RABBITMQ_URL"))
    await init_db()
    await send_restored_notifications()
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue("task_queue", durable=True)

        await queue.consume(process_message)
        await asyncio.Future()


if __name__ == "__main__":
    try:
        logger.info("Start Task_Service_App")
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Interrupted")
    except Exception as ex:
        logger.critical(ex)
