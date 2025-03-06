import logging
import sys
from logging.handlers import RotatingFileHandler


def configure_logging(name: str = "sms_client") -> logging.Logger:
    """Конфигурация системы логирования

        Args:
            name (str): Название логгера. По умолчанию 'sms_client'

        Returns:
            Logger: Объект логгера.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)

    file_handler = RotatingFileHandler(
        "sms_client.log",
        maxBytes=1024 * 1024,
        backupCount=3,
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)

    if logger.hasHandlers():
        logger.handlers.clear()

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


# Инициализация основного логгера
logger = configure_logging()
