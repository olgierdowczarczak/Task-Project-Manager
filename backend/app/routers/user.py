from typing import Any
from fastapi import APIRouter, Response, Depends
from sqlalchemy.orm import Session
from auth.dependencies import get_current_active_admin_user
from database.dependencies import get_db
from models.user import UserModel, UserPublic, UserCreate, UserUpdate
from services.user import get_users, create_user_in_db, get_user_by_id, update_user_by_id, delete_user_by_id


router: APIRouter = APIRouter(prefix="/users", tags=["users"])

@router.get(path="/", response_model=list[UserPublic])
def get_all_users(q: str="", _: UserModel = Depends(dependency=get_current_active_admin_user), session: Session = Depends(dependency=get_db)) -> Any:
    return get_users(session=session, q=q)

@router.post(path="/", response_model=UserPublic)
def create_user(user: UserCreate, _: UserCreate = Depends(dependency=get_current_active_admin_user), session: Session = Depends(dependency=get_db)) -> Any:
    return create_user_in_db(session=session, user=user)

@router.get(path="/{id}", response_model=UserPublic)
def get_user(id: int, _: UserModel = Depends(dependency=get_current_active_admin_user), session: Session = Depends(dependency=get_db)) -> Any:
    return get_user_by_id(session=session, id=id)

@router.put(path="/{id}", response_model=UserPublic)
def update_user(id: int, user: UserUpdate, _: UserModel = Depends(dependency=get_current_active_admin_user), session: Session = Depends(dependency=get_db)) -> Any:
    return update_user_by_id(session=session, new_user=user, id=id)

@router.delete(path="/{id}")
def delete_user(id: int, _: UserModel = Depends(dependency=get_current_active_admin_user), session: Session = Depends(dependency=get_db)) -> Response:
    return delete_user_by_id(session=session, id=id)