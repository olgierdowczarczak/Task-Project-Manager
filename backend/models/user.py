from pydantic import BaseModel, Field


class UserModel(BaseModel):
    id: int
    name: str
    password: str
    is_admin: bool = Field(alias="isAdmin")
    
    class Config:
        allow_population_by_field_name = True
        populate_by_name = True
        
class UserPublic(BaseModel):
    id: int
    name: str
    is_admin: bool = Field(alias="isAdmin")

    class Config:
        allow_population_by_field_name = True
        populate_by_name = True
        
class UserCreate(BaseModel):
    id: int = Field(default=0)
    name: str
    password: str
    is_admin: bool = Field(alias="isAdmin")

    class Config:
        allow_population_by_field_name = True
        populate_by_name = True
        
class UserUpdate(BaseModel):
    name: str
    is_admin: bool = Field(alias="isAdmin")

    class Config:
        allow_population_by_field_name = True
        populate_by_name = True