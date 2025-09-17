"""Модуль зависимостей для работы с БД"""

__author__: str = "Старков Е.П."

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from dh_platform.config import base_settings
from dh_platform.source.database.session_manager import DatabaseSessionManager

session_manager: DatabaseSessionManager = DatabaseSessionManager(base_settings.DATABASE_URL)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency для получения асинхронной сессии БД

    :return: генератор асинхронной сессии подключения к БД

    .. code-block:: python
    >>> from dh_platform.source.database import get_db
    >>>
    >>> async def endpoint(db: AsyncSession = Depends(get_db)):
    >>>     ...
    """
    async with session_manager.get_session() as session:
        yield session
