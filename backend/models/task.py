from pydantic import BaseModel, Field


class TaskModel(BaseModel):
    name: str = Field(alias="taskName")
    status: int = Field(default=0, alias="taskStatus")
    assignee: int = Field(default=0, alias="taskAssignee")
    deadline: int = Field(default=0, alias="taskDeadline")