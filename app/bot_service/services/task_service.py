async def get_tasks(tg_id: int):
    result = [
        {
            "task_id": "abc123",
            "description": "Сделать отчет",
            "deadline": "2025-02-20T18:00:00",
            "reminder": "2025-02-19T10:00:00",
        },
        {
            "task_id": "xyz789",
            "description": "Подготовить презентацию",
            "deadline": "2025-02-22T15:00:00",
            "reminder": "2025-02-21T09:00:00",
        },
    ]
    return result
