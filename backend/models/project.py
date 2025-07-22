from pydantic import BaseModel, Field


class ProjectModel(BaseModel):
    name: str = Field(alias="projectName")