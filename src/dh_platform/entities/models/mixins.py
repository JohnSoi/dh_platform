"""Миксины с базовыми колонками для таблиц"""

__author__ = "Старков Е.П."

import uuid
from datetime import datetime

from sqlalchemy import DateTime, func, Integer
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID


class UUIDMixin:
    UUID: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
        unique=True,
        nullable=False
    )


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )


class SoftDeleteMixin:
    deleted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )


class AuditMixin:
    created_by: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False
    )
    updated_by: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=True
    )


class OrderMixin:
    order: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0
    )


class FullEntityMixin(UUIDMixin, TimestampMixin, AuditMixin, SoftDeleteMixin, OrderMixin):
    ...


class FullTimeStampMixin(TimestampMixin, SoftDeleteMixin):
    ...


class BaseEntityMixin(UUIDMixin, FullTimeStampMixin):
    ...