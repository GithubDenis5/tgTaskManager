import asyncio
import aio_pika


async def process_message(message: aio_pika.IncomingMessage):
    """Обработка входящего сообщения и отправка ответа"""
    async with message.process():
        request = message.body.decode()
        print(f" [x] Получено сообщение: {request}")

        response = f"Шаблонный ответ на: {request}"

        # Отправляем ответ в `reply_to` с `correlation_id`
        connection = await aio_pika.connect_robust("amqp://localhost/")
        async with connection:
            channel = await connection.channel()
            await channel.default_exchange.publish(
                aio_pika.Message(
                    body=response.encode(),
                    correlation_id=message.correlation_id,  # Возвращаем тот же ID
                ),
                routing_key=message.reply_to,  # Отправляем в указанную очередь
            )
            print(f" [x] Отправлен ответ: {response}")


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
