from sqlalchemy.orm import Session
from src.models.task_log import TaskLog
from src.schemas.task_logs import TaskLogCreate, TaskLogUpdate


def get_task_log(db: Session, log_id: int) -> TaskLog | None:
    return db.get(TaskLog, log_id)


def get_all_task_logs(db: Session, task_id: int | None = None) -> list[TaskLog]:
    query = db.query(TaskLog)
    if task_id is not None:
        query = query.filter(TaskLog.task_id == task_id)
    return query.all()


def create_task_log(db: Session, data: TaskLogCreate, user_id: int | None = None) -> TaskLog:
    obj_data = data.model_dump()
    if user_id:
        obj_data['user_id'] = user_id
    obj = TaskLog(**obj_data)
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
