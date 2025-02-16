FROM python:3.11-slim

WORKDIR /bot_service

# Copy pyproject.toml and poetry.lock for dependency installation
COPY pyproject.toml poetry.lock* ./

# Install Poetry and dependencies
RUN python -m pip install --no-cache-dir poetry==1.8.3 \
    && poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi \
    && rm -rf $(poetry config cache-dir)/{cache,artifacts}

# Copy the rest of the application code
COPY . .

# Set the entrypoint for the bot
ENTRYPOINT ["python3", "-u", "-B", "-m", "bot_service"]
