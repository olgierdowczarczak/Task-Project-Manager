from pydantic import BaseModel, Field


class UserModel(BaseModel):
    name: str
    password: str
    is_admin: bool
        
class UserModelPublic(BaseModel):
    name: str
    is_admin: bool = Field(alias="isAdmin")