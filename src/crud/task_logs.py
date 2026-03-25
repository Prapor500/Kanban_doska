from sqlalchemy.orm import Session
from src.models.task_log import TaskLog
from src.schemas.task_logs import TaskLogCreate, TaskLogUpdate


def get_task_log(db: Session, log_id: int) -> TaskLog | None:
    return db.query(TaskLog).filter(TaskLog.id == log_id).first()


def get_task_logs(db: Session, task_id: int, skip: int = 0, limit: int = 100) -> list[TaskLog]:
    return (
        db.query(TaskLog)
          .filter(TaskLog.task_id == task_id)
          .order_by(TaskLog.created_at.desc())
          .offset(skip)
          .limit(limit)
          .all()
    )


def create_task_log(db: Session, data: TaskLogCreate) -> TaskLog:
    obj = TaskLog(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update_task_log(db: Session, log_id: int, updates: TaskLogUpdate) -> TaskLog | None:
    obj = get_task_log(db, log_id)
    if not obj:
        return None
    for field, val in updates.model_dump(exclude_unset=True).items():
        setattr(obj, field, val)
    db.commit()
    db.refresh(obj)
    return obj


def delete_task_log(db: Session, log_id: int) -> TaskLog | None:
    obj = get_task_log(db, log_id)
    if not obj:
        return None
    db.delete(obj)
    db.commit()
    return obj
