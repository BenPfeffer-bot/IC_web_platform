# database/user_store.py

import json
from typing import Dict, Optional
from dataclasses import dataclass, asdict
from config.settings import settings
from core.exceptions import DatabaseError
import logging

@dataclass
class User:
    """User data model"""
    username: str
    name: str
    password: str  # In a real app, this would be hashed

    def to_dict(self) -> Dict:
        """Convert user object to dictionary"""
        try:
            return asdict(self)
        except Exception as e:
            logging.error(f"Error converting user to dict: {str(e)}")
            raise DatabaseError("Failed to convert user data")

class UserStore:
    """Handles user data storage operations"""
    def __init__(self):
        self.file_path = settings.USERS_FILE
        self._ensure_database_directory()

    def _ensure_database_directory(self) -> None:
        """Ensure database directory exists"""
        try:
            settings.DATABASE_DIR.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            logging.error(f"Failed to create database directory: {str(e)}")
            raise DatabaseError("Could not initialize database directory")

    def _read_users(self) -> Dict:
        """
        Read users from JSON file

        Returns:
            Dict: Dictionary of users

        Raises:
            DatabaseError: If file operations fail
        """
        try:
            if not self.file_path.exists():
                return {}
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if not isinstance(data, dict):
                    raise DatabaseError("Invalid data format in users file")
                return data
        except json.JSONDecodeError as e:
            logging.error(f"JSON decode error reading users file: {str(e)}")
            raise DatabaseError("Invalid JSON in users file")
        except Exception as e:
            logging.error(f"Error reading users file: {str(e)}")
            raise DatabaseError(f"Failed to read users data: {str(e)}")

    def _write_users(self, users: Dict) -> None:
        """
        Write users to JSON file

        Args:
            users: Dictionary of users to write

        Raises:
            DatabaseError: If file operations fail
        """
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(users, f, indent=2, ensure_ascii=False)
        except (IOError, OSError) as e:
            logging.error(f"IO error writing users file: {str(e)}")
            raise DatabaseError("Failed to write to users file")
        except Exception as e:
            logging.error(f"Unexpected error writing users file: {str(e)}")
            raise DatabaseError(f"Failed to save users data: {str(e)}")

    def get_user(self, username: str) -> Optional[User]:
        """
        Get user by username

        Args:
            username: Username to look up

        Returns:
            Optional[User]: User object if found, None otherwise

        Raises:
            DatabaseError: If database operations fail
        """
        if not username:
            return None

        try:
            users = self._read_users()
            if username in users:
                user_data = users[username]
                return User(
                    username=username,
                    name=user_data['name'],
                    password=user_data['password']
                )
            return None
        except KeyError as e:
            logging.error(f"Missing required user field: {str(e)}")
            raise DatabaseError("Invalid user data format")
        except Exception as e:
            logging.error(f"Error retrieving user: {str(e)}")
            raise DatabaseError(f"Failed to retrieve user: {str(e)}")

    def create_user(self, user: User) -> bool:
        """
        Create new user

        Args:
            user: User object to create

        Returns:
            bool: True if user created successfully, False if username exists

        Raises:
            DatabaseError: If database operations fail
        """
        if not user or not user.username:
            raise DatabaseError("Invalid user data")

        try:
            users = self._read_users()
            if user.username in users:
                return False

            users[user.username] = user.to_dict()
            self._write_users(users)
            return True

        except Exception as e:
            logging.error(f"Error creating user: {str(e)}")
            raise DatabaseError(f"Failed to create user: {str(e)}")
