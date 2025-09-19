"""Типы для функций безопасности"""

__author__: str = "Старков Е.П."

from typing import TypeAlias

# Данные валидации сложности пароля
PasswordStrengthValidationType: TypeAlias = dict[str, list[str] | bool]
