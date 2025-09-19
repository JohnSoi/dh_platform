"""Константы логгера"""

__author__ = "Старков Е.П."

from enum import StrEnum

# Делитель для перевода информации
FILE_SIZE_DELIMITER: int = 1024


class LogLevel(StrEnum):
    """
    Уровни логирования. Верхние уровни включают в себя все нижние.

    :cvar DEBUG: уровень отладки. Рекомендуется только при разработке
    :cvar INFO: информационные сообщения - вызов метода, запрос и т.д.
    :cvar WARN: предупреждения
    :cvar ERROR: ошибки
    """

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARN = "WARN"
    ERROR = "ERROR"
