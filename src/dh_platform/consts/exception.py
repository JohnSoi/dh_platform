"""Константы для исключений"""

__author__: str = "Старков Е.П."

from enum import StrEnum


class ErrorCode(StrEnum):
    CUSTOM_ERROR = "custom_error"
    VALIDATION_ERROR = "validation_error"
    NOT_FOUND = "not_found"
    UNAUTHORIZED = "unauthorized"
    FORBIDDEN = "forbidden"
    DATABASE_ERROR = "database_error"
    SERVICE_UNAVAILABLE = "service_unavailable"
