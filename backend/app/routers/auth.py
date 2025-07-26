from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from auth.dependencies import get_db
from models.token import Token
from models.user import UserCreate
from services.auth import register_user, get_token


router: APIRouter = APIRouter(prefix="/auth", tags=["auth"])

@router.post(path="/register")
def register(user: UserCreate, session: Session = Depends(dependency=get_db)) -> Token:
    return register_user(session=session, user=user)

@router.post(path="/token")
def token(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(dependency=get_db)) -> Token:
    return get_token(session=session, username=form_data.username, password=form_data.password)