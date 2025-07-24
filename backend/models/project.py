from pydantic import BaseModel, Field


class ProjectModel(BaseModel):
    id: int
    name: str
    user_id: int = Field(alias="userId")
    
    class Config:
        allow_population_by_field_name = True
        populate_by_name = True
    
class ProjectPublic(BaseModel):
    id: int
    name: str
    user_id: int = Field(alias="userId")
    
    class Config:
        allow_population_by_field_name = True
        populate_by_name = True
    
class ProjectCreate(BaseModel):
    name: str
    user_id: int = Field(default=0, alias="userId")
    
class ProjectUpdate(BaseModel):
    user_id: int = Field(alias="userId")
    
    class Config:
        allow_population_by_field_name = True
        populate_by_name = True