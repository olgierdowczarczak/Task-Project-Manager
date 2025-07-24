from typing import Any
from fastapi import HTTPException, status
from database.task import static_tasks
from models.task import TaskModel


def find_task_by_id(id: int) -> TaskModel:
    user: dict[Any, Any] | None = next((project for project in static_tasks if project["id"] == id), None)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    return TaskModel(**user)