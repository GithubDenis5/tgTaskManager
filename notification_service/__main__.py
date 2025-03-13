import asyncio
from notification_service.logger import setup_logger

logger = setup_logger(__name__)


def main():
    pass


if __name__ == "__main__":
    try:
        logger.info("Start Notification_Service_App")
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Interrupted")
    except Exception as ex:
        logger.critical(ex)
