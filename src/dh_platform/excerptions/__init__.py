"""Пакет базовых исключений приложений"""

__author__: str = "Старков Е.П."

from .custom_errors import (
    DatabaseException,
    ForbiddenException,
    NotFoundException,
    ServiceUnavailableException,
    UnauthorizedException,
    ValidationException,
)
