import secrets
from passlib.context import CryptContext

from dh_platform.consts.security import EMAIL_REGEXP

# Контекст для хеширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверка пароля"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Хеширование пароля"""
    return pwd_context.hash(password)


def generate_random_string(length: int = 32) -> str:
    """Генерация случайной строки"""
    return secrets.token_urlsafe(length)


def generate_secure_filename(original_filename: str) -> str:
    """Генерация безопасного имени файла"""
    import uuid
    from pathlib import Path

    ext = Path(original_filename).suffix
    return f"{uuid.uuid4().hex}{ext}"


# Дополнительные security-утилиты
class SecurityUtils:
    @staticmethod
    def sanitize_input(input_string: str) -> str:
        """Очистка входных данных от потенциально опасных символов"""
        import html
        return html.escape(input_string.strip())

    @staticmethod
    def is_valid_email(email: str) -> bool:
        """Проверка валидности email"""
        import re
        return bool(re.match(EMAIL_REGEXP, email))

    @staticmethod
    def validate_password_strength(password: str) -> dict:
        """Проверка сложности пароля"""
        result = {
            "valid": True,
            "errors": []
        }

        if len(password) < 8:
            result["valid"] = False
            result["errors"].append("Минимальная длинна пароля 8 символов")

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
