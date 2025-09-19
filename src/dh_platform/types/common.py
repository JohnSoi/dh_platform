"""Модуль общих типов"""

__author__: str = "Старков Е.П."

from typing import TypeAlias, Any

# Навигация в системе
NavigationType: TypeAlias = dict[str, int]
# Детали для исключений
ExceptionDetailsType: TypeAlias = dict[str, Any]
