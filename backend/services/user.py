from fastapi import HTTPException, status
from auth.dependencies import get_user
from models.user import UserModel


def find_user_by_id(id: int) -> UserModel:
    user: UserModel | None = get_user(data=id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    return user