# Используем Python 3.11
FROM python:3.11

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта
COPY app/bot_service /app

# Устанавливаем Poetry
RUN pip install poetry

# Устанавливаем зависимости
RUN poetry install --no-root

# Запускаем бота
CMD ["poetry", "run", "python", "-m", "bot_service"]
