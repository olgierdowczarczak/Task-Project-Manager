from sqlalchemy import text
from sqlalchemy.orm import Session
from fastapi import Response, HTTPException, status
from models.task import TaskModel, TaskDb, TaskCreate, TaskUpdate


def get_db_task_by_id(session: Session, id: int) -> TaskDb:
    task: TaskDb | None = session.query(TaskDb).filter(TaskDb.id==id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task

def get_tasks(session: Session, q: str) -> list[TaskModel]:
    return [TaskModel.model_validate(obj=task) for task in session.query(TaskDb).filter(text(text=q)).all()]

def create_task_in_db(session: Session, task: TaskCreate) -> TaskModel:
    new_task: TaskDb = TaskDb(**task.model_dump())
    session.add(instance=new_task)
    session.commit()
    session.refresh(instance=new_task)
    return TaskModel.model_validate(obj=new_task)

def get_task_by_id(session: Session, id: int) -> TaskModel:
    return TaskModel.model_validate(obj=get_db_task_by_id(session=session, id=id))

def update_task_by_id(session: Session, new_task: TaskUpdate, id: int) -> TaskModel:
    task: TaskDb = get_db_task_by_id(session=session, id=id)
    for key, value in new_task.model_dump(exclude_unset=True).items():
        setattr(task, key, value)
    session.commit()
    session.refresh(instance=task)
    return TaskModel.model_validate(obj=task)

def delete_task_by_id(session: Session, id: int) -> Response:
    task: TaskDb = get_db_task_by_id(session=session, id=id)
    session.delete(instance=task)
    session.commit()
    return Response(content="OK", status_code=status.HTTP_204_NO_CONTENT)