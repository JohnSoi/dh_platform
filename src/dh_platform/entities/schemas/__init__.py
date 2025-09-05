"""Пакет базовых схем данных"""

__author__: str = "Старков Е.П."

from .base import BaseSchema
from .mixins import (
    ActiveSchemaMixin,
    AuditSchemaMixin,
    BaseEntitySchemaMixin,
    FullEntitySchemaMixin,
    FullTimeStampMixin,
    OrderSchemaMixin,
    SoftDeleteSchemaMixin,
    TimestampSchemaMixin,
    UUIDSchemaMixin,
)
