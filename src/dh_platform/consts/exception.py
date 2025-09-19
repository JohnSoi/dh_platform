"""Константы для исключений"""

__author__: str = "Старков Е.П."

from enum import StrEnum


class ErrorCode(StrEnum):
    """
    Текстовые коды ошибок

    :cvar CUSTOM_ERROR: кастомное исключение в приложении
    :cvar VALIDATION_ERROR: ошибка валидации данных
    :cvar NOT_FOUND: ошибка ненайденного ресурса
    :cvar UNAUTHORIZED: ошибка аутентификации в приложении
    :cvar FORBIDDEN: ошибка отсутствия доступа
    :cvar DATABASE_ERROR: ошибка при работе с базой данных
    :cvar SERVICE_UNAVAILABLE: ошибка недоступности сервиса
    """

    CUSTOM_ERROR = "custom_error"
    VALIDATION_ERROR = "validation_error"
    NOT_FOUND = "not_found"
    UNAUTHORIZED = "unauthorized"
    FORBIDDEN = "forbidden"
    DATABASE_ERROR = "database_error"
    SERVICE_UNAVAILABLE = "service_unavailable"
