from bot_service.services.rabbitmq import rabbitmq
from bot_service.services.utils import ADD_TASK_MQ, GET_TASK_BY_ID_MQ, EDIT_TASK_MQ

from bot_service.logger import setup_logger

import json

logger = setup_logger(__name__)


async def parse_tasks_to_list(input_str):
    try:
        return json.loads(input_str)
    except json.JSONDecodeError:
        fixed_str = input_str.replace("'", '"')
        return json.loads(fixed_str)


async def add_user(tg_id: int):
    message = f"add_user|{tg_id}"

    response = await rabbitmq.send_message("task_queue", message)

    return response


async def get_tasks(tg_id: int):
    message = f"get_tasks|{tg_id}"

    response = await parse_tasks_to_list(await rabbitmq.send_message("task_queue", message))

    logger.debug(f"get_tasks answer: {response}")

    return response


async def add_task(tg_id: int, name: str, description: str, deadline: str, notification: str):
    message = ADD_TASK_MQ.format(tg_id, name, description, deadline, notification)

    response = await rabbitmq.send_message("task_queue", message)

    logger.debug(f"add_task answer: {response}")


async def get_task(tg_id: int, task_id: str):
    message = GET_TASK_BY_ID_MQ.format(tg_id, task_id)

    response = await parse_tasks_to_list(await rabbitmq.send_message("task_queue", message))

    logger.debug(f"get_tasks answer: {response}")

    return response


async def edit_task(tg_id, task_id, field, deadline, notification):
    message = EDIT_TASK_MQ.format(tg_id, task_id, field, deadline, notification)

    response = await rabbitmq.send_message("task_queue", message)

    logger.debug(f"edit_task field-{field} answer: {response}")
