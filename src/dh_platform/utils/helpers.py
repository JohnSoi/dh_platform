import datetime
import json
from decimal import Decimal
from typing import Any, Dict
from uuid import UUID

from dh_platform.consts import BASE_SQL_DATE_FORMAT, ENCODING


class JSONEncoder(json.JSONEncoder):
    """Кастомный JSON encoder для обработки специальных типов"""

    def default(self, obj: Any) -> Any:
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        if isinstance(obj, datetime.date):
            return obj.isoformat()
        if isinstance(obj, Decimal):
            return float(obj)
        if isinstance(obj, UUID):
            return str(obj)
        if isinstance(obj, bytes):
            return obj.decode(ENCODING)
        if hasattr(obj, "to_dict"):
            return obj.to_dict()
        return super().default(obj)


def json_serialize(obj: Any) -> str:
    """Сериализация объекта в JSON с поддержкой специальных типов"""
    return json.dumps(obj, cls=JSONEncoder, ensure_ascii=False)


def to_camel_case(snake_str: str) -> str:
    """Конвертация snake_case в camelCase"""
    components = snake_str.split("_")
    return components[0] + "".join(x.title() for x in components[1:])


def to_snake_case(camel_str: str) -> str:
    """Конвертация camelCase в snake_case"""
    import re

    return re.sub(r"(?<!^)(?=[A-Z])", "_", camel_str).lower()


def deep_update(mapping: Dict, *updating_mappings: Dict) -> Dict:
    """Рекурсивное обновление словаря"""
    result = mapping.copy()
    for updating_mapping in updating_mappings:
        for k, v in updating_mapping.items():
            if k in result and isinstance(result[k], dict) and isinstance(v, dict):
                result[k] = deep_update(result[k], v)
            else:
                result[k] = v
    return result


def get_pagination_params(skip: int = 0, limit: int = 100) -> dict:
    """Валидация параметров пагинации"""
    skip = max(0, skip)
    limit = min(100, max(1, limit))  # Ограничение 100 записей на страницу
    return {"skip": skip, "limit": limit}


class DateTimeHelper:
    """Утилиты для работы с датой и временем"""

    @staticmethod
    def get_utc_now() -> datetime:
        """Текущее время в UTC"""
        return datetime.datetime.now(datetime.UTC)

    @staticmethod
    def format_datetime(dt: datetime, format_str: str = BASE_SQL_DATE_FORMAT) -> str:
        """Форматирование datetime в строку"""
        return dt.strftime(format_str)

    @staticmethod
    def time_ago(dt: datetime) -> str:
        """Время в формате 'X time ago'"""
        now = DateTimeHelper.get_utc_now()
        diff = now - dt

        if diff.days > 365:
            years = diff.days // 365
            return f"{years} {'год' if years == 1 else 'года' if years < 5 else 'лет'} назад"
        if diff.days > 30:
            months = diff.days // 30
            return f"{months} месяц{'' if months == 1 else 'месяца' if months < 5 else 'месяцев'} назад"
        if diff.days > 0:
            return f"{diff.days} {'день' if diff.days == 1 else 'дня' if diff.days < 5 else 'дней'} назад"
        if diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"{hours} {'час' if diff.days == 1 else 'часа' if diff.days < 5 else 'часов'} назад"
        if diff.seconds > 60:
            minutes = diff.seconds // 60
            return f"{minutes} {'минуту' if diff.days == 1 else 'минуты' if diff.days < 5 else 'минут'} назад"

        return "сейчас"
