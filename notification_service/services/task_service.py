import asyncio
from notification_service.notification_processor import handle_notification
from task_service.logger import setup_logger

logger = setup_logger(__name__)


scheduled_notifications = {}


async def process_task_update(message: str):
    logger.debug(f"process update: {message}")

    parts = message.split("|")
    command, task_id, tg_id = parts[:3]
    notification_time = parts[3] if len(parts) > 3 else None

    if command in ("add_new", "edit"):
        if task_id in scheduled_notifications:
            logger.debug(f"delete existing notification for task: {task_id}")
            scheduled_notifications[task_id].cancel()

        task = asyncio.create_task(handle_notification(task_id, tg_id, notification_time))
        logger.debug(f"create notification for task: {task_id}")
        scheduled_notifications[task_id] = task

    elif command in ("complete", "delete"):
        if task_id in scheduled_notifications:
            logger.debug(f"delete notification for task: {task_id}")
            scheduled_notifications[task_id].cancel()
            del scheduled_notifications[task_id]
