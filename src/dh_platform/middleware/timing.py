# pylint: disable=too-few-public-methods
"""Модуль для middleware для отслеживания времени выполнения и логирования медленных запросов"""

__author__: str = "Старков Е.П."

import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from starlette.types import ASGIApp

from dh_platform.config import base_settings
from dh_platform.consts.logger import LogLevel
from dh_platform.utils import logger


class TimingMiddleware(BaseHTTPMiddleware):
    """
    Middleware для замера времени выполнения запросов

    .. code-block:: python
    >>> from fastapi import FastAPI
    >>> from dh_platform.middleware import TimingMiddleware
    >>>
    >>> app: FastAPI = FastAPI()
    >>> app.add_middleware(TimingMiddleware)
    """

    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next) -> Response:
        """
        Старт обработки запроса

        :param request: запрос
        :type request: Request
        :param call_next: функция обработки запроса
        :return: результат запроса
        :rtype: Response
        """
        start_time: float = time.perf_counter()

        # Добавляем timer в state
        request.state.timer = {"start": start_time}

        response: Response = await call_next(request)

        end_time: float = time.perf_counter()
        execution_time: float = end_time - start_time

        # Сохраняем timing information
        request.state.timer["end"] = end_time
        request.state.timer["execution_time"] = execution_time

        # Добавляем в headers
        response.headers["X-Process-Time"] = f"{execution_time:.3f}"

        # Логируем медленные запросы
        if execution_time > 1.0 or (
            base_settings.DEBUG and base_settings.LOG_LEVEL == LogLevel.DEBUG
        ):  # Больше 1 секунды
            logger.warning(
                "Обнаружен медленный запрос",
                extra={
                    "method": request.method,
                    "url": str(request.url),
                    "execution_time": f"{execution_time:.3f}s",
                    "threshold": "1.0s",
                },
            )

        return response
