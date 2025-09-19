# pylint: disable=too-few-public-methods
"""Модуль middleware для логирования запросов"""

__author__: str = "Старков Е.П."

import time
import uuid

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from dh_platform.utils import logger


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware для логирования запросов и ответов

    .. code-block:: python
    >>> from fastapi import FastAPI
    >>> from dh_platform.middleware import LoggingMiddleware
    >>>
    >>> app: FastAPI = FastAPI()
    >>> app.add_middleware(LoggingMiddleware)
    """

    async def dispatch(self, request: Request, call_next) -> Response:
        """
        Старт обработки запроса

        :param request: запрос
        :type request: Request
        :param call_next: функция обработки запроса
        :return: результат запроса
        :rtype: Response
        """
        # Логирование входящего запроса
        start_time: float = time.time()

        logger.info(
            "Старт запроса",
            extra={
                "method": request.method,
                "url": str(request.url),
                "client": request.client.host if request.client else "Неизвестный",
                "user_agent": request.headers.get("user-agent", ""),
            },
        )

        try:
            response: Response = await call_next(request)
        except Exception as e:
            # Логирование ошибок
            logger.error(
                "Ошибка запроса",
                extra={
                    "method": request.method,
                    "url": str(request.url),
                    "error": str(e),
                    "execution_time": time.time() - start_time,
                },
                exc_info=True,
            )
            raise

        # Логирование успешного ответа
        execution_time: float = time.time() - start_time

        logger.info(
            "Запрос завершен",
            extra={
                "method": request.method,
                "url": str(request.url),
                "status_code": response.status_code,
                "execution_time": f"{execution_time:.3f}s",
            },
        )

        # Добавляем время выполнения в headers
        response.headers["X-Execution-Time"] = f"{execution_time:.3f}"

        return response


class RequestIDMiddleware(BaseHTTPMiddleware):
    """
    Middleware для добавления Request ID

    .. code-block:: python
    >>> from fastapi import FastAPI
    >>> from dh_platform.middleware import LoggingMiddleware
    >>>
    >>> app: FastAPI = FastAPI()
    >>> app.add_middleware(RequestIDMiddleware)
    """

    async def dispatch(self, request: Request, call_next):
        """
        Старт обработки запроса

        :param request: запрос
        :type request: Request
        :param call_next: функция обработки запроса
        :return: результат запроса
        :rtype: Response
        """
        request_id: str = request.headers.get("X-Request-ID", str(uuid.uuid4()))

        # Добавляем request_id в state
        request.state.request_id = request_id

        response: Response = await call_next(request)
        response.headers["X-Request-ID"] = request_id

        return response
