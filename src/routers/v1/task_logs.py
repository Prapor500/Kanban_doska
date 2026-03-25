from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from src.core.services.db import get_db
from src.crud.task_logs import get_task_log, get_task_logs, create_task_log, update_task_log, delete_task_log
from src.schemas.task_logs import TaskLogCreate, TaskLogOut, TaskLogUpdate

router_task_logs = APIRouter(prefix="/task-logs", tags=["task-logs"])


@router_task_logs.get("/", response_model=List[TaskLogOut])
def list_task_logs(
    task_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return get_task_logs(db, task_id, skip, limit)


@router_task_logs.post("/", response_model=TaskLogOut, status_code=status.HTTP_201_CREATED)
def create_task_log_endpoint(
    data: TaskLogCreate,
    db: Session = Depends(get_db)
):
    return create_task_log(db, data)


@router_task_logs.get("/{log_id}", response_model=TaskLogOut)
def get_task_log_endpoint(
    log_id: int,
    db: Session = Depends(get_db)
):
    log = get_task_log(db, log_id)
    if not log:
        raise HTTPException(status_code=404, detail="TaskLog not found")
    return log


@router_task_logs.put("/{log_id}", response_model=TaskLogOut)
def update_task_log_endpoint(
    log_id: int,
    data: TaskLogUpdate,
    db: Session = Depends(get_db)
):
    log = update_task_log(db, log_id, data)
    if not log:
        raise HTTPException(status_code=404, detail="TaskLog not found")
    return log


@router_task_logs.delete("/{log_id}", response_model=TaskLogOut)
def delete_task_log_endpoint(
    log_id: int,
    db: Session = Depends(get_db)
):
    log = delete_task_log(db, log_id)
    if not log:
        raise HTTPException(status_code=404, detail="TaskLog not found")
    return log
