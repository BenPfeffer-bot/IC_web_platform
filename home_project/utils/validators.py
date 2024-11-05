# utils/validators.py
from typing import Optional
from core.exceptions import ValidationError

class InputValidator:
    def validate_username(self, username: str) -> str:
        if not username or len(username) < 3:
            raise ValidationError("Username must be at least 3 characters long")
        return username.strip()

    def validate_password(self, password: str) -> str:
        if not password or len(password) < 6:
            raise ValidationError("Password must be at least 6 characters long")
        return password

    def validate_name(self, name: str) -> str:
        if not name or len(name) < 2:
            raise ValidationError("Name must be at least 2 characters long")
        return name.strip()
