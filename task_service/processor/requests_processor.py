from task_service.logger import setup_logger

logger = setup_logger(__name__)


async def get_tasks_by_id(tg_id: int):
    result = [
        {
            "task_id": "abc123",
            "name": "Отчет",
            "description": "Сделать отчет",
            "deadline": "2025-02-20T18:00:00",
            "notification": "2025-02-19T10:00:00",
        },
        {
            "task_id": "xyz789",
            "name": "Презентация",
            "description": "Подготовить презентацию",
            "deadline": "2025-02-22T15:00:00",
            "notification": "2025-02-21T09:00:00",
        },
    ]

    return result


async def add_new_task_from_user(
    tg_id: int, name: str, description: str, deadline: str, notification: str
):

    # усли нет ошибки, то возвращаем 0, иначе 1

    return "0"


async def get_task_by_task_id(tg_id: int, task_id: str):
    result = [
        {
            "task_id": "abc123",
            "name": "Отчет",
            "description": "Сделать отчет",
            "deadline": "2025-02-20T18:00:00",
            "notification": "2025-02-19T10:00:00",
        },
        {
            "task_id": "xyz789",
            "name": "Презентация",
            "description": "Подготовить презентацию",
            "deadline": "2025-02-22T15:00:00",
            "notification": "2025-02-21T09:00:00",
        },
    ]
    if task_id == "abc123":
        return result[0]
    elif task_id == "xyz789":
        return result[1]


async def edit_task_by_task_id(tg_id, task_id, field, deadline, notification):

    # усли нет ошибки, то возвращаем 0, иначе 1

    return "0"


async def add_user(tg_id: int):

    return "0"
