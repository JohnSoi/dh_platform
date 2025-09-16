from enum import StrEnum

FILE_SIZE_DELIMITER: int = 1024

class LogLevel(StrEnum):
    INFO = "INFO"
    DEBUG = "DEBUG"
    WARN = "WARN"
    ERROR = "ERROR"
