from pydantic import BaseModel


class TaskModel(BaseModel):
    name: str
    status: int
    assignee: int
    deadline: int