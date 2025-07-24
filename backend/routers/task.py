from fastapi import APIRouter, Response, Depends
from auth.dependencies import get_current_active_admin_user
from database.task import static_tasks
from models.user import UserModel
from models.task import TaskModel, TaskPublic, TaskCreate, TaskUpdate
from services.task import find_task_by_id


router: APIRouter = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get(path="/", response_model=list[TaskPublic])
def get_tasks(_: UserModel = Depends(dependency=get_current_active_admin_user)) -> list[TaskPublic]:
    return [TaskPublic(**task) for task in static_tasks]

@router.post(path="/", response_model=TaskPublic)
def create_task(task: TaskCreate, _: UserModel = Depends(dependency=get_current_active_admin_user)) -> TaskPublic:
    # for demo
    new_task_id: int = len(static_tasks) + 1
    static_tasks.append({"id": new_task_id}|task.model_dump())
    return TaskPublic(id=new_task_id, **task.model_dump())

@router.get(path="/{id}", response_model=TaskPublic)
def get_task_by_id(id: int, _: UserModel = Depends(dependency=get_current_active_admin_user)) -> TaskPublic:
    return find_task_by_id(id=id) # type: ignore

@router.put(path="/{id}", response_model=TaskPublic)
def update_task_by_id(id: int, data: TaskUpdate, _: UserModel = Depends(dependency=get_current_active_admin_user)) -> TaskPublic:
    task: TaskModel = find_task_by_id(id=id)
    # for demo
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(task, key, value)
        static_tasks[id-1].update({key: value})
        
    return task # type: ignore

@router.delete(path="/{id}")
def delete_task_by_id(id: int, _: UserModel = Depends(dependency=get_current_active_admin_user)) -> Response:
    find_task_by_id(id=id)
    del static_tasks[id-1] # for demo
    return Response(content="OK")