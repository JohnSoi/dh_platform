"""Модуль класса для работы с подключениями к БД"""

__author__: str = "Старков Е.П."

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from pydantic import PostgresDsn
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from dh_platform.config import base_settings


class DatabaseSessionManager:
    """
    Класс для работы с сессиями подключений к БД

    :ivar _engine: подключение к БД
    :type _engine: AsyncEngine
    :ivar _async_session: менеджер асинхронных сессий
    :type _async_session: async_sessionmaker[AsyncSession]
    """

    def __init__(self, url: PostgresDsn) -> None:
        """
        Инициализация класса работы с сессиями БД

        :param url: адрес для подключения к БД
        :type url: PostgresDsn
        """
        self._engine: AsyncEngine = create_async_engine(
            str(url),
            echo=base_settings.DB_ECHO,
            future=True,
            pool_size=base_settings.DB_POOL_SIZE,
            max_overflow=base_settings.DB_MAX_OVERFLOW,
        )

        self._async_session: async_sessionmaker[AsyncSession] = async_sessionmaker(
            self._engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autoflush=False,
        )

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """
        Получение сессии подключения

        :return: асинхронный генератор сессий
        :rtype: AsyncGenerator[AsyncSession, None]
        """
        session = self._async_session()

        try:
            yield session
            await session.close()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

    async def connection_close(self) -> None:
        """Закрытие подключения к БД"""
        await self._engine.dispose()
