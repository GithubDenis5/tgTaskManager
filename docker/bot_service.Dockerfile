FROM python:3.11-slim

WORKDIR /bot_service

COPY pyproject.toml poetry.lock* ./

RUN python -m pip install --no-cache-dir poetry==1.8.3 \
    && poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi \
    && rm -rf $(poetry config cache-dir)/{cache,artifacts}

COPY . .

ENTRYPOINT ["python3", "-u", "-B", "-m", "bot_service"]
