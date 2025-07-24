from typing import Any
from fastapi import HTTPException, status
from database.project import static_projects
from models.project import ProjectModel


def find_project_by_id(id: int) -> ProjectModel:
    user: dict[Any, Any] | None = next((project for project in static_projects if project["id"] == id), None)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    return ProjectModel(**user)