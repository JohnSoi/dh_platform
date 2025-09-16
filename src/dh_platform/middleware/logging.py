import time
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from dh_platform.utils import logger


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware для логирования запросов и ответов"""

    async def dispatch(self, request: Request, call_next):
        # Логирование входящего запроса
        start_time = time.time()

        logger.info(
            "Request started",
            extra={
                "method": request.method,
                "url": str(request.url),
                "client": request.client.host if request.client else "unknown",
                "user_agent": request.headers.get("user-agent", ""),
            }
        )

        try:
            response = await call_next(request)
        except Exception as e:
            # Логирование ошибок
            logger.error(
                "Request failed",
                extra={
                    "method": request.method,
                    "url": str(request.url),
                    "error": str(e),
                    "execution_time": time.time() - start_time
                },
                exc_info=True
            )
            raise

        # Логирование успешного ответа
        execution_time = time.time() - start_time

        logger.info(
            "Request completed",
            extra={
                "method": request.method,
                "url": str(request.url),
                "status_code": response.status_code,
                "execution_time": f"{execution_time:.3f}s",
            }
        )

        # Добавляем время выполнения в headers
        response.headers["X-Execution-Time"] = f"{execution_time:.3f}"

        return response


class RequestIDMiddleware(BaseHTTPMiddleware):
    """Middleware для добавления Request ID"""

    async def dispatch(self, request: Request, call_next):
        import uuid
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))

        # Добавляем request_id в state
        request.state.request_id = request_id

        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id

        return response
