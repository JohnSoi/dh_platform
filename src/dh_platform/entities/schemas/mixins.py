# pylint: disable=too-few-public-methods, unnecessary-ellipsis
"""Базовые миксины полей схем данных"""

__author__: str = "Старков Е.П."

from datetime import datetime
from uuid import UUID


class UUIDSchemaMixin:
    """
    Миксин схемы данных для поля UUID сущности

    :cvar UUID: идентификатор сущности
    :type UUID: UUID

    .. code-block:: python
    >>> from dh_platform.entities.schemas import BaseSchema, UUIDSchemaMixin
    >>>
    >>>
    >>> # Схема данных пользователя с полями: ID, UUID, name, surname
    >>> class UserBaseData(BaseSchema, UUIDSchemaMixin):
    >>>     name: str
    >>>     surname: str
    """

    UUID: UUID


class TimestampSchemaMixin:
    """
    Миксин схемы данных для полей временных меток создания и обновления сущности

    :cvar created_at: дата создания сущности
    :type created_at: datetime
    :cvar updated_at: дата обновления сущности
    :type updated_at: datetime

    .. code-block:: python
    >>> from dh_platform.entities.schemas import BaseSchema, TimestampSchemaMixin
    >>>
    >>>
    >>> # Схема данных пользователя с полями: ID, created_at, updated_at, name, surname
    >>> class UserBaseData(BaseSchema, TimestampSchemaMixin):
    >>>     name: str
    >>>     surname: str
    """

    created_at: datetime
    updated_at: datetime


class SoftDeleteSchemaMixin:
    """
    Миксин схемы данных для полей даты и автора удаления сущности

    :cvar deleted_at: дата удаления сущности
    :type deleted_at: datetime
    :cvar deleted_by: автор удаления сущности
    :type deleted_by: UUID

    .. code-block:: python
    >>> from dh_platform.entities.schemas import BaseSchema, SoftDeleteSchemaMixin
    >>>
    >>>
    >>> # Схема данных пользователя с полями: ID, deleted_at, deleted_by, name, surname
    >>> class UserBaseData(BaseSchema, SoftDeleteSchemaMixin):
    >>>     name: str
    >>>     surname: str
    """

    deleted_at: datetime
    deleted_by: UUID


class AuditSchemaMixin:
    """
    Миксин схемы данных для полей авторов создания и обновления сущностей

    :cvar created_by: автор создания сущности
    :type created_by: UUID
    :cvar updated_by: автор обновления сущности
    :type updated_by: UUID

    .. code-block:: python
    >>> from dh_platform.entities.schemas import BaseSchema, AuditSchemaMixin
    >>>
    >>>
    >>> # Схема данных пользователя с полями: ID, created_by, updated_by, name, surname
    >>> class UserBaseData(BaseSchema, AuditSchemaMixin):
    >>>     name: str
    >>>     surname: str
    """

    created_by: UUID
    updated_by: UUID


class ActiveSchemaMixin:
    """
    Миксин схемы данных для полей даты и автора деактивации сущности

    :cvar deactivated_at: дата деактивации сущности
    :type deactivated_at: datetime
    :cvar deactivated_by: автор деактивации сущности
    :type deactivated_by: UUID

    .. code-block:: python
    >>> from dh_platform.entities.schemas import BaseSchema, ActiveSchemaMixin
    >>>
    >>>
    >>> # Схема данных пользователя с полями: ID, deactivated_at, deactivated_by, name, surname
    >>> class UserBaseData(BaseSchema, ActiveSchemaMixin):
    >>>     name: str
    >>>     surname: str
    """

    deactivated_at: datetime
    deactivated_by: UUID


class OrderSchemaMixin:
    """
    Миксин схемы данных для поля сортировки сущности

    :cvar order: индекс сортировки сущности
    :type order: int

    .. code-block:: python
    >>> from dh_platform.entities.schemas import BaseSchema, OrderSchemaMixin
    >>>
    >>>
    >>> # Схема данных пользователя с полями: ID, order, name, surname
    >>> class UserBaseData(BaseSchema, OrderSchemaMixin):
    >>>     name: str
    >>>     surname: str
    """

    order: int


class FullEntitySchemaMixin(
    UUIDSchemaMixin,
    TimestampSchemaMixin,
    SoftDeleteSchemaMixin,
    AuditSchemaMixin,
    ActiveSchemaMixin,
    OrderSchemaMixin,
):
    """
    Полный миксин схемы данных. Содержит все базовы миксины

    .. code-block:: python
    >>> from dh_platform.entities.schemas import BaseSchema, FullEntitySchemaMixin
    >>>
    >>>
    >>> # Схема данных пользователя с полями: ID, UUID, created_at, updated_at, deleted_at, created_by, updated_by,
    >>> # deleted_by, order, deactivated_at, deactivated_by, name, surname
    >>> class UserBaseData(BaseSchema, FullEntitySchemaMixin):
    >>>     name: str
    >>>     surname: str
    """

    ...


class FullTimeStampMixin(TimestampSchemaMixin, SoftDeleteSchemaMixin):
    """
    Миксин временных меток сущностей. Содержит миксины врменени создания, обновления, удаления

    .. code-block:: python
    >>> from dh_platform.entities.schemas import BaseSchema, FullTimeStampMixin
    >>>
    >>>
    >>> # Схема данных пользователя с полями: ID, created_at, updated_at, deleted_at, deleted_by, name, surname
    >>> class UserBaseData(BaseSchema, FullTimeStampMixin):
    >>>     name: str
    >>>     surname: str
    """

    ...


class BaseEntitySchemaMixin(FullEntitySchemaMixin, UUIDSchemaMixin):
    """
    Базовый миксин сущности. Содержит миксины врменени создания, обновления, удаления, а так же UUID самой сущности

    .. code-block:: python
    >>> from dh_platform.entities.schemas import BaseSchema, FullEntitySchemaMixin
    >>>
    >>>
    >>> # Схема данных пользователя с полями: ID, UUID, created_at, updated_at, deleted_at, deleted_by, name, surname
    >>> class UserBaseData(BaseSchema, FullEntitySchemaMixin):
    >>>     name: str
    >>>     surname: str
    """

    ...
