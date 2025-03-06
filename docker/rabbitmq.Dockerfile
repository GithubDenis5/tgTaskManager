# Используем официальный образ RabbitMQ с веб-интерфейсом
FROM rabbitmq:3-management

# Если нужно добавить плагины или настройки
# RUN rabbitmq-plugins enable rabbitmq_management