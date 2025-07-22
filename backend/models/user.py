from pydantic import BaseModel, Field


class UserModel(BaseModel):
    name: str = Field(alias="userName")
    password: str
    role: int = Field(default=0, alias="userRole")
    
class UserModelPublic(BaseModel):
    name: str = Field(alias="userName")