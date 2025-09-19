"""Пакет промежуточного ПО"""

__author__: str = "Старков Е.П."

from fastapi import FastAPI

from .logging import LoggingMiddleware, RequestIDMiddleware
from .timing import TimingMiddleware


def setup_base_middleware(app: FastAPI) -> None:
    """
    Устанавливает базовые middleware для приложения

    :param app: экземпляр приложения
    :type app: FastAPI

    .. code-block:: python
    >>> from fastapi import FastAPI
    >>> from dh_platform.middleware import setup_base_middleware
    >>>
    >>> app_inst: FastAPI = FastAPI()
    >>> setup_base_middleware(app_inst)
    """
    app.add_middleware(LoggingMiddleware)
    app.add_middleware(RequestIDMiddleware)
    app.add_middleware(TimingMiddleware)
