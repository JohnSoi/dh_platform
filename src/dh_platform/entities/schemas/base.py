"""Модуль базовой схемы данных приложений"""

__author__: str = "Старков Е.П."

from pydantic import BaseModel


class BaseSchema(BaseModel):
    """
    Базовая схема данных приложений

    :cvar ID: идентификатор сущности
    :type ID: int

    .. code-block:: python
    >>> from dh_platform.entities.schemas import BaseSchema
    >>>
    >>>
    >>> # Схема данных пользователя с полями: ID, name, surname
    >>> class UserBaseData(BaseSchema):
    >>>     name: str
    >>>     surname: str
    """

    ID: int
