from typing import Any
from fastapi import APIRouter, Response, Depends
from sqlalchemy.orm import Session
from auth.dependencies import get_current_active_admin_user
from database.dependencies import get_db
from models.project import ProjectPublic, ProjectCreate, ProjectUpdate
from models.user import UserModel
from services.project import get_projects, create_project_in_db, get_project_by_id, update_project_by_id, delete_project_by_id


router: APIRouter = APIRouter(prefix="/projects", tags=["projects"])

@router.get(path="/", response_model=list[ProjectPublic])
def get_all_projects(q: str="", _: UserModel = Depends(dependency=get_current_active_admin_user), session: Session = Depends(dependency=get_db)) -> Any:
    return get_projects(session=session, q=q)

@router.post(path="/", response_model=ProjectPublic)
def create_project(project: ProjectCreate, _: UserModel = Depends(dependency=get_current_active_admin_user), session: Session = Depends(dependency=get_db)) -> Any:
    return create_project_in_db(session=session, project=project)

@router.get(path="/{id}", response_model=ProjectPublic)
def get_project(id: int, _: UserModel = Depends(dependency=get_current_active_admin_user), session: Session = Depends(dependency=get_db)) -> Any:
    return get_project_by_id(session=session, id=id)

@router.put(path="/{id}", response_model=ProjectPublic)
def update_project(id: int, project: ProjectUpdate, _: UserModel = Depends(dependency=get_current_active_admin_user), session: Session = Depends(dependency=get_db)) -> Any:
    return update_project_by_id(session=session, new_project=project, id=id)

@router.delete(path="/{id}")
def delete_project(id: int, _: UserModel = Depends(dependency=get_current_active_admin_user), session: Session = Depends(dependency=get_db)) -> Response:
    return delete_project_by_id(session=session, id=id)