from typing import Tuple
from core.exceptions import AuthenticationError, ValidationError
from database.user_store import UserStore, User
from utils.validators import InputValidator

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
                raise AuthenticationError("Invalid username or password")
            
            if user.password != password:  # In production, use proper password hashing
                raise AuthenticationError("Invalid username or password")
                
            return True, user.name
            
        except ValidationError as e:
            raise AuthenticationError(f"Validation error: {str(e)}")
        except Exception as e:
            raise AuthenticationError(f"Login failed: {str(e)}")

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
                raise AuthenticationError("Username already exists")
            
            # Create new user
            user = User(
                username=username,
                password=password,  # In production, hash the password
                name=name
            )
            
            # Attempt to save user
            if not self.user_store.create_user(user):
                raise AuthenticationError("Failed to create user")
                
            return True
            
        except ValidationError as e:
            raise AuthenticationError(f"Validation error: {str(e)}")
        except Exception as e:
            raise AuthenticationError(f"Registration failed: {str(e)}")
