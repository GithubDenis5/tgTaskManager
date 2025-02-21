import asyncio
import aio_pika
import uuid


class RabbitMQ:
    def __init__(self, rabbitmq_url: str):
        self.rabbitmq_url = rabbitmq_url
        self.connection = None
        self.channel = None
        self.responses = {}

    async def connect(self):
        """Устанавливает соединение с RabbitMQ (если не установлено)"""
        if not self.connection:
            self.connection = await aio_pika.connect_robust(self.rabbitmq_url)
            self.channel = await self.connection.channel()

    async def send_message(self, queue_name: str, message: str) -> str:
        """Отправляет сообщение и ожидает ответ с тем же correlation_id"""
        await self.connect()

        correlation_id = str(uuid.uuid4())  # Генерируем уникальный ID
        callback_queue = await self.channel.declare_queue(exclusive=True)  # Временная очередь

        future = asyncio.Future()
        self.responses[correlation_id] = future  # Сохраняем ожидание ответа

        # Отправляем сообщение с `correlation_id` и `reply_to`
        await self.channel.default_exchange.publish(
            aio_pika.Message(
                body=message.encode(),
                correlation_id=correlation_id,
                reply_to=callback_queue.name,
            ),
            routing_key=queue_name,
        )

        # Подписываемся на очередь ответов
        await callback_queue.consume(self._on_response)

        return await future  # Ожидаем ответ

    async def _on_response(self, message: aio_pika.IncomingMessage):
        """Обрабатывает ответ и передает его в соответствующий Future"""
        correlation_id = message.correlation_id
        if correlation_id in self.responses:
            future = self.responses.pop(correlation_id)
            future.set_result(message.body.decode())


# Глобальный клиент RabbitMQ
rabbitmq = RabbitMQ("amqp://localhost/")
