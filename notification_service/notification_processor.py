import asyncio
import datetime
from notification_service.services.bot_service import send_notification
from notification_service.logger import setup_logger

logger = setup_logger(__name__)


async def handle_notification(task_id: str, tg_id: str, notification_time: str):
    notification_dt = datetime.datetime.fromisoformat(notification_time)
    now = datetime.datetime.now()

    delay = (notification_dt - now).total_seconds()

    logger.debug(f"notification: {task_id} created for user: {tg_id} delay: {delay}")

    if delay > 0:
        await asyncio.sleep(delay)

    await send_notification(tg_id, task_id)
