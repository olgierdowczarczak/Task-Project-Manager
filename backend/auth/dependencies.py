from typing import Any
from datetime import datetime, timezone, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
import os
from .auth import verify_password
from database.user import static_users
from models.user import UserModel
from models.token import TokenData


oauth2_scheme: OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl="token")

def get_user(data: str|int) -> UserModel | None:
    user: Any | None = next((user for user in static_users if user["id"] == data), None) \
        if isinstance(data, int) else next((user for user in static_users if user["name"] == data), None)
    return UserModel(**user) if user else None
    
def authenticate_user(username: str, password: str) -> None | UserModel:
    user: UserModel | None = get_user(data=username)
    if not user:
        return None

    if not verify_password(plain_password=password, hashed_password=user.password):
        return None
    
    return user

def get_current_user(token: str = Depends(dependency=oauth2_scheme)) -> UserModel:
    try:
        username: str | None = jwt.decode(jwt=token, key=os.environ.get("CODE_KEY"), algorithms=[os.environ.get("CODE_ALGORITHM", default="")]).get("sub")
        if not username:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        token_data: TokenData = TokenData(name=username)
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    user: UserModel | None = get_user(data=token_data.name)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user

def get_current_active_user(user: UserModel = Depends(dependency=get_current_user)) -> UserModel:
    return user

def get_current_active_admin_user(user: UserModel = Depends(dependency=get_current_user)) -> UserModel:
    if user.is_admin is False:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
    return user

def create_access_token(data: dict[str, Any], expires_delta: timedelta | None = None) -> str:
    to_encode: dict[str, Any] = data.copy()
    to_encode.update({"exp": datetime.now(tz=timezone.utc) + expires_delta if expires_delta else datetime.now(tz=timezone.utc) + timedelta(minutes=15)})
    return jwt.encode(payload=to_encode, key=os.environ.get("CODE_KEY"), algorithm=os.environ.get("CODE_ALGORITHM"))