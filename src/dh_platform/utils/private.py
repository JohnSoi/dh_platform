"""Приватные функции. Недоступны для использования вне данного пакета"""


__author__ = "Старков Е.П."

import datetime
from decimal import Decimal
from json import JSONEncoder as BaseJSONEncoder
from typing import Any
from uuid import UUID

from dh_platform.consts import ENCODING


class JSONEncoder(BaseJSONEncoder):
    """Кастомный JSON encoder для обработки специальных типов"""

    def default(self, o: Any) -> Any:
        """Основной обработчик энкодера"""
        if isinstance(o, (datetime.datetime, datetime.date)):
            return o.isoformat()

        if isinstance(o, Decimal):
            return float(o)

        if isinstance(o, UUID):
            return str(o)

        if isinstance(o, bytes):
            return o.decode(ENCODING)

        if hasattr(o, "to_dict"):
            return o.to_dict()

        return super().default(o)
