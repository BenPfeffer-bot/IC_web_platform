# utils/authentication.py

from database.user_store import UserStore, User
from core.exceptions import AuthenticationError, ValidationError
from utils.validators import InputValidator
from typing import Tuple

class AuthenticationService:
    """Handles user authentication"""
    def __init__(self):
        self.user_store = UserStore()
        self.validator = InputValidator()

    def login(self, username: str, password: str) -> Tuple[bool, str]:
        """
        Authenticate user login

        Args:
            username (str): User's username
            password (str): User's password

        Returns:
            Tuple[bool, str]: (success status, user's name if successful)

        Raises:
            AuthenticationError: If validation fails or credentials are invalid
        """
        try:
            # Validate inputs
            username = self.validator.validate_username(username)
            password = self.validator.validate_password(password)

            # Check if user exists and verify password
            user = self.user_store.get_user(username)
            if not user:
                return False, ""

            if user.password != password:  # In production, use proper password hashing
                return False, ""

            return True, user.name

        except ValidationError as e:
            return False, ""
        except Exception as e:
            return False, ""

    def register(self, username: str, password: str, name: str) -> bool:
        """
        Register new user

        Args:
            username (str): Desired username
            password (str): User's password
            name (str): User's full name

        Returns:
            bool: True if registration successful

        Raises:
            AuthenticationError: If validation fails or username already exists
        """
        try:
            # Validate inputs
            username = self.validator.validate_username(username)
            password = self.validator.validate_password(password)
            name = self.validator.validate_name(name)

            # Check if username already exists
            if self.user_store.get_user(username):
                return False

            # Create new user
            user = User(
                username=username,
                password=password,  # In production, hash the password
                name=name
            )

            # Attempt to save user
            if not self.user_store.create_user(user):
                return False

            return True

        except ValidationError as e:
            return False
        except Exception as e:
            return False
