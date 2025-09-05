"""Базовая модель сущностей"""

__author__: str = "Старков Е.П."

from sqlalchemy import Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class BaseModel(DeclarativeBase):
    """
    Базовая модель для всех сущностей приложений

    :cvar ID: идентификатор сущности
    :type ID: int

    .. code-block:: python
    >>> from sqlalchemy import String
    >>> from sqlalchemy.orm import Mapped, mapped_column
    >>>
    >>> from dh_platform.entities.models import BaseModel
    >>>
    >>>
    >>> # Создание модели пользователя с полями: ID, name, surname
    >>> class MyModel(BaseModel):
    >>>     name: Mapped[str] = mapped_column(String, unique=True, index=True)
    >>>     surname: Mapped[str] = mapped_column(String, unique=True, index=True)
    """
    __abstract__ = True

    ID: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        auto_increment=True,
        index=True,
        nullable=False,
        unique=True
    )
