from bot_service.config import messages
from datetime import datetime


def format_datetime(iso_str: str) -> str:
    """Преобразует строку в ISO формате в формат 'дд.мм.гггг чч:мм'."""
    dt = datetime.fromisoformat(iso_str)
    return dt.strftime("%d.%m.%Y %H:%M")


async def format_tasks_list(tasks: list):
    if not tasks:
        return "✅ У вас нет активных задач!"

    return "".join(
        messages.TASK_FOR_LIST_FORMATER.format(
            task["name"],
            format_datetime(task["deadline"]),
        )
        for task in tasks
    ).strip()
