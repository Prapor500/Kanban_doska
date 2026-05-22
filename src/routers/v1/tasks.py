from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from src.core.services.db import get_db
from src.crud.tasks import (
    get_all_tasks, get_task,
    create_task, update_task, delete_task, move_task
)
from src.schemas.tasks import TaskCreate, TaskOut, TaskUpdate
from src.models.user import User
from src.core.services.auth_for_users import get_current_user_from_token

router_tasks = APIRouter(prefix="/tasks", tags=["tasks"])


@router_tasks.get("/", response_model=List[TaskOut])
def list_tasks(project_id: int | None = None, db: Session = Depends(get_db)):
    return get_all_tasks(db, project_id)


@router_tasks.get("/{task_id}", response_model=TaskOut)
def read_task(task_id: int, db: Session = Depends(get_db)):
    task = get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router_tasks.post("/", response_model=TaskOut)
def create_task_endpoint(
    data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token)
):
    return create_task(db, data, current_user.id)


@router_tasks.put("/{task_id}", response_model=TaskOut)
def update_task_endpoint(
    task_id: int, 
    data: TaskUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token)
):
    # Обычное обновление: позиция не передана — перемещение не требуется
    if data.position is None:
        task = update_task(db, task_id, data, user_id=current_user.id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return task

    # Перемещение задачи: определяем целевую колонку (текущая, если не задана)
    current_task = get_task(db, task_id)
    if not current_task:
        raise HTTPException(status_code=404, detail="Task not found")

    target_column_id = data.column_id if data.column_id is not None else current_task.column_id
    task = move_task(db, task_id, target_column_id, data.position, user_id=current_user.id)

    # Применяем остальные поля (title, description и т.д.) — position/column_id уже обработаны move_task
    remaining_data = data.model_dump(exclude={"position", "column_id"}, exclude_unset=True)
    if remaining_data:
        task = update_task(db, task_id, TaskUpdate(**remaining_data), user_id=current_user.id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router_tasks.delete("/{task_id}", response_model=TaskOut)
def delete_task_endpoint(task_id: int, db: Session = Depends(get_db)):
    task = delete_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
