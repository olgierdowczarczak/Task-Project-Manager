from typing import Any
from datetime import datetime, timezone, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
import os
from .auth import verify_password
from models.user import UserModel
from models.token import TokenData


oauth2_scheme: OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl="token")

# fake db
static_users: dict[str, Any] = {
    "tester1": {
        "name": "tester1",
        "password": "$2b$12$NslLj1flO6ce04lTGj6OHupbdVdTTG4AToP7dEJ7vw.YTcaAIouPq", # testpwd
        "is_admin": 1
    }
}

def get_user(username: str) -> UserModel | None:
    data: Any | None = static_users.get(username)
    return UserModel(**data) if data else None
    
def authenticate_user(username: str, password: str) -> None | UserModel:
    user: UserModel | None = get_user(username=username)
    if not user:
        return None
    
    if not verify_password(plain_password=password, hashed_password=user.password):
        return None
    
    return user

def get_current_user(token: str = Depends(dependency=oauth2_scheme)) -> UserModel:
    credentials_exception: HTTPException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload: dict[Any, str] = jwt.decode(jwt=token, key=os.environ.get("CODE_KEY"), algorithms=[os.environ.get("CODE_ALGORITHM", default="")])
        username: str | None = payload.get("sub")
        if not username:
            raise credentials_exception
        
        token_data: TokenData = TokenData(name=username)
    except:
        raise credentials_exception
        
    user: UserModel | None = get_user(username=token_data.name)
    if not user:
        raise credentials_exception
    
    return user

def get_current_active_user(user: UserModel = Depends(dependency=get_current_user)) -> UserModel:
    return user

def create_access_token(data: dict[str, Any], expires_delta: timedelta | None = None) -> str:
    to_encode: dict[str, Any] = data.copy()
    to_encode.update({"exp": datetime.now(tz=timezone.utc) + expires_delta if expires_delta else datetime.now(tz=timezone.utc) + timedelta(minutes=15)})
    return jwt.encode(payload=to_encode, key=os.environ.get("CODE_KEY"), algorithm=os.environ.get("CODE_ALGORITHM"))