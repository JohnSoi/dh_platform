# pylint: disable=too-few-public-methods, not-callable, unnecessary-ellipsis
"""Миксины с базовыми колонками для таблиц"""

__author__ = "Старков Е.П."

import uuid
from datetime import datetime

from sqlalchemy import DateTime, Integer, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column


class UUIDMixin:
    """
    Миксин для добавления колонки UUID в таблицу сущности

    :cvar UUID: UUID сущности для взаимодействия с другими подсистемами
    :type UUID: UUID

    .. code-block:: python
    >>> from sqlalchemy import String
    >>> from sqlalchemy.orm import Mapped, mapped_column
    >>>
    >>> from dh_platform.entities.models import BaseModel, UUIDMixin
    >>>
    >>>
    >>> # Создание модели пользователя с полями: ID, UUID, name, surname
    >>> class MyModel(BaseModel, UUIDMixin):
    >>>     name: Mapped[str] = mapped_column(String, unique=True, index=True)
    >>>     surname: Mapped[str] = mapped_column(String, unique=True, index=True)
    """

    UUID: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)


class TimestampMixin:
    """
    Миксин для отслеживание времени изменений сущности

    :cvar created_at: дата создания сущности
    :type created_at: datetime
    :cvar updated_at: дата обновления сущности
    :type updated_at: datetime

    .. code-block:: python
    >>> from sqlalchemy import String
    >>> from sqlalchemy.orm import Mapped, mapped_column
    >>>
    >>> from dh_platform.entities.models import BaseModel, TimestampMixin
    >>>
    >>>
    >>> # Создание модели пользователя с полями: ID, created_at, updated_at, name, surname
    >>> class MyModel(BaseModel, TimestampMixin):
    >>>     name: Mapped[str] = mapped_column(String, unique=True, index=True)
    >>>     surname: Mapped[str] = mapped_column(String, unique=True, index=True)
    """

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class SoftDeleteMixin:
    """
    Миксин для отслеживание времени удаления сущности

    :cvar deleted_at: дата удаления сущности
    :type deleted_at: datetime
    :cvar deleted_by: автор удаления сущнсоти
    :type deleted_by: UUID

    .. code-block:: python
    >>> from sqlalchemy import String
    >>> from sqlalchemy.orm import Mapped, mapped_column
    >>>
    >>> from dh_platform.entities.models import BaseModel, SoftDeleteMixin
    >>>
    >>>
    >>> # Создание модели пользователя с полями: ID, deleted_at, deleted_by, name, surname
    >>> class MyModel(BaseModel, SoftDeleteMixin):
    >>>     name: Mapped[str] = mapped_column(String, unique=True, index=True)
    >>>     surname: Mapped[str] = mapped_column(String, unique=True, index=True)
    """

    deleted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    deleted_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)


class ActiveMixin:
    """
    Миксин для отслеживание времени деактивации сущности

    :cvar deactivated_at: дата деактивации сущности
    :type deactivated_at: datetime
    :cvar deactivated_by: автор деактивации сущнсоти
    :type deactivated_by: UUID

    .. code-block:: python
    >>> from sqlalchemy import String
    >>> from sqlalchemy.orm import Mapped, mapped_column
    >>>
    >>> from dh_platform.entities.models import BaseModel, ActiveMixin
    >>>
    >>>
    >>> # Создание модели пользователя с полями: ID, deactivated_at, deactivated_by, name, surname
    >>> class MyModel(BaseModel, ActiveMixin):
    >>>     name: Mapped[str] = mapped_column(String, unique=True, index=True)
    >>>     surname: Mapped[str] = mapped_column(String, unique=True, index=True)
    """

    deactivated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    deactivated_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)


