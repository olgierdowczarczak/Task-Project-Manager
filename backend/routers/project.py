from fastapi import APIRouter, HTTPException, Response, Depends, status
from auth.dependencies import get_current_active_admin_user
from database.project import static_projects
from models.project import ProjectModel, ProjectPublic, ProjectCreate, ProjectUpdate
from models.user import UserModel
from services.project import find_project_by_id


router: APIRouter = APIRouter(prefix="/projects", tags=["projects"])

@router.get(path="/", response_model=list[ProjectPublic])
def get_projects(_: UserModel = Depends(dependency=get_current_active_admin_user)) -> list[ProjectPublic]:
    return [ProjectPublic(**project) for project in static_projects]

@router.post(path="/", response_model=ProjectPublic)
def create_project(project: ProjectCreate, _: UserModel = Depends(dependency=get_current_active_admin_user)) -> ProjectPublic:
    if any(db_project["name"] == project.name for db_project in static_projects):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Project with this name already exists")
    
    # for demo
    new_project_id: int = len(static_projects) + 1
    static_projects.append({"id": new_project_id}|project.model_dump())
    return ProjectPublic(id=new_project_id, **project.model_dump())

@router.get(path="/{id}", response_model=ProjectPublic)
def get_project_by_id(id: int, _: UserModel = Depends(dependency=get_current_active_admin_user)) -> ProjectPublic:
    return find_project_by_id(id=id) # type: ignore

@router.put(path="/{id}", response_model=ProjectPublic)
def update_project_by_id(id: int, data: ProjectUpdate, _: UserModel = Depends(dependency=get_current_active_admin_user)) -> ProjectPublic:
    project: ProjectModel = find_project_by_id(id=id)
    # for demo
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(project, key, value)
        static_projects[id-1].update({key: value})
        
    return project # type: ignore

@router.delete(path="/{id}")
def delete_project_by_id(id: int, _: UserModel = Depends(dependency=get_current_active_admin_user)) -> Response:
    find_project_by_id(id=id)
    del static_projects[id-1] # for demo
    return Response(content="OK")