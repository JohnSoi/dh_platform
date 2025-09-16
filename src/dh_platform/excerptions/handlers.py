from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from dh_platform.utils import logger
from .custom_errors import (
    CustomHTTPException,
    ValidationException,
    NotFoundException,
    UnauthorizedException,
    ForbiddenException
)


def setup_exception_handlers(app: FastAPI):
    """Настройка обработчиков исключений"""

    @app.exception_handler(CustomHTTPException)
    async def custom_http_exception_handler(request: Request, exc: CustomHTTPException):
        """Обработчик кастомных HTTP исключений"""
        logger.warning(
            "Custom HTTP exception",
            extra={
                "status_code": exc.status_code,
                "detail": exc.detail,
                "url": str(request.url),
            }
        )

        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "code": exc.code,
                    "message": exc.detail,
                    "details": exc.details
                }
            },
            headers=exc.headers
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        """Обработчик стандартных HTTP исключений"""
        logger.warning(
            "HTTP exception",
            extra={
                "status_code": exc.status_code,
                "detail": exc.detail,
                "url": str(request.url),
            }
        )

        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "code": "http_error",
                    "message": exc.detail
                }
            }
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """Обработчик ошибок валидации"""
        errors = []
        for error in exc.errors():
            errors.append({
                "field": " -> ".join(str(loc) for loc in error["loc"]),
                "message": error["msg"],
                "type": error["type"]
            })

        logger.warning(
            "Validation error",
            extra={
                "errors": errors,
                "url": str(request.url),
            }
        )

        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error": {
                    "code": "validation_error",
                    "message": "Validation failed",
                    "details": errors
                }
            }
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        """Глобальный обработчик исключений"""
        logger.error(
            "Unhandled exception",
            extra={
                "error": str(exc),
                "url": str(request.url),
                "method": request.method,
            },
            exc_info=True
        )

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": {
                    "code": "internal_error",
                    "message": "Internal server error"
                }
            }
        )
