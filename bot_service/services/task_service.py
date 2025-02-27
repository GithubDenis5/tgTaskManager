from bot_service.services.rabbitmq import rabbitmq
from bot_service.services.utils import ADD_TASK_MQ, GET_TASK_BY_ID_MQ, EDIT_TASK_MQ

from bot_service.logger import setup_logger

logger = setup_logger(__name__)


async def get_tasks(tg_id: int):
    """Получить все задачи для user

    Args:
        tg_id (int): telegram id

    Returns:
        _type_: задачи из бд
    """
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

    message = f"get_task|{tg_id}"

    response = await rabbitmq.send_message("task_queue", message)

    logger.debug(f"get_tasks answer: {response}")

    return result


async def add_task(tg_id: int, name: str, description: str, deadline: str, notification: str):
    """Добавить новую задачу

    Args:
        tg_id (int): telegram id
        name (str): название задачи
        description (str): пояснение
        deadline (str): дата окончания
        notification (str): дата напоминания
    """

    # Формируем сообщение
    message = ADD_TASK_MQ.format(tg_id, name, description, deadline, notification)

    # Отправляем сообщение и ждем ответ
    response = await rabbitmq.send_message("task_queue", message)

    logger.debug(f"add_task answer: {response}")

    pass


async def get_task(tg_id: int, task_id: str):
    """Получение задачи по id

    Args:
        tg_id (int): telegram id
        task_id (str): id задачи

    Returns:
        _type_: вернуть задачу из бд
    """
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

    message = GET_TASK_BY_ID_MQ.format(tg_id, task_id)

    response = await rabbitmq.send_message("task_queue", message)

    logger.debug(f"get_tasks answer: {response}")

    return None


async def edit_task(tg_id, task_id, field, deadline, notification):
    """Редактирование задачи

    Args:
        tg_id (_type_): telegram id
        task_id (_type_): id задачи
        field (_type_): complete(надо переместить в архив)/delete(удалить из бд)/prolong(изменить
            deadline и notification на новые)
        deadline (_type_): новый дедлайн
        notification (_type_): новое уведомление
    """

    message = EDIT_TASK_MQ.format(tg_id, task_id, field, deadline, notification)

    response = await rabbitmq.send_message("task_queue", message)

    logger.debug(f"edit_task field-{field} answer: {response}")

    pass
