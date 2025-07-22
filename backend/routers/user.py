from typing import Any
from fastapi import APIRouter, Depends
from auth.dependencies import get_current_active_user
from models.user import UserModelPublic


router: APIRouter = APIRouter(prefix="/users", tags=["users"])

@router.get(path="/me", response_model=UserModelPublic)
def me(user = Depends(dependency=get_current_active_user)) -> Any:
    return user