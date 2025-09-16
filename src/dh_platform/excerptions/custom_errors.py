from fastapi import HTTPException, status
from typing import Any, Dict, Optional


class CustomHTTPException(HTTPException):
    """Базовое кастомное исключение"""

    def __init__(
            self,
            status_code: int,
            detail: str,
            code: str = "custom_error",
            details: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, str]] = None
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)
        self.code = code
        self.details = details or {}


class ValidationException(CustomHTTPException):
    """Ошибка валидации данных"""

    def __init__(
            self,
            detail: str = "Validation failed",
            details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail,
            code="validation_error",
            details=details
        )


class NotFoundException(CustomHTTPException):
    """Ресурс не найден"""

    def __init__(
            self,
            resource: str = "Resource",
            details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{resource} not found",
            code="not_found",
            details=details
        )


class UnauthorizedException(CustomHTTPException):
    """Не авторизован"""

    def __init__(
            self,
            detail: str = "Not authenticated",
            details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            code="unauthorized",
            details=details
        )


class ForbiddenException(CustomHTTPException):
    """Доступ запрещен"""

    def __init__(
            self,
            detail: str = "Access forbidden",
            details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
            code="forbidden",
            details=details
        )


class DatabaseException(CustomHTTPException):
    """Ошибка базы данных"""

    def __init__(
            self,
            detail: str = "Database error occurred",
            details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
            code="database_error",
            details=details
        )


class ServiceUnavailableException(CustomHTTPException):
    """Сервис недоступен"""

    def __init__(
            self,
            detail: str = "Service temporarily unavailable",
            details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=detail,
            code="service_unavailable",
            details=details
        )
