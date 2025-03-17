import asyncio
import os
import aio_pika

from task_service.logger import setup_logger
import task_service.requests_processor as rp

logger = setup_logger(__name__)


async def process_request(request: str):
    request_function = request.split("|")[0]
    tg_id = request.split("|")[1]

    logger.debug(f"get |{request_function}| from user:{tg_id}")

    match request_function:
        case "add_task":
            _, _, name, description, deadline, notification = request.split("|")
            return await rp.add_new_task_from_user(
                tg_id, name, description, deadline, notification
            )
        case "get_task":
            _, _, task_id = request.split("|")
            return await rp.get_task_by_task_id(tg_id, task_id)
        case "edit_task":
            _, _, task_id, field, deadline, notification = request.split("|")
            return await rp.edit_task_by_task_id(tg_id, task_id, field, deadline, notification)
        case "get_tasks":
            return await rp.get_tasks_by_id(tg_id)
        case "add_user":
            return await rp.add_user(tg_id)

    return 0


async def process_message(message: aio_pika.IncomingMessage):
    async with message.process():
        request = message.body.decode()

        response = str(await process_request(request))

        # connection = await aio_pika.connect_robust("amqp://localhost/")
        connection = await aio_pika.connect_robust(os.getenv("RABBITMQ_URL"))
        async with connection:
            channel = await connection.channel()
            await channel.default_exchange.publish(
                aio_pika.Message(
                    body=response.encode(),
                    correlation_id=message.correlation_id,  # Возвращаем тот же ID
                ),
                routing_key=message.reply_to,
            )
            logger.debug(f"send to user: {response}")
