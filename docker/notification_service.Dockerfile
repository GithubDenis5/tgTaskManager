FROM python:3.11-slim

WORKDIR /notification_service

ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY pyproject.toml poetry.lock* ./

RUN pip install --no-cache-dir poetry==1.8.3 \
    && poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi \
    && rm -rf $(poetry config cache-dir)/{cache,artifacts}

COPY . .

ENTRYPOINT ["python3", "-u", "-B", "-m", "notification_service"]
