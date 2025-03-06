import logging
import os
from logging.handlers import RotatingFileHandler


def setup_logger(logger_name):
    """Настройка логгеров.

    Returns:
        Logger: Логгер.
    """

    if len(logging.getLogger().handlers) > 0:
        return logging.getLogger(logger_name)

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),
        ],
    )

    # Custom
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    # # Aiogram
    # logging.getLogger("aiogram").setLevel(logging.DEBUG)

    logging.getLogger("aiormq").setLevel(logging.CRITICAL)

    logging.getLogger("aio_pika").setLevel(logging.ERROR)

    # Asyncio
    logging.getLogger("asyncio").setLevel(logging.DEBUG)

    return logger
