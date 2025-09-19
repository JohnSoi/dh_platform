"""Общие вспомогательные функции"""

__author__ = "Старков Е.П."

import datetime
import json
import re
from datetime import timedelta
from typing import Any

from dh_platform.consts import BASE_SQL_DATE_FORMAT, MAX_NAV_LIMIT
from dh_platform.types import NavigationType

from .private import JSONEncoder


def json_serialize(obj: Any) -> str:
    """
    Сериализация объекта в JSON с поддержкой специальных типов

    :param obj: объект для сериализации
    :type obj: Any
    :return: сериализованный объект в виде строки
    :rtype: str

    .. code-block:: python
    >>> from datetime import datetime
    >>> from dh_platform.utils import json_serialize
    >>>
    >>> print(json_serialize({"a": 1, "b": 2, "c": datetime.now()}))
    """
    return json.dumps(obj, cls=JSONEncoder, ensure_ascii=False)


def to_camel_case(snake_str: str) -> str:
    """
    Конвертация snake_case в camelCase

    :param snake_str: строка в snake_case формате
    :type snake_str: str
    :return: строка в camelCase формате
    :rtype: str

    .. code-block:: python
    >>> from dh_platform.utils import to_camel_case
    >>>
    >>> print(to_camel_case("hello_world")) # helloWorld
    """
    components: list[str] = snake_str.split("_")
    return components[0] + "".join(x.title() for x in components[1:])


def to_snake_case(camel_str: str) -> str:
    """
    Конвертация camelCase в snake_case

    :param camel_str: строка в camelCase формате
    :type camel_str: str
    :return: строка в snake_case формате
    :rtype: str

    .. code-block:: python
    >>> from dh_platform.utils import to_snake_case
    >>>
    >>> print(to_snake_case("helloWorld")) # hello_world
    """
    return re.sub(r"(?<!^)(?=[A-Z])", "_", camel_str).lower()


def deep_update(mapping: dict, *updating_mappings: dict) -> dict:
    """
    Рекурсивное обновление словаря

    :param mapping: словарь для обновления
    :type mapping: dict
    :param updating_mappings: словарь с данными для обновления
    :type updating_mappings: dict
    :return: новый обновленный словарь
    :rtype: dict

    .. code-block:: python
    >>> from dh_platform.utils import deep_update
    >>>
    >>> print(deep_update({"new": {"old": {"old1": 1}}}, {"old1": 2})) # {"new": {"old": {"old1": 2}}}
    """
    result: dict = mapping.copy()

    for updating_mapping in updating_mappings:
        for k, v in updating_mapping.items():
            if k in result and isinstance(result[k], dict) and isinstance(v, dict):
                result[k] = deep_update(result[k], v)
            else:
                result[k] = v

    return result


def get_pagination_params(skip: int = 0, limit: int = 100) -> NavigationType:
    """
    Валидация параметров пагинации

    :param skip: с какой записи нудно начать вычитывание (offset)
    :type skip: int
    :param limit: сколько записей нужно вычитать. Не более MAX_NAV_LIMIT
    :type limit: int
    :return: параметры навигации
    :rtype: NavigationType

    .. code-block:: python
    >>> from dh_platform.utils import get_pagination_params
    >>>
    >>> # будут взяты строки с 10 в количестве 10 штук
    >>> print(get_pagination_params(skip=10, limit=10))
    >>> # будут взяты строки с 100 в количестве 1000 штук (при условии MAX_NAV_LIMIT = 1000)
    >>> print(get_pagination_params(skip=100, limit=10000))
    """
    skip: int = max(0, skip)
    # Ограничение 100 записей на страницу
    limit: int = min(MAX_NAV_LIMIT, max(1, limit))

    return {"skip": skip, "limit": limit}


class DateTimeHelper:
    """Утилиты для работы с датой и временем"""

    @staticmethod
    def get_utc_now() -> datetime:
        """
        Текущее время в UTC

        :return: текущее UTC время
        :rtype: datetime

        .. code-block:: python
        >>> from dh_platform.utils import DateTimeHelper
        >>>
        >>> # datetime.datetime(2025, 9, 17, 3, 39, 0, 938626, tzinfo=datetime.timezone.utc)
        >>> print(DateTimeHelper.get_utc_now())
        """
        return datetime.datetime.now(datetime.UTC)

    @staticmethod
    def format_datetime(dt: datetime, format_str: str = BASE_SQL_DATE_FORMAT) -> str:
        """
        Форматирование datetime в строку. Без параметра format_str форматирует дату для SQL

        :param dt: дата и время
        :type dt: datetime
        :param format_str: формат для преобразования даты
        :type format_str: str
        :return: форматированная строка с датой и временем в зависимости от format_str
        :rtype: str

        .. code-block:: python
        >>> from datetime import datetime
        >>> from dh_platform.utils import DateTimeHelper
        >>>
        >>> # 17.09.2025 08:41:32
        >>> print(DateTimeHelper.format_datetime(dt=datetime.now(), format_str="%d.%m.%Y %H:%M:%S"))
        """
        return dt.strftime(format_str)

    @staticmethod
    def time_ago(dt: datetime) -> str:
        """
        Время в формате 'X время назад'

        :param dt: дата и время
        :type dt: datetime
        :return: человекочитаемая строка срока назад
        :rtype: str

        .. code-block:: python
        >>> from datetime import datetime, date
        >>> from dateutil.relativedelta import relativedelta
        >>> from dh_platform.utils import DateTimeHelper
        >>>
        >>> print(DateTimeHelper.time_ago(dt=datetime.now())) # сейчас
        >>> print(DateTimeHelper.time_ago(dt=date.today() - relativedelta(months=3))) # 3 месяца назад
        """
        now: datetime = DateTimeHelper.get_utc_now()
        diff: timedelta = now - dt

        if diff.days > 365:
            years: int = diff.days // 365
            return f"{years} {'год' if years == 1 else 'года' if years < 5 else 'лет'} назад"
        if diff.days > 30:
            months: int = diff.days // 30
            return f"{months} месяц{'' if months == 1 else 'месяца' if months < 5 else 'месяцев'} назад"
        if diff.days > 0:
            return f"{diff.days} {'день' if diff.days == 1 else 'дня' if diff.days < 5 else 'дней'} назад"
        if diff.seconds > 3600:
            hours: int = diff.seconds // 3600
            return f"{hours} {'час' if diff.days == 1 else 'часа' if diff.days < 5 else 'часов'} назад"
        if diff.seconds > 60:
            minutes: int = diff.seconds // 60
            return f"{minutes} {'минуту' if diff.days == 1 else 'минуты' if diff.days < 5 else 'минут'} назад"

        return "сейчас"
