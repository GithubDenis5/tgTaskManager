from config import messages


async def format_tasks_list(tasks: list):
    if not tasks:
        return "✅ У вас нет активных задач!"

    return "".join(
        messages.TASK_FORMATER.format(
            task["description"], task["description"], task["deadline"], task["reminder"]
        )
        for task in tasks
    ).strip()
