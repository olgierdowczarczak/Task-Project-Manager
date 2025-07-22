from pydantic import BaseModel


class ProjectModel(BaseModel):
    name: str