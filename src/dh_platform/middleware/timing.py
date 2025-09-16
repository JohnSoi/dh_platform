import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from dh_platform.config import base_settings
from dh_platform.consts.logger import LogLevel


class TimingMiddleware(BaseHTTPMiddleware):
    """Middleware для замера времени выполнения запросов"""

    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.timings = {}

    async def dispatch(self, request: Request, call_next):
        start_time = time.perf_counter()

        # Добавляем timer в state
        request.state.timer = {"start": start_time}

        response = await call_next(request)

        end_time = time.perf_counter()
        execution_time = end_time - start_time

        # Сохраняем timing information
        request.state.timer["end"] = end_time
        request.state.timer["execution_time"] = execution_time

        # Добавляем в headers
        response.headers["X-Process-Time"] = f"{execution_time:.3f}"

        # Логируем медленные запросы
        if execution_time > 1.0 or (base_settings.DEBUG and base_settings.LOG_LEVEL == LogLevel.DEBUG):  # Больше 1 секунды
            from dh_platform.utils import logger
            logger.warning(
                "Slow request detected",
                extra={
                    "method": request.method,
                    "url": str(request.url),
                    "execution_time": f"{execution_time:.3f}s",
                    "threshold": "1.0s"
                }
            )

        return response
