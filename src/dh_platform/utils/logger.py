"""Модуль логирования в приложении"""

__author__: str = "Старков Е.П."

import logging
import sys

from logging.handlers import RotatingFileHandler
from pathlib import Path

from dh_platform.config import base_settings
from dh_platform.types import LogLevelType
from dh_platform.consts.logger import FILE_SIZE_DELIMITER, LogLevel


def setup_logger(
    name: str = base_settings.LOG_NAME,
    log_level: LogLevelType = LogLevel.WARN,
    log_file: str | None = None,
    max_bytes: int = base_settings.LOG_FILE_SIZE_MB * FILE_SIZE_DELIMITER * FILE_SIZE_DELIMITER,
    backup_count: int = 5
) -> logging.Logger:
    """
    Настройка логгера для приложения

    :param name: название логгера
    :type name: str
    :param log_level: уровень логирования
    :type log_level: LogLevelType
    :param log_file: файл для логов
    :type log_file: str | None
    :param max_bytes: максимальный размер в байтах
    :type max_bytes: int
    :param backup_count: количество файлов бекапа
    :type backup_count: int
    :return: логгер
    :rtype: logging.Logger

    .. code-block:: python
        from dh_platform.logger import setup_logger

        # Глобальный логгер
        logger: logging.Logger = setup_logger(
            log_level=base_settings.LOG_LEVEL,
            log_file=base_settings.LOG_DIRECTORY if not base_settings.SAVE_LOG_FILES else None
        )
    """
    app_logger: logging.Logger = logging.getLogger(name)
    app_logger.setLevel(getattr(logging, log_level.upper()))

    # Форматтер
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s [%(filename)s:%(lineno)d]"
    )

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    app_logger.addHandler(console_handler)

    # File handler (если указан файл)
    if log_file:
        # Создаем директорию если не существует
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding="utf-8"
        )
        file_handler.setFormatter(formatter)
        app_logger.addHandler(file_handler)

    return app_logger


# Глобальный логгер
logger: logging.Logger = setup_logger(
    log_level=base_settings.LOG_LEVEL,
    log_file=base_settings.LOG_DIRECTORY if not base_settings.SAVE_LOG_FILES else None
)