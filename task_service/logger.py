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

    logging.getLogger("aiormq").setLevel(logging.CRITICAL)

    logging.getLogger("aio_pika").setLevel(logging.ERROR)

    # Asyncio
    logging.getLogger("asyncio").setLevel(logging.DEBUG)

    logging.getLogger("pymongo").setLevel(logging.ERROR)

    return logger
