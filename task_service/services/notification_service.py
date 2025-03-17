import os
import aio_pika


async def publish_task_update(
    event: str, task_id: str, tg_id: str, notification_time: str | None = None
):
    rabbitmq_url = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost/")

    message = f"{event}|{task_id}|{tg_id}"
    if notification_time:
        message += f"|{notification_time}"

    connection = await aio_pika.connect_robust(rabbitmq_url)
    async with connection:
        channel = await connection.channel()

        queue = await channel.declare_queue("task_updates_queue", durable=True)

        await channel.default_exchange.publish(
            aio_pika.Message(
                body=message.encode(),
                content_type="text/plain",
            ),
            routing_key=queue.name,
        )
