import asyncio
import os
from handler import user
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from middlewares.logging import LoggingMiddleware

from logger import setup_logger

logger = setup_logger(__name__)


async def main():

    dp = Dispatcher()
    dp.include_routers(user)
    dp.callback_query.middleware(LoggingMiddleware())
    dp.message.middleware(LoggingMiddleware())

    bot = Bot(token=os.getenv("TOKEN_BOT"), default=DefaultBotProperties(parse_mode="html"))
    logger.info("Bot start")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        logger.info("Start Bot_Service_App")
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Interrupted")
    except Exception as ex:
        logger.critical(ex)
