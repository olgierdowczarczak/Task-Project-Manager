from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String
from database.database import Base


class TaskModel(BaseModel):
    id: int
    project_id: int = Field(alias="projectId")
    name: str
    status: int
    user_id: int = Field(alias="userId")
    
    class Config:
        allow_population_by_field_name = True
        populate_by_name = True
        from_attributes = True
        
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
        
class TaskDb(Base):
    __tablename__: str = "tasks"
    
    id: Column[int] = Column(Integer, primary_key=True, index=True)
    project_id: Column[int] = Column(Integer, nullable=False)
    name: Column[str] = Column(String, nullable=False)
    status: Column[int] = Column(Integer, default=0, nullable=False)
    user_id: Column[int] = Column(Integer, default=0, nullable=False)