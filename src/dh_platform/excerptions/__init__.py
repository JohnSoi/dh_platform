"""Пакет базовых исключений приложений"""

__author__: str = "Старков Е.П."

from .custom_errors import (ValidationException, NotFoundException, UnauthorizedException,
                            ForbiddenException, DatabaseException, ServiceUnavailableException)
