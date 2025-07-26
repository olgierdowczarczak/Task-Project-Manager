from typing import Any
from fastapi import APIRouter, Response, Depends
from sqlalchemy.orm import Session
from auth.dependencies import get_current_active_admin_user
from database.dependencies import get_db
from models.user import UserModel
from models.task import TaskPublic, TaskCreate, TaskUpdate
from services.task import get_tasks, create_task_in_db, get_task_by_id, update_task_by_id, delete_task_by_id


router: APIRouter = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get(path="/", response_model=list[TaskPublic])
def get_all_tasks(q: str = "", _: UserModel = Depends(dependency=get_current_active_admin_user), session: Session = Depends(dependency=get_db)) -> Any:
    return get_tasks(session=session, q=q)

@router.post(path="/", response_model=TaskPublic)
def create_task(task: TaskCreate, _: UserModel = Depends(dependency=get_current_active_admin_user), session: Session = Depends(dependency=get_db)) -> Any:
    return create_task_in_db(session=session, task=task)

@router.get(path="/{id}")
def get_task(id: int, _: UserModel = Depends(dependency=get_current_active_admin_user), session: Session = Depends(dependency=get_db)) -> Any:
    return get_task_by_id(session=session, id=id)

@router.put(path="/{id}", response_model=TaskPublic)
def update_project(id: int, task: TaskUpdate, _: UserModel = Depends(dependency=get_current_active_admin_user), session: Session = Depends(dependency=get_db)) -> Any:
    return update_task_by_id(session=session, new_task=task, id=id)

@router.delete(path="/{id}")
def delete_project(id: int, _: UserModel = Depends(dependency=get_current_active_admin_user), session: Session = Depends(dependency=get_db)) -> Response:
    return delete_task_by_id(session=session, id=id)