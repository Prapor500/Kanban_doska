from sqlalchemy.orm import Session
from src.models.task_log import TaskLog
from src.schemas.task_logs import TaskLogCreate, TaskLogUpdate


def get_task_log(db: Session, log_id: int) -> TaskLog | None:
    return db.get(TaskLog, log_id)


def get_all_task_logs(db: Session) -> list[TaskLog]:
    return db.query(TaskLog).all()


def create_task_log(db: Session, data: TaskLogCreate) -> TaskLog:
    obj = TaskLog(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update_task_log(db: Session, log_id: int, data: TaskLogUpdate) -> TaskLog | None:
    obj = get_task_log(db, log_id)
    if not obj:
        return None
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
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
