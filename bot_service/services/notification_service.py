from aiogram import Bot

from bot_service.logger import setup_logger
from bot_service.services.task_service import get_task
from bot_service.utils.formaters import format_task_info
from bot_service.config import messages
from bot_service.utils.keyboards import task_info_keyboard

logger = setup_logger(__name__)


async def process_notification(bot: Bot, message: str):
    logger.debug(message)

    parts = message.split("|")
    if len(parts) != 3:
        logger.warning(f"unexpected message format: {message}")
        return

    command, tg_id, task_id = parts
    logger.debug(f"get notification for task: {task_id}")

    task_info = await get_task(tg_id, task_id)

    text = messages.NOTIFICATION

    text += await format_task_info(task_info)

    kb = await task_info_keyboard(task_id, 1)

    await bot.send_message(chat_id=tg_id, text=text, reply_markup=kb)
