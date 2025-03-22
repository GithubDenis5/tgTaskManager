from bot_service.config import messages
from datetime import datetime, timedelta


def format_datetime(iso_str: str) -> str:
    dt = datetime.fromisoformat(iso_str)
    return dt.strftime("%d.%m.%Y %H:%M")


def get_time_left(deadline: str) -> str:
    deadline_dt = datetime.fromisoformat(deadline)
    now = datetime.now()
    delta: timedelta = deadline_dt - now

    if delta.total_seconds() <= 0:
        return "Просрочено"

    days, remainder = divmod(delta.total_seconds(), 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, _ = divmod(remainder, 60)

    parts = []
    if days:
        parts.append(f"{int(days)} д.")
    if hours:
        parts.append(f"{int(hours)} ч.")
    if minutes or not parts:
        parts.append(f"{int(minutes)} мин.")

    return " ".join(parts)


async def format_tasks_list(tasks: list):
    if not tasks:
        return "✅ У вас нет активных задач!"

    return "".join(
        messages.TASK_FOR_LIST_FORMATTER.format(
            task["name"],
            format_datetime(task["deadline"]),
            get_time_left(task["deadline"]),
        )
        for task in tasks
    ).strip()


def convert_datetime(date_str: str, time_str: str) -> str:
    dt = datetime.strptime(f"{date_str} {time_str}", "%d.%m.%Y %H:%M")
    return dt.strftime("%Y-%m-%dT%H:%M:%S")


async def format_task_info(task):
    return "".join(
        messages.TASK_INFO_FORMATER.format(
            task["name"],
            task["description"],
            format_datetime(task["deadline"]),
            format_datetime(task["notification"]),
        )
    ).strip()
