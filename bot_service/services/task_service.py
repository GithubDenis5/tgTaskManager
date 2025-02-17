async def get_tasks(tg_id: int):
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


async def add_task(name: str, description: str, deadline: str, notification: str):
    pass


async def get_task(tg_id: int, task_id: int):
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

    return None


async def edit_task(tg_id, task_id, field, deadline, notification):
    pass
