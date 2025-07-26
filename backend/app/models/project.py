from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String
from database.database import Base


class ProjectModel(BaseModel):
    id: int
    name: str
    user_id: int = Field(alias="userId")
    
    class Config:
        allow_population_by_field_name = True
        populate_by_name = True
        from_attributes = True
    
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
        
class ProjectDb(Base):
    __tablename__: str = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    user_id = Column(Integer, default=0, nullable=False)