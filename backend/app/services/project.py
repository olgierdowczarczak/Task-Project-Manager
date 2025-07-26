from sqlalchemy import text
from sqlalchemy.orm import Session
from fastapi import Response, HTTPException, status
from models.project import ProjectDb, ProjectModel, ProjectCreate, ProjectUpdate


def get_db_project_by_id(session: Session, id: int) -> ProjectDb:
    project: ProjectDb | None = session.query(ProjectDb).filter(ProjectDb.id==id).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return project

def get_projects(session: Session, q: str) -> list[ProjectModel]:
    return [ProjectModel.model_validate(obj=project) for project in session.query(ProjectDb).filter(text(text=q)).all()]

def create_project_in_db(session: Session, project: ProjectCreate) -> ProjectModel:
    new_project: ProjectDb = ProjectDb(**project.model_dump())
    session.add(instance=new_project)
    session.commit()
    session.refresh(instance=new_project)
    return ProjectModel.model_validate(obj=new_project)

def get_project_by_id(session: Session, id: int) -> ProjectModel:
    return ProjectModel.model_validate(obj=get_db_project_by_id(session=session, id=id))

def update_project_by_id(session: Session, new_project: ProjectUpdate, id: int) -> ProjectModel:
    project: ProjectDb = get_db_project_by_id(session=session, id=id)
    for key, value in new_project.model_dump(exclude_unset=True).items():
        setattr(project, key, value)
    session.commit()
    session.refresh(instance=project)
    return ProjectModel.model_validate(obj=project)

def delete_project_by_id(session: Session, id: int) -> Response:
    project: ProjectDb = get_db_project_by_id(session=session, id=id)
    session.delete(instance=project)
    session.commit()
    return Response(content="OK", status_code=status.HTTP_204_NO_CONTENT)