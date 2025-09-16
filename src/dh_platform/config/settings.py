"""Модуль конфигурации приложений"""

__author__: str = "Старков Е.П."

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings

from dh_platform.consts.logger import LogLevel
from dh_platform.types import LogLevelType


class BaseAppSettings(BaseSettings):
    """
    Класс с базовыми настройками приложения

    :cvar DATABASE_URL: адрес подключения к БД
    :type DATABASE_URL: PostgresDsn
    :cvar DB_ECHO: логирование sql запросов включено
    :type DB_ECHO: bool
    :cvar DB_POOL_SIZE: размер пула соединенйи с БД
    :type DB_POOL_SIZE: int
    :cvar DB_MAX_OVERFLOW: максимальное количество временных соединений поверх пула
    :type DB_MAX_OVERFLOW: int

    :cvar APP_NAME: название приложения
    :type APP_NAME: str
    :cvar DEBUG: режим отладки
    :type DEBUG: bool
    """

    DATABASE_URL: PostgresDsn
    DB_ECHO: bool = False
    DB_POOL_SIZE: int = 20
    DB_MAX_OVERFLOW: int = 10

    APP_NAME: str
    DEBUG: bool = False

    LOG_NAME: str = "dh_app"
    LOG_LEVEL: LogLevelType = LogLevel.INFO
    LOG_FILE_SIZE_MB: int = 10
    LOG_DIRECTORY: str = "logs"
    SAVE_LOG_FILES: bool = True

    class Config:
        """Конфигурация получения настроек"""

        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


base_settings: BaseAppSettings = BaseAppSettings()
