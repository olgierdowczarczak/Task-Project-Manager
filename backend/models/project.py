from pydantic import BaseModel, Field


class ProjectModel(BaseModel):
    id: int
    name: str
    manager_id: int = Field(alias="managerId")
    
    class Config:
        allow_population_by_field_name = True
        populate_by_name = True
    
class ProjectPublic(BaseModel):
    id: int
    name: str
    manager_id: int = Field(alias="managerId")
    
    class Config:
        allow_population_by_field_name = True
        populate_by_name = True
    
class ProjectCreate(BaseModel):
    name: str
    manager_id: int = Field(default=0, alias="managerId")
    
class ProjectUpdate(BaseModel):
    manager_id: int = Field(alias="managerId")
    
    class Config:
        allow_population_by_field_name = True
        populate_by_name = True