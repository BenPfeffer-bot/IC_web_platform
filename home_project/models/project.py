# models/project.py
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
from enum import Enum

class ProjectStatus(Enum):
    PLANNING = "Planning"
    IN_PROGRESS = "In Progress"
    ON_HOLD = "On Hold"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"

class ProjectPriority(Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"

@dataclass
class ProjectMilestone:
    title: str
    due_date: datetime
    completed: bool = False
    completion_date: Optional[datetime] = None
    description: Optional[str] = None

@dataclass
class Project:
    id: str
    name: str
    description: str
    start_date: datetime
    end_date: datetime
    status: ProjectStatus
    priority: ProjectPriority
    budget: float
    spent: float = 0.0
    progress: float = 0.0
    milestones: List[ProjectMilestone] = None
    team_members: List[str] = None
    created_at: datetime = None
    updated_at: datetime = None

    def __post_init__(self):
        self.milestones = self.milestones or []
        self.team_members = self.team_members or []
        self.created_at = self.created_at or datetime.now()
        self.updated_at = self.updated_at or datetime.now()

    @property
    def budget_status(self) -> float:
        """Returns budget utilization percentage"""
        return (self.spent / self.budget * 100) if self.budget > 0 else 0

    @property
    def is_overdue(self) -> bool:
        """Check if project is overdue"""
        return datetime.now() > self.end_date and self.status != ProjectStatus.COMPLETED

