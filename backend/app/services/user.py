from sqlalchemy import text
from sqlalchemy.orm import Session
from fastapi import Response, HTTPException, status
from models.user import UserModel, UserDb, UserCreate, UserUpdate


def get_db_user_by_id(session: Session, id: int) -> UserDb:
    user: UserDb | None = session.query(UserDb).filter(UserDb.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

def get_db_user_by_name(session: Session, username: str) -> UserDb:
    user: UserDb | None = session.query(UserDb).filter(UserDb.name==username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

def get_users(session: Session, q: str) -> list[UserModel]:
    return [UserModel.model_validate(obj=user) for user in session.query(UserDb).filter(text(text=q)).all()]

def create_user_in_db(session: Session, user: UserCreate) -> UserModel:
    new_user: UserDb = UserDb(**user.model_dump())
    session.add(instance=new_user)
    session.commit()
    session.refresh(instance=new_user)
    return UserModel.model_validate(obj=new_user)

def get_user_by_id(session: Session, id: int) -> UserModel:
    return UserModel.model_validate(obj=get_db_user_by_id(session=session, id=id))

def get_user_by_name(session: Session, username: str) -> UserModel:
    return UserModel.model_validate(obj=get_db_user_by_name(session=session, username=username))

def update_user_by_id(session: Session, new_user: UserUpdate, id: int) -> UserModel:
    user: UserDb = get_db_user_by_id(session=session, id=id)
    for key, value in new_user.model_dump(exclude_unset=True).items():
        setattr(user, key, value)
    session.commit()
    session.refresh(instance=user)
    return UserModel.model_validate(obj=user)

def delete_user_by_id(session: Session, id: int) -> Response:
    user: UserDb = get_db_user_by_id(session=session, id=id)
    session.delete(instance=user)
    session.commit()
    return Response(content="OK", status_code=status.HTTP_204_NO_CONTENT)