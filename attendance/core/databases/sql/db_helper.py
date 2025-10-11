"""
Модуль для работы с базой данных.
"""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from loguru import logger
from sqlalchemy.exc import SQLAlchemyError

from core.config import settings
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


class DBHelper:
    """
    Класс - помощник для работы с базой данных.
    """

    def __init__(self, url: str, echo: bool = False) -> None:
        """
        Инициализация класса.

        Параметры:
        url: Строка для подключения к базе данных
        echo: Принимает значения True или False

        Если установлен в True, то в консоль будут
        выводиться запросы к базе. По умолчанию False.
        """
        self.engine = create_async_engine(
            url=str(url), echo=echo
        )  # Двигатель для работы с асинхронной базой данных
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autocommit=False,
            expire_on_commit=False,
        )  # Фабрика сессий для работы с асинхронной базой данных

    async def dispose(self) -> None:
        """
        Освобождает ресурсы, связанные с базой данных.
        """
        await self.engine.dispose()
        logger.success("Соединение с базой данных закрыто.")

    @asynccontextmanager
    async def get_async_session_without_commit(
        self,
    ) -> AsyncGenerator[AsyncSession, None]:
        """
        Возвращает сессию для асинхронной работы с базой данных.
        """
        async with self.session_factory() as session:  # type: AsyncSession
            yield session

    @asynccontextmanager
    async def get_async_session_with_commit(
        self,
    ) -> AsyncGenerator[AsyncSession, None]:
        """
        Возвращает сессию для асинхронной работы с базой данных и делает коммит.
        """
        async with self.session_factory() as session:  # type: AsyncSession
            try:
                yield session
            except SQLAlchemyError:
                pass
            else:
                await session.commit()


db_helper = DBHelper(
    url=settings.db.url,
    echo=settings.db.echo,
)