class AuditMixin:
    """
    Миксин для отслеживания автора создания и изменения сущности

    :cvar created_by: автор создания сущности
    :type created_by: UUID
    :cvar updated_by: автор обновления сущности
    :type updated_by: UUID

    .. code-block:: python
    >>> from sqlalchemy import String
    >>> from sqlalchemy.orm import Mapped, mapped_column
    >>>
    >>> from dh_platform.entities.models import BaseModel, AuditMixin
    >>>
    >>>
    >>> # Создание модели пользователя с полями: ID, created_by, updated_by, name, surname
    >>> class MyModel(BaseModel, AuditMixin):
    >>>     name: Mapped[str] = mapped_column(String, unique=True, index=True)
    >>>     surname: Mapped[str] = mapped_column(String, unique=True, index=True)
    """

    created_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    updated_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=True)


class OrderMixin:
    """
    Миксин для поля сортировки сущностей

    :cvar order: значение индекса сортировки сущности
    :type order: int

    .. code-block:: python
    >>> from sqlalchemy import String
    >>> from sqlalchemy.orm import Mapped, mapped_column
    >>>
    >>> from dh_platform.entities.models import BaseModel, OrderMixin
    >>>
    >>>
    >>> # Создание модели пользователя с полями: ID, order, name, surname
    >>> class MyModel(BaseModel, OrderMixin):
    >>>     name: Mapped[str] = mapped_column(String, unique=True, index=True)
    >>>     surname: Mapped[str] = mapped_column(String, unique=True, index=True)
    """

    order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)


class FullEntityMixin(UUIDMixin, TimestampMixin, AuditMixin, SoftDeleteMixin, OrderMixin, ActiveMixin):
    """
    Полный миксин сущностей. Содержит все базовые миксины

    .. code-block:: python
    >>> from sqlalchemy import String
    >>> from sqlalchemy.orm import Mapped, mapped_column
    >>>
    >>> from dh_platform.entities.models import BaseModel, FullEntityMixin
    >>>
    >>>
    >>> # Создание модели пользователя с полями: ID, UUID, created_at, updated_at, deleted_at, created_by, updated_by,
    >>> # deleted_by, order, deactivated_at, deactivated_by, name, surname
    >>> class MyModel(BaseModel, FullEntityMixin):
    >>>     name: Mapped[str] = mapped_column(String, unique=True, index=True)
    >>>     surname: Mapped[str] = mapped_column(String, unique=True, index=True)
    """

    ...


class FullTimeStampMixin(TimestampMixin, SoftDeleteMixin):
    """
    Миксин временных меток сущностей. Содержит миксины врменени создания, обновления, удаления

    .. code-block:: python
    >>> from sqlalchemy import String
    >>> from sqlalchemy.orm import Mapped, mapped_column
    >>>
    >>> from dh_platform.entities.models import BaseModel, FullTimeStampMixin
    >>>
    >>>
    >>> # Создание модели пользователя с полями: ID, created_at, updated_at, deleted_at, deleted_by, name, surname
    >>> class MyModel(BaseModel, FullTimeStampMixin):
    >>>     name: Mapped[str] = mapped_column(String, unique=True, index=True)
    >>>     surname: Mapped[str] = mapped_column(String, unique=True, index=True)
    """

    ...


class BaseEntityMixin(UUIDMixin, FullTimeStampMixin):
    """
    Базовый миксин сущности. Содержит миксины врменени создания, обновления, удаления, а так же UUID самой сущности

    .. code-block:: python
    >>> from sqlalchemy import String
    >>> from sqlalchemy.orm import Mapped, mapped_column
    >>>
    >>> from dh_platform.entities.models import BaseModel, BaseEntityMixin
    >>>
    >>>
    >>> # Создание модели пользователя с полями: ID, UUID, created_at, updated_at, deleted_at, deleted_by, name, surname
    >>> class MyModel(BaseModel, BaseEntityMixin):
    >>>     name: Mapped[str] = mapped_column(String, unique=True, index=True)
    >>>     surname: Mapped[str] = mapped_column(String, unique=True, index=True)
    """

    ...
