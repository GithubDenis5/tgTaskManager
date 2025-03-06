import asyncio
import aio_pika
from task_service.processor.message_processor import process_message


async def main():
    connection = await aio_pika.connect_robust("amqp://localhost/")
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue("task_queue", durable=True)

        await queue.consume(process_message)
        print(" [*] Ожидание сообщений...")
        await asyncio.Future()  # Бесконечный цикл


if __name__ == "__main__":
    asyncio.run(main())
