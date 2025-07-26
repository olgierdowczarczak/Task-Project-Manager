from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import timedelta
import os
from auth.auth import verify_password
from auth.dependencies import create_access_token
from models.token import Token
from models.user import UserModel, UserDb, UserCreate
from .user import get_user_by_name


def generate_token(username: str) -> Token:
    return Token(access_token=create_access_token(data={"sub": username}, expires_delta=timedelta(minutes=int(os.environ.get("TOKEN_DURATION", default="15")))), token_type="bearer")

def authenticate_user(session: Session, username: str, password: str) -> None | UserModel:
    user: UserModel | None = get_user_by_name(session=session, username=username)
    if not user:
        return None
    if not verify_password(plain_password=password, hashed_password=user.password):
        return None
    return user

def register_user(session: Session, user: UserCreate) -> Token:
    new_user: UserDb = UserDb(**user.model_dump())
    session.add(instance=new_user)
    session.commit()
    session.refresh(instance=new_user)
    return generate_token(username=user.name)

def get_token(session: Session, username: str, password: str) -> Token:
    user: None | UserModel = authenticate_user(session=session, username=username, password=password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect data", headers={"WWW-Authenticate": "Bearer"})
    return generate_token(username=user.name)