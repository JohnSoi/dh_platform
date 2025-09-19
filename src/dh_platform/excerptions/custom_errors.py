# pylint: disable=too-many-arguments, too-many-positional-arguments
"""Базовые исключения приложения"""

__author__: str = "Старков Е.П."

from fastapi import HTTPException, status

from dh_platform.consts.exception import ErrorCode
from dh_platform.types.common import ExceptionDetailsType


class CustomHTTPException(HTTPException):
    """
    Базовое кастомное исключение

    :ivar code: текстовый код ошибки
    :type code: str
    :ivar details: дополнительные данные об ошибке
    :type details: ExceptionDetailsType
    """

    def __init__(
        self,
        status_code: int,
        detail: str,
        code: str = ErrorCode.CUSTOM_ERROR,
        details: ExceptionDetailsType | None = None,
        headers: dict[str, str] | None = None,
    ):
        """
        Инициализация исключения

        :param status_code: HTTP код ошибки
        :type status_code: int
        :param detail: текст сообщения об ошибке
        :type detail: str
        :param code: текстовый код ошибки
        :type code: str
        :param details: дополнительные данные об ошибке
        :type details: ExceptionDetailsType
        :param headers: заголовки для HTTP ответа
        :type headers: dict[str, str]
        """
        super().__init__(status_code=status_code, detail=detail, headers=headers)
        self.code: str = code
        self.details: ExceptionDetailsType | None = details or {}


class ValidationException(CustomHTTPException):
    """
    Ошибка валидации данных

    .. code-block:: python
    >>> from dh_platform.excerptions import ValidationException
    >>>
    >>> def check_min_length(value: str, name: str, min_length: int = 4) -> None:
    >>>     if len(value) < min_length:
    >>>         raise ValidationException(
    >>>             {"Field": name, "Error": f"Длинна должна быть не меньше {min_length} символов"}
    >>>         )
    """

    def __init__(self, details: ExceptionDetailsType | None = None):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Ошибка валидации данных",
            code=ErrorCode.VALIDATION_ERROR,
            details=details,
        )


class NotFoundException(CustomHTTPException):
    """
    Ресурс не найден

    .. code-block:: python
    >>> from dh_platform.excerptions import
    >>>
    >>> def check_user_exist(user_id: int) -> None:
    >>>     if not User.read(user_id):
    >>>         raise ValidationException({"Error": "Пользователь не найден"})
    """

    def __init__(self, details: ExceptionDetailsType | None = None):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND, detail="Объект не найден", code=ErrorCode.NOT_FOUND, details=details
        )


class UnauthorizedException(CustomHTTPException):
    """
    Не авторизован

    .. code-block:: python
    >>> from multiprocessing.managers import Token    >>> from uuid import UUID
    >>> from dh_platform.excerptions import UnauthorizedException
    >>>
    >>> def check_token_is_active(token: UUID) -> None:
    >>>     if not (token_data := Token.read(token)) or token_data.data_deactivated:
    >>>         raise UnauthorizedException({"Error": "Токен не действителен"})
    """

    def __init__(self, details: ExceptionDetailsType | None = None):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Аутентификация не пройдена",
            code=ErrorCode.UNAUTHORIZED,
            details=details,
        )


class ForbiddenException(CustomHTTPException):
    """
    Доступ запрещен

    .. code-block:: python
    >>> from dh_platform.excerptions import ForbiddenException
    >>>
    >>> def check_write_access(user_id: int, resource_author: int) -> None:
    >>>     if not User.read(user_id).is_admin and not resource_author != user_id:
    >>>         raise ForbiddenException()
    """

    def __init__(self, details: ExceptionDetailsType | None = None):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Доступ к ресурсу запрещен",
            code=ErrorCode.FORBIDDEN,
            details=details,
        )


class DatabaseException(CustomHTTPException):
    """
    Ошибка базы данных

    .. code-block:: python
    >>> from pydantic import PostgresDsn
    >>> from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

    >>> from dh_platform.config import base_settings
    >>> from dh_platform.excerptions import DatabaseException
    >>>
    >>> def connect_db(url: PostgresDsn) -> None:
    >>>     try
    >>>         engine: AsyncEngine = create_async_engine(
    >>>             str(url),
    >>>             echo=base_settings.DB_ECHO,
    >>>             future=True,
    >>>             pool_size=base_settings.DB_POOL_SIZE,
    >>>             max_overflow=base_settings.DB_MAX_OVERFLOW,
    >>>         )
    >>>     except Exception as ex:
    >>>         raise DatabaseException({"Error": str(ex)})
    """

    def __init__(self, details: ExceptionDetailsType | None = None):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка базы данных",
            code=ErrorCode.DATABASE_ERROR,
            details=details,
        )


class ServiceUnavailableException(CustomHTTPException):
    """
    Сервис недоступен

    .. code-block:: python
    >>>     import urllib.request
    >>>
    >>> from dh_platform.excerptions import ServiceUnavailableException
    >>>
    >>> def check_service_unavailable(url: str) -> None:
    >>>     status_code = urllib.request.urlopen(url).getcode()
    >>>     if status_code != status.HTTP_200_OK:
    >>>         raise ServiceUnavailableException({
    >>>             "Url": url,
    >>>             "Error": "Сервис не доступен",
    >>>             "ServiceStatusCode": status_code
    >>>         })
    """

    def __init__(self, details: ExceptionDetailsType | None = None):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Внутренняя ошибка сервиса",
            code=ErrorCode.SERVICE_UNAVAILABLE,
            details=details,
        )
