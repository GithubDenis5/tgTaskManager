import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
import aio_pika

from bot_service.handler import user
from bot_service.middlewares.logging import LoggingMiddleware
from bot_service.logger import setup_logger
from bot_service.services.notification_service import process_notification

logger = setup_logger(__name__)

RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost/")
BOT_QUEUE = "bot_notifications_queue"


async def consume_notifications(bot: Bot):
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue(BOT_QUEUE, durable=True)

        logger.info("Notification consumming started")

        async for message in queue:
            async with message.process():
                await process_notification(bot, message.body.decode())


async def main():
    dp = Dispatcher()
    dp.include_routers(user)
    dp.callback_query.middleware(LoggingMiddleware())
    dp.message.middleware(LoggingMiddleware())

    bot = Bot(token=os.getenv("TOKEN_BOT"), default=DefaultBotProperties(parse_mode="html"))
    logger.info("Bot start")

    await asyncio.gather(dp.start_polling(bot), consume_notifications(bot))


if __name__ == "__main__":
    try:
        logger.info("Start Bot_Service_App")
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Interrupted")
    except Exception as ex:
        logger.critical(ex)
