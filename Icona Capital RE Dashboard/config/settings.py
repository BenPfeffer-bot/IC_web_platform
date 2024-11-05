# config/settings.py

import pathlib
from dataclasses import dataclass, field
from typing import Dict

@dataclass
class Settings:
    """Application settings and constants"""
    # Directory settings
    BASE_DIR: pathlib.Path = pathlib.Path(__file__).parent.parent
    DATABASE_DIR: pathlib.Path = field(init=False)
    LOGO_DIR: pathlib.Path = field(init=False)

    # File paths
    USERS_FILE: pathlib.Path = field(init=False)
    PROJECTS_FILE: pathlib.Path = field(init=False)

    # Authentication settings
    MIN_PASSWORD_LENGTH: int = 6

    # UI settings
    ANIMATION_DURATION: int = 5

    # Dashboard settings
    ITEMS_PER_PAGE: int = 10
    DEFAULT_CURRENCY: str = "EUR"
    DATE_FORMAT: str = "%d-%m-%Y"

    # Project settings
    MAX_TEAM_MEMBERS: int = 20
    MIN_PROJECT_NAME_LENGTH: int = 3
    MAX_PROJECT_NAME_LENGTH: int = 100
    MIN_PROJECT_DESCRIPTION_LENGTH: int = 10
    MAX_PROJECT_DESCRIPTION_LENGTH: int = 1000

    # Cache settings
    CACHE_EXPIRY: int = 300  # 5 minutes

    # Color scheme
    COLORS: Dict[str, str] = field(default_factory=lambda: {
        'primary': '#1f77b4',
        'secondary': '#ff7f0e',
        'success': '#2ca02c',
        'warning': '#d62728',
        'info': '#17becf',
        'background': '#f0f2f6'
    })

    def __post_init__(self):
        """Initialize paths after BASE_DIR is set"""
        self.DATABASE_DIR = self.BASE_DIR / "data"
        self.LOGO_DIR = self.BASE_DIR / "statics" / "image"
        self.USERS_FILE = self.DATABASE_DIR / "users.json"
        self.PROJECTS_FILE = self.DATABASE_DIR / "projects.json"

# Instantiate settings so it can be imported and used in other modules
settings = Settings()
