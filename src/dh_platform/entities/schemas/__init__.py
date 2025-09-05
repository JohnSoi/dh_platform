"""Пакет базовых схем данных"""

__author__: str = "Старков Е.П."

from .base import BaseSchema
from .mixins import (UUIDSchemaMixin, TimestampSchemaMixin, SoftDeleteSchemaMixin, ActiveSchemaMixin, AuditSchemaMixin,
                     OrderSchemaMixin, FullTimeStampMixin, FullEntitySchemaMixin, BaseEntitySchemaMixin)
