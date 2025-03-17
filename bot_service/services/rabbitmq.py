import asyncio
import aio_pika
import uuid
import os


class RabbitMQ:
    def __init__(self, rabbitmq_url: str):
        self.rabbitmq_url = rabbitmq_url
        self.responses = {}

    async def send_message(self, queue_name: str, message: str) -> str:
        connection = await aio_pika.connect_robust(self.rabbitmq_url)
        channel = await connection.channel()

        correlation_id = str(uuid.uuid4())
        callback_queue = await channel.declare_queue(exclusive=True)

        future = asyncio.Future()
        self.responses[correlation_id] = future

        await channel.default_exchange.publish(
            aio_pika.Message(
                body=message.encode(),
                correlation_id=correlation_id,
                reply_to=callback_queue.name,
            ),
            routing_key=queue_name,
        )

        await callback_queue.consume(self._on_response)

        try:
            return await future
        finally:
            await connection.close()

    async def _on_response(self, message: aio_pika.IncomingMessage):
        async with message.process():
            correlation_id = message.correlation_id
            if correlation_id in self.responses:
                future = self.responses.pop(correlation_id)
                future.set_result(message.body.decode())


rabbitmq = RabbitMQ(os.getenv("RABBITMQ_URL"))
