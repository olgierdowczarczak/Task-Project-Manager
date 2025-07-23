from typing import Any
from pydantic import BaseModel, Field, PrivateAttr
from auth.auth import get_hashed_password


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
    _id: int = PrivateAttr()
    name: str
    password: str
    is_admin: bool = Field(alias="isAdmin")

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