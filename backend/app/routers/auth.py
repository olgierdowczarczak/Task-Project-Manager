from typing import Any
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from auth.dependencies import get_db, get_current_active_admin_user
from models.token import Token
from models.user import UserModel, UserCreate, UserPublic
from services.auth import register_user, get_token


router: APIRouter = APIRouter(prefix="/auth", tags=["auth"])

@router.post(path="/register")
def register(user: UserCreate, session: Session = Depends(dependency=get_db)) -> Token:
    return register_user(session=session, user=user)

@router.post(path="/token")
def token(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(dependency=get_db)) -> Token:
    return get_token(session=session, username=form_data.username, password=form_data.password)

@router.get(path="/me", response_model=UserPublic)
def get_me(user: UserModel = Depends(dependency=get_current_active_admin_user)) -> Any:
    return user