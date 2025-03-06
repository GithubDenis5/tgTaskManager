FROM python:3.11-slim

WORKDIR /task_service

# Копируем файлы проекта
COPY pyproject.toml poetry.lock* ./

# Устанавливаем зависимости через Poetry
RUN pip install --no-cache-dir poetry==1.8.3 \
    && poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi \
    && rm -rf $(poetry config cache-dir)/{cache,artifacts}

# Копируем оставшиеся файлы
COPY . .

# Указываем точку входа
ENTRYPOINT ["python3", "-u", "-B", "-m", "task_service"]