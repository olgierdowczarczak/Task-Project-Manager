from pydantic import BaseModel, Field


class TaskModel(BaseModel):
    id: int
    project_id: int = Field(alias="projectId")
    name: str
    status: int
    user_id: int = Field(alias="userId")
    
    class Config:
        allow_population_by_field_name = True
        populate_by_name = True
        
class TaskPublic(BaseModel):
    id: int
    project_id: int = Field(alias="projectId")
    name: str
    status: int
    user_id: int = Field(alias="userId")
    
    class Config:
        allow_population_by_field_name = True
        populate_by_name = True
        
class TaskCreate(BaseModel):
    project_id: int = Field(alias="projectId")
    name: str
    status: int = Field(default=0)
    user_id: int = Field(default=0, alias="userId")
    
    class Config:
        allow_population_by_field_name = True
        populate_by_name = True

class TaskUpdate(BaseModel):
    project_id: int = Field(alias="projectId")
    name: str
    status: int
    user_id: int = Field(alias="userId")
    
    class Config:
        allow_population_by_field_name = True
        populate_by_name = True