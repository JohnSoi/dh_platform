from typing import Literal, TypeAlias

from dh_platform.consts.logger import LogLevel

LogLevelType: TypeAlias = Literal[LogLevel.INFO, LogLevel.DEBUG, LogLevel.WARN, LogLevel.ERROR]
