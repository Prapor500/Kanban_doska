from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session

from src.core.services.db import get_db
from src.crud.tasks import (
    get_task, get_tasks,
    create_task, update_task, delete_task
)
from src.schemas.tasks import TaskCreate, TaskOut, TaskUpdate

router_tasks = APIRouter(prefix="/tasks", tags=["tasks"])


@router_tasks.get("/", response_model=List[TaskOut])
def list_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_tasks(db, skip, limit)


@router_tasks.post("/", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
def create_task_endpoint(data: TaskCreate, db: Session = Depends(get_db)):
    return create_task(db, data)


@router_tasks.get("/{task_id}", response_model=TaskOut)
def get_task_endpoint(task_id: int, db: Session = Depends(get_db)):
    task = get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router_tasks.put("/{task_id}", response_model=TaskOut)
def update_task_endpoint(task_id: int, data: TaskUpdate, db: Session = Depends(get_db)):
    task = update_task(db, task_id, data)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router_tasks.delete("/{task_id}", response_model=TaskOut)
def delete_task_endpoint(task_id: int, db: Session = Depends(get_db)):
    task = delete_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
