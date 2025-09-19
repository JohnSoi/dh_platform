"""Модуль для типов логирования в системе"""

__author__: str = "Старков Е.П."

from typing import Literal, TypeAlias

from dh_platform.consts.logger import LogLevel

# Доступные уровни логирования
LogLevelType: TypeAlias = Literal[LogLevel.INFO, LogLevel.DEBUG, LogLevel.WARN, LogLevel.ERROR]
