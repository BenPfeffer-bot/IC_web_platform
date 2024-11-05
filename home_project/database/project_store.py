import json
from typing import List, Optional, Dict
from datetime import datetime
from models.project import Project, ProjectStatus, ProjectPriority,ProjectMilestone
from core.exceptions import DatabaseError
from config.settings import settings
import logging

class ProjectStore:
    """Handles project data storage operations"""
    def __init__(self):
        self.file_path = settings.DATABASE_DIR / "projects.json"
        self._ensure_database_directory()

    def _ensure_database_directory(self) -> None:
        """Ensure database directory exists"""
        try:
            settings.DATABASE_DIR.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            logging.error(f"Failed to create database directory: {str(e)}")
            raise DatabaseError("Could not initialize database directory")

    def _serialize_project(self, project: Project) -> Dict:
        """Convert Project object to dictionary for storage"""
        return {
            "id": project.id,
            "name": project.name,
            "description": project.description,
            "start_date": project.start_date.isoformat(),
            "end_date": project.end_date.isoformat(),
            "status": project.status.value,
            "priority": project.priority.value,
            "budget": project.budget,
            "spent": project.spent,
            "progress": project.progress,
            "milestones": [
                {
                    "title": m.title,
                    "due_date": m.due_date.isoformat(),
                    "completed": m.completed,
                    "completion_date": m.completion_date.isoformat() if m.completion_date else None,
                    "description": m.description
                }
                for m in project.milestones
            ],
            "team_members": project.team_members,
            "created_at": project.created_at.isoformat(),
            "updated_at": project.updated_at.isoformat()
        }

    def _deserialize_project(self, data: Dict) -> Project:
        """Convert stored dictionary to Project object"""
        return Project(
            id=data["id"],
            name=data["name"],
            description=data["description"],
            start_date=datetime.fromisoformat(data["start_date"]),
            end_date=datetime.fromisoformat(data["end_date"]),
            status=ProjectStatus(data["status"]),
            priority=ProjectPriority(data["priority"]),
            budget=data["budget"],
            spent=data["spent"],
            progress=data["progress"],
            milestones=[
                ProjectMilestone(
                    title=m["title"],
                    due_date=datetime.fromisoformat(m["due_date"]),
                    completed=m["completed"],
                    completion_date=datetime.fromisoformat(m["completion_date"]) if m["completion_date"] else None,
                    description=m["description"]
                )
                for m in data["milestones"]
            ],
            team_members=data["team_members"],
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"])
        )

    def get_all_projects(self) -> List[Project]:
        """Retrieve all projects"""
        try:
            if not self.file_path.exists():
                return []
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return [self._deserialize_project(p) for p in data]
        except Exception as e:
            logging.error(f"Error reading projects: {str(e)}")
            raise DatabaseError(f"Failed to retrieve projects: {str(e)}")

    def get_project(self, project_id: str) -> Optional[Project]:
        """Retrieve specific project by ID"""
        projects = self.get_all_projects()
        return next((p for p in projects if p.id == project_id), None)

    def create_project(self, project: Project) -> bool:
        """Create new project"""
        try:
            projects = self.get_all_projects()
            if any(p.id == project.id for p in projects):
                return False
            
            projects.append(project)
            self._save_projects(projects)
            return True
        except Exception as e:
            logging.error(f"Error creating project: {str(e)}")
            raise DatabaseError(f"Failed to create project: {str(e)}")

    def update_project(self, project: Project) -> bool:
        """Update existing project"""
        try:
            projects = self.get_all_projects()
            for i, p in enumerate(projects):
                if p.id == project.id:
                    project.updated_at = datetime.now()
                    projects[i] = project
                    self._save_projects(projects)
                    return True
            return False
        except Exception as e:
            logging.error(f"Error updating project: {str(e)}")
            raise DatabaseError(f"Failed to update project: {str(e)}")

    def delete_project(self, project_id: str) -> bool:
        """Delete project by ID"""
        try:
            projects = self.get_all_projects()
            filtered_projects = [p for p in projects if p.id != project_id]
            if len(filtered_projects) == len(projects):
                return False
            self._save_projects(filtered_projects)
            return True
        except Exception as e:
            logging.error(f"Error deleting project: {str(e)}")
            raise DatabaseError(f"Failed to delete project: {str(e)}")

    def _save_projects(self, projects: List[Project]) -> None:
        """Save projects to file"""
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump([self._serialize_project(p) for p in projects], f, indent=2)
        except Exception as e:
            logging.error(f"Error saving projects: {str(e)}")
            raise DatabaseError(f"Failed to save projects: {str(e)}")