from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
import os
from auth.dependencies import authenticate_user, create_access_token
from models.user import UserModel
from models.token import Token


router: APIRouter = APIRouter(prefix="/auth", tags=["auth"])

@router.post(path="/token")
def token(form_data: OAuth2PasswordRequestForm = Depends()) -> Token:
    user: None | UserModel = authenticate_user(username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect data", headers={"WWW-Authenticate": "Bearer"})
    
    return Token(access_token=create_access_token(data={"sub": user.name}, expires_delta=timedelta(minutes=int(os.environ.get("TOKEN_DURATION", default="15")))), token_type="bearer")