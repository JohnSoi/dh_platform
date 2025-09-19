"""Вспомогательные функции для обеспечения защиты"""

__author__: str = "Старков Е.П."

import html
import re
import secrets
import uuid
from pathlib import Path

from passlib.context import CryptContext

from dh_platform.consts.security import EMAIL_REGEXP, MIN_PASSWORD_LENGTH
from dh_platform.types import PasswordStrengthValidationType

# Контекст для хеширования паролей
pwd_context: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Проверка пароля на совпадение с кешем

    :param plain_password: пароль для проверки
    :type plain_password: str
    :param hashed_password: хеш пароля из БД
    :type hashed_password: str
    :return: совпадение паролей
    :rtype: bool

    .. code-block:: python
    >>> from dh_platform.utils import verify_password

    >>> user: User = User.get(1)
    >>> hashed_password: str = user.password
    >>> input_password: str = "123"

    >>> print(verify_password(input_password, hashed_password)) # выдаст результат совпадения
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Хеширование пароля

    :param password: текст пароля для хеширования
    :type password: str
    :return: хеш пароля
    :rtype: str

    .. code-block:: python
    >>> from dh_platform.utils import get_password_hash
    >>> print(get_password_hash("1234")) # хеш пароля
    """
    return pwd_context.hash(password)


def generate_random_string(length: int = 32) -> str:
    """
    Генерация случайной строки

    :param length: длинна генерируемой строки
    :type length: int
    :return: случайная строка
    :rtype: str

    .. code-block:: python
    >>> from dh_platform.utils import generate_random_string
    >>> print(generate_random_string()) # случайная строка в 32 символа
    """
    return secrets.token_urlsafe(length)


def generate_secure_filename(original_filename: str) -> str:
    """
    Генерация безопасного имени файла

    :param original_filename: оригинальное имя файла
    :type original_filename: str
    :return: безопасное имя файла для сохранения
    :rtype: str

    .. code-block:: python
    >>> from dh_platform.utils import generate_secure_filename
    >>> print(generate_secure_filename("text.txt")) # название в виде UUID для сохранения
    """
    ext: str = Path(original_filename).suffix
    return f"{uuid.uuid4().hex}{ext}"


class SecurityUtils:
    """Дополнительные security-утилиты"""

    @staticmethod
    def sanitize_input(input_string: str) -> str:
        """
        Очистка входных данных от потенциально опасных символов

        :param input_string: входная строка с небезопасным текстом
        :type input_string: str
        :return: очищенная для HTML строка
        :rtype: str

        .. code-block:: python
        >>> from dh_platform.utils import SecurityUtils
        >>>
        >>> #&lt;script&gt;alert(&#x27;!!!!&#x27;)&lt;/script&gt;
        >>> print(SecurityUtils.sanitize_input("<script>alert('!!!!')</script>"))
        """
        return html.escape(input_string.strip())

    @staticmethod
    def is_valid_email(email: str) -> bool:
        """
        Проверка валидности email

        :param email: введенный email
        :type email: str
        :return: корректный адрес электронной почты
        :rtype: bool

        .. code-block:: python
        >>> from dh_platform.utils import SecurityUtils
        >>>
        >>> print(SecurityUtils.is_valid_email("test@tes.ru")) # True
        >>> print(SecurityUtils.is_valid_email("tes.ru")) # False
        """
        return bool(re.match(EMAIL_REGEXP, email))

    @staticmethod
    def validate_password_strength(password: str) -> PasswordStrengthValidationType:
        """
        Проверка сложности пароля

        :param password: введенный пароль
        :type password: str
        :return: словарь с данными о валидации
        :rtype: PasswordStrengthValidationType

        .. code-block:: python
        >>> from dh_platform.utils import SecurityUtils
        >>> print(SecurityUtils.validate_password_strength("1234")) # Длинна не MIN_PASSWORD_LENGTH символов
        >>> print(SecurityUtils.validate_password_strength("1234abc")) # Нет заглавных
        >>> print(SecurityUtils.validate_password_strength("aBc")) # Нет цифр
        >>> print(SecurityUtils.validate_password_strength("1234aBc")) # OK
        """
        result: PasswordStrengthValidationType = {"valid": True, "errors": []}

        if len(password) < MIN_PASSWORD_LENGTH:
            result["valid"] = False
            result["errors"].append(f"Минимальная длинна пароля {MIN_PASSWORD_LENGTH} символов")

        if not any(char.isdigit() for char in password):
            result["valid"] = False
            result["errors"].append("Пароль должен содержать хотя бы 1 цифру")

        if not any(char.isupper() for char in password):
            result["valid"] = False
            result["errors"].append("Пароль должен содержать хотя бы один заглавный символ")

        if not any(char.islower() for char in password):
            result["valid"] = False
            result["errors"].append("Пароль должен содержать хотя бы один строчный символ")

        return result
