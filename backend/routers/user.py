from fastapi import APIRouter, HTTPException, Response, Depends, status
from auth.dependencies import get_current_active_user, get_current_active_admin_user
from database.user import static_users
from models.user import UserModel, UserPublic, UserCreate, UserUpdate
from services.user import find_user_by_id


router: APIRouter = APIRouter(prefix="/users", tags=["users"])

@router.get(path="/", response_model=list[UserPublic])
def get_users(_: UserModel = Depends(dependency=get_current_active_admin_user)) -> list[UserPublic]:
    return [UserPublic(**user) for user in static_users]

@router.post(path="/", response_model=UserPublic)
def create_user(user: UserCreate, _: UserModel = Depends(dependency=get_current_active_admin_user)) -> UserPublic:
    if any(db_user["name"] == user.name for db_user in static_users):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this username already exists")
    
    static_users.append(user.model_dump()) # for demo
    return UserPublic(id=len(static_users), **user.model_dump())

@router.get(path="/me", response_model=UserPublic)
def me(user: UserModel = Depends(dependency=get_current_active_user)) -> UserPublic:
    return user # type: ignore

@router.get(path="/{id}", response_model=UserPublic)
def get_user_by_id(id: int, _: UserModel = Depends(dependency=get_current_active_admin_user)) -> UserPublic:
    return find_user_by_id(id=id) # type: ignore

@router.put(path="/{id}", response_model=UserPublic)
def update_user_by_id(id: int, data: UserUpdate, _: UserModel = Depends(dependency=get_current_active_admin_user)) -> UserPublic:
    user: UserModel = find_user_by_id(id=id)
    
    # for demo
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(user, key, value)
        static_users[id-1].update({key: value})
        
    return user # type: ignore

@router.delete(path="/{id}")
def delete_user_by_id(id: int, _: UserModel = Depends(dependency=get_current_active_admin_user)) -> Response:
    find_user_by_id(id=id)
    del static_users[id-1] # for demo
    return Response(content="OK")