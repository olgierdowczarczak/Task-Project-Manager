from typing import Any
from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String, Boolean
from database.database import Base
from auth.auth import get_hashed_password


class UserModel(BaseModel):
    id: int
    name: str
    password: str
    is_admin: bool = Field(alias="isAdmin")
    
    class Config:
        allow_population_by_field_name = True
        populate_by_name = True
        from_attributes = True
        
class UserPublic(BaseModel):
    id: int
    name: str
    is_admin: bool = Field(alias="isAdmin")

    class Config:
        allow_population_by_field_name = True
        populate_by_name = True
        
class UserCreate(BaseModel):
    name: str
    password: str
    is_admin: bool = Field(default=False, alias="isAdmin")

    def model_post_init(self, _: Any) -> None:
        self.password = get_hashed_password(plain_password=self.password)
        
    class Config:
        allow_population_by_field_name = True
        populate_by_name = True
        
class UserUpdate(BaseModel):
    name: str
    is_admin: bool = Field(alias="isAdmin")

    class Config:
        allow_population_by_field_name = True
        populate_by_name = True
        
class UserDb(Base):
    __tablename__: str = "users"
    
    id: Column[int] = Column(Integer, primary_key=True, index=True)
    name: Column[str] = Column(String, nullable=False)
    password: Column[str] = Column(String, nullable=False)
    is_admin: Column[bool] = Column(Boolean, default=False, nullable=False)